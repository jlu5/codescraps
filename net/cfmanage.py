#!/usr/bin/env python3
###
# A Round Robin DNS manager for CloudFlare domains.
#
# Copyright (c) 2017 Ken Spencer <iota@electrocode.net>
# Copyright (c) 2017-2018 James Lu <james@overdrivenetworks.com>
#
# Some rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
###

import CloudFlare
import json
import configparser
import ipaddress

cf_conf = configparser.ConfigParser()
cf_conf.read('cfmanage.conf')
email = cf_conf['cloudflare']['api_login']
api_key = cf_conf['cloudflare']['api_key']
zone = cf_conf['cloudflare']['target_zone']

CF = None
base_domain = None

def setup():
    global CF, base_domain
    CF = CloudFlare.CloudFlare(email=email, token=api_key, raw=True)
    base_domain = CF.zones.get(zone)['result']['name']

def get_record_type(address):
    """
    Returns:
        - "A" if the address is an IPv4 address
        - "AAAA" if the address is an IPv6 address
        - "CNAME" if the address is neither of the above
    """
    if ' ' in address:
        raise ValueError("Unknown record type; use --type TYPE to override")
    try:
        ip = ipaddress.ip_address(address)
    except ValueError:
        return "CNAME"
    else:
        if isinstance(ip, ipaddress.IPv4Address):
            return "A"
        elif isinstance(ip, ipaddress.IPv6Address):
            return "AAAA"
        else:
            raise ValueError("Got unknown value %r from ipaddress.ip_address()" % address)

def cf_add(name, content, record_type=None, ttl=1, proxied=False):
    """Adds a DNS record with <content> to a subdomain <name>. TTL defaults to 1
    (automatic) if not given.
    """

    body = {
        'type':    record_type or get_record_type(content),
        'name':    name,
        'content': content,
        'ttl':     ttl,
        'proxied': proxied
    }

    response = CF.zones.dns_records.post(zone, data=body)
    result = response["result"]
    print("Record Added. %(name)s as %(content)s" % result)
    print("Record ID: %(id)s" % result)

def _show_records(response, page):
    """Displays all the DNS records given in "response", and returns the amount of records shown."""
    result_info = response['result_info']
    count = result_info['count']
    total_count = result_info['total_count']
    if not count:
        print('No results for zone %s / %s' % (zone, base_domain))
    else:
        print("Showing %d out of %d records in zone %s / %s (page %d)" %
                  (count, total_count, zone, base_domain, page))

        for res in response['result']:
            print("\t%(name)s\t%(type)s\t%(content)s" % res)
            print("\t\tID: %(id)s" % res)
    return count

RESULTS_PER_PAGE = 50
def cf_show(name=None, type=None, content=None, page=1, match_any=False):
    """
    Lists CloudFlare DNS records. Records can be filtered by name, type, and content.
    """

    params = {
        'per_page': RESULTS_PER_PAGE,
        'page':     page,
        'match':    "any" if match_any else "all"
    }
    if name:
        params['name'] = "%s.%s" % (name, base_domain)
    if type:
        params['type'] = type
    if content:
        params['content'] = content

    print('DEBUG: using params %s for cf_show' % params)
    response = CF.zones.dns_records.get(zone, params=params)

    _show_records(response, page)

def cf_edit(record_id, new_name=None, new_content=None, ttl=None, proxied=None):
    """
    Edits CloudFlare DNS records by record ID.
    """
    response = CF.zones.dns_records.get(zone, record_id)
    result = response['result']

    new_name = new_name or result['name']
    new_content = new_content or result['content']

    body = {
        'name':    new_name,
        'content': new_content,
        'type':    result['type']
    }
    if ttl is not None:
        body['ttl'] = ttl
    if proxied is not None:
        body['proxied'] = proxied
    response = CF.zones.dns_records.put(zone, record_id, data=body)
    result = response["result"]
    print("Record Edited. %(name)s as %(content)s" % result)

def cf_del(record_id):
    """
    Removes a record by its ID (Use cf_show() to display a list of records).
    """
    response = CF.zones.dns_records.delete(zone, record_id)
    result = response['result']
    print("Record removed. ID: %(id)s" % result)
cf_delete = cf_del  # Alias support

def cf_delall(name):
    """
    Removes all entries with the target entry name.
    """
    get_records_params = {'name': '%s.%s' % (name, base_domain)}
    removal_targets = CF.zones.dns_records.get(zone, params=get_records_params)

    print('Will remove the following records:')
    count = _show_records(removal_targets, page=1)
    if count:
        print('If the results span multiple pages, you may have to run this command multiple times.')
        print()

        for record in removal_targets['result']:
            cf_del(record['id'])
    else:
        print('No entries to remove.')

cf_deletall = cf_delall

