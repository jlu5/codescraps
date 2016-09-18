#!/usr/bin/env python2
"""bconv.py - Script to parse relayer text in chatlogs, making them available to stats generators like PISG."""

### Configuration ###

import datetime
import os
import re
from sys import argv
import glob

yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
if len(argv) >= 2:
    filelist = argv[1:]
else:
    filelist = glob.glob('/home/gl/pisglog/ovd_#*_%s.log' % datetime.datetime.now().strftime('%Y%m%d'))
    filelist += glob.glob('/home/gl/pisglog/ovd_#*_%s.log' % yesterday.strftime('%Y%m%d'))

outfile_dir = '/home/gl/pisglog'
outfile_prefix = ''
outfile_suffix = '.conv'

### Converter ###
convmsg = re.compile(r"<.+?> \x02?\[.+?\]\x02? <[@%+]?-?(?:\x03|\d)*-?(.*?)\x03?>", re.I)
convme = re.compile(r"<.+?> \x02?\[.+?\]\x02? \* [@%+]?-?(?:\x03|\d)*-?(.*?)\x03?", re.I)
convmode = re.compile(r"<.+?> \x02?\[.+?\]\x02? [@%+]?-?(?:\x03|\d)*-?(.*?)\x03? \(.*?\) set mode (.*?) on .*", re.IGNORECASE)
convjoin = re.compile(r"<.+?> \x02?\[.+?\]\x02? [@%+]?-?(?:\x03|\d)*-?(.*?)\x03? \((.*?)\) has joined .*", re.IGNORECASE)
convpart = re.compile(r"<.+?> \x02?\[.+?\]\x02? [@%+]?-?(?:\x03|\d)*-?(.*?)\x03? \((.*?)\) has parted .*", re.IGNORECASE)
convquit = re.compile(r"<.+?> \x02?\[.+?\]\x02? [@%+]?-?(?:\x03|\d)*-?(.*?)\x03? has quit .*", re.IGNORECASE)
convnick = re.compile(r"<.+?> \x02?\[.+?\]\x02? [@%+]?-?(?:\x03|\d)*-?(.*?)\x03? is now known as \x03\d\d(.*?)\x03", re.IGNORECASE)
convkick = re.compile(r"<.+?> \x02?\[.+?\]\x02? [@%+]?-?(?:\x03|\d)*-?(.*?)\x03? \(.*?\) has been kicked from .*? by (.*?) \((.*?)\)", re.IGNORECASE)
# PISG doesn't like slashes in nicks. Clobber them.
convslash = re.compile(r"<(.*?)\/(.*?)>", re.IGNORECASE)
convslashme = re.compile(r"\* (.*?)\/(.*?) (.*)", re.IGNORECASE)

def _conv(infile):
    inread = open(infile)
    os.chdir(outfile_dir)
    outfilename = '%s%s%s' % (outfile_prefix, infile, outfile_suffix)
    outfile = open(outfilename, 'w')
    for line in inread:
        line = line.replace("\u200b", "")
        line = convmsg.sub(r"<\1>", line)
        line = convmode.sub(r"*** \1 sets mode: \2", line)
        line = convjoin.sub(r"*** Joins: \1 (\2)", line)
        line = convpart.sub(r"*** Parts: \1 (\2) ()", line)
        line = convquit.sub(r"*** Quits: \1 (generic@placeholder.host) ()", line)
        line = convnick.sub(r"*** \1 is now known as \2", line)
        line = convkick.sub(r"*** \1 was kicked by \2 (\3)", line)
        line = convme.sub(r"* \1", line)
        line = convslash.sub(r"<\1>", line)
        line = convslashme.sub(r"* \1 \3", line)
        outfile.write(line)
    inread.close()
    outfile.close()
    return outfilename

for file in sorted(filelist):
    outname = _conv(file)
    print('Converted file: %s => %s' % (file, outname))
print('Finished, converted a total of %s file(s).' % len(filelist))