def cf_pool(source_subdomain, target_subdomain):
    """
    Copies + merges all records from source subdomain into the target subdomain.
    This can be used to maintain IRC round robins, for example.
    """
    # API request body
    body = {'name': '%s.%s' % (source_subdomain, base_domain)}

    processed = 0
    # Iterate over all DNS records in the source subdomain
    for record in CF.zones.dns_records.get(zone, params=body)['result']:
        print('Copying record %s (%s, ttl %s) from %s.%s to %s.%s' %
              (record['id'], record['content'], record['ttl'],
               source_subdomain, base_domain, target_subdomain, base_domain))

        # Switch the record name and add them into the new subdomain
        record['name'] = target_subdomain
        CF.zones.dns_records.post(zone, data=record)
        processed += 1
    else:
        print('Done, processed %s result(s).' % processed)

def cf_depool(source_subdomain, target_subdomain):
    """
    Removes all entries in the target subdomain that are also present in the source subdomain.
    This can be used to maintain IRC round robins, for example.
    """
    # CloudFlare only allows removing entries by ID, so look up the exact record contents we need to remove here.
    get_source_records_params = {'name': '%s.%s' % (source_subdomain, base_domain)}
    removal_targets = [record['content'] for record in
                       CF.zones.dns_records.get(zone, params=get_source_records_params)['result']]

    target_body = {'name': '%s.%s' % (target_subdomain, base_domain)}
    # Iterate over all DNS records in the target subdomain
    target_records = CF.zones.dns_records.get(zone, params=target_body)['result']

    if len(removal_targets) > len(target_records):
        raise ValueError("Refusing to remove more records than there are in the target! Did you reverse the argument order?")

    processed = 0
    for record in target_records:
        if record['content'] in removal_targets:
            print('Removing record %s (%s, ttl %s) from %s.%s' %
                  (record['id'], record['content'], record['ttl'], target_subdomain, base_domain))
            response = CF.zones.dns_records.delete(zone, record['id'])
            processed += 1
    else:
        print('Done, processed %s result(s).' % processed)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='A Round Robin DNS manager for CloudFlare domains.')
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    parser_add = subparsers.add_parser('add', help="adds a DNS record (A/AAAA/CNAME are autodetected)")
    parser_add.add_argument('name', help="name of the new entry")
    parser_add.add_argument('content', help="content of the new entry")
    parser_add.add_argument('--type',    '-t', dest='record_type', type=str, help='DNS record type (leave blank to autodetect A/AAAA/CNAME)')
    parser_add.add_argument('--ttl',     '-l', type=int, help="record TTL (1=automatic)", default=1)
    parser_add.add_argument('--proxied', '-p', action="store_true", help="whether this record should pass through Cloudflare's CDN",
                            default=False)

    parser_edit = subparsers.add_parser('edit', help="edits a DNS record by ID")
    parser_edit.add_argument('record_id', type=str, help="record ID")
    parser_edit.add_argument('--name',    '-n', type=str, dest="new_name", help="new record name")
    parser_edit.add_argument('new_content', type=str, help="new record content (IP, etc.)", nargs='?')
    parser_edit.add_argument('--ttl',     '-l', type=int, help="new TTL (1=automatic)", default=1)
    parser_edit.add_argument('--proxied', '-p', action="store_true", help="whether this record should pass through Cloudflare's CDN",
                             default=False)

    parser_show = subparsers.add_parser('show', help="shows DNS records with optional filtering")
    parser_show.add_argument('name', nargs="?", help="only show records matching this name")
    parser_show.add_argument('--type',      '-t', type=str, help="only show records of this type")
    parser_show.add_argument('--content',   '-c', type=str, help="only show records with this content")
    parser_show.add_argument('--page',      '-p', type=int, help="page number to show", default=1)
    parser_show.add_argument('--match-any', '-a', action="store_true",
                            help="matches any of the selected filters (vs. the default of all of them)")

    parser_del = subparsers.add_parser('del', help="deletes a DNS record", aliases=["delete"])
    parser_del.add_argument('record_id', help="record ID to delete")

    parser_del = subparsers.add_parser('delall', help="deletes all DNS records matching a name", aliases=["deleteall"])
    parser_del.add_argument('name', help="entry name to clear")

    parser_pool = subparsers.add_parser('pool', help="pools a subdomain into a round robin")
    parser_pool.add_argument('source_subdomain', help="source subdomain")
    parser_pool.add_argument('target_subdomain', help="target (round-robin) subdomain")

    parser_depool = subparsers.add_parser('depool', help="depools a subdomain from a round robin")
    parser_depool.add_argument('source_subdomain', help="source subdomain")
    parser_depool.add_argument('target_subdomain', help="target (round-robin) subdomain")

    print("DEBUG: Got", parser.parse_args())

    # Pass the command details to the target functions as keyword args
    setup()
    cmd_vars = vars(parser.parse_args())
    func = globals()["cf_" + cmd_vars.pop('command')]
    func(**cmd_vars)
