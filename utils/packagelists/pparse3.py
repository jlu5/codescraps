#!/usr/bin/env python3
# HTML package listing script for aptly servers, as seen on https://packages.overdrivenetworks.com
# TODO: document exactly what this script does
import time
import subprocess
import sys
import shutil
import os
import re

### BEGIN CONFIGURATION VARIABLES ###

# Sets the folder where the generated package lists should go. This should be the same folder that
# contains the public dists/ and pool/ folders.
outdir = "/srv/aptly/public"

# A list of extra distributions to process.
extradists = ["sid-imports"]

# REGEX to look for snapshots for the distribution we're looking up. Defaults to ${dist}-YYYY-MM-DD.
# If this regex doesn't match a certain distribution, it is treated as its own repository in lookup.
snapshotregex_base = r'^%s-\d{4}-\d{2}-\d{2}'  # First %s is the distribution name

# Determines whether we should experimentally create pool/ links to each package entry. This may be
# time consuming.
showpoollinks = True

### END CONFIGURATION VARIABLES ###

if not shutil.which('aptly'):
    print('Error: aptly not found in path!')
    sys.exit(1)

print('Output directory set to: %s' % outdir)
repolist = subprocess.check_output(("aptly", "repo", "list", "-raw")).decode('utf-8').splitlines()
mirrorlist = subprocess.check_output(("aptly", "mirror", "list", "-raw")).decode('utf-8').splitlines()
repolist += mirrorlist
repolist += extradists
snapshotlist = subprocess.check_output(("aptly", "snapshot", "list", "-raw")).decode('utf-8').splitlines()

if showpoollinks:  # Pre-enumerate a list of all objects in pool/
    import pathlib
    poolobjects = list(pathlib.Path(outdir).glob('pool/*/*/*/*.*'))

def plist(dist):
    packagelist = []
    unique = set()
    snapshotregex = re.compile(snapshotregex_base % dist)
    try:
        try:  # Try to find a snapshot matching the distribution
            snapshotname = [s for s in snapshotlist if snapshotregex.search(s)][-1]
        except IndexError:  # If that fails, just treat it as a repo
            print('Using packages in repo %r...' % dist)
            packages_raw = subprocess.check_output(("aptly", "repo", "show", "-with-packages", dist)).splitlines()
        else:
            print('Using packages in snapshot %r...' % snapshotname)
            packages_raw = subprocess.check_output(("aptly", "snapshot", "show", "-with-packages", snapshotname)).splitlines()
    except subprocess.CalledProcessError:  # It broke, whatever...
        return
    for line in packages_raw:
        # We can't get a raw list of packages, but all package entries are indented... Use that.
        if line.startswith(b" "):
            # Each package is given as a string in the format packagename_version_arch
            fullname = line.decode("utf-8").strip()
            name, version, arch = fullname.split("_")

            # Track a list of unique source packages
            if arch == "source":
                 unique.add(name)

            packagelist.append((name, version, arch, fullname))
    # Sort everything by package name
    packagelist.sort(key=lambda k: k[0])

    os.chdir(outdir)
    with open('%s_list.html' % dist, 'w') as f:
        f.write("""<!DOCTYPE HTML>
<html>
<head><title>Package List for the Utopia Repository - {}</title>
<meta charset="UTF-8">
<meta name=viewport content="width=device-width">
<link rel="stylesheet" type="text/css" href="gstyle.css">
</head>
<body>
<a href="javascript:history.back()">Go back</a>
<br><br>
<table>
<tr>
<th>Package Name</th>
<th>Version</th>
<th>Architectures</th>
</tr>""".format(dist))
        for p in packagelist:
            # If enabled, try to find a link to the file for the package given.
            if showpoollinks:
                name, version, arch, fullname = p

                poolresults = subprocess.check_output(("aptly", "package", "show", "-with-files", fullname))

                # First, locate the raw filename corresponding to the package we asked for.
                filename = ''
                for line in poolresults.splitlines():
                    line = line.decode('utf-8')
                    if line.startswith('Filename:'):
                        # .deb's get a fancy "Filename: hello_1.0.0-1_all.deb" line in aptly's output.
                        filename = line.split(' ')[1]
                        break
                    elif arch == 'source' and '.dsc' in line:
                        # Source packages are listed as raw files in the pool though. Look for .dsc
                        # files in this case, usually in the line format
                        # 72c1479a7564c47cc2643336332c1e1d 711 utopia-defaults_2016.05.21+1.dsc
                        filename = line.split(' ')[-1]
                        break

                if filename:
                    # Then, once we've found the filename, look it up in the pool/ tree we made
                    # earlier.
                    #print("Found filename %s for %s" % (filename, fullname))
                    for poolfile in poolobjects:
                        if poolfile.name == filename:
                            # Filename matched found, make the "arch" field a relative link to the path given.
                            location = poolfile.relative_to(outdir)
                            arch = '<a href="%s">%s</a>' % (location, arch)
                            #print("Found %s for %s" % (poolfile, fullname))
                            break

                f.write(("""<tr><td>{}</td><td>{}</td><td>{}</td></tr>""".format(name, version, arch)))
        f.write("""</table>
<p><b>Total items:</b> {} ({} unique source packages)</p>
<p>Last updated {}</p>
</body></html>""".format(len(packagelist), len(unique), time.strftime("%I:%M:%S %p, %b %d %Y +0000", time.gmtime())))

if __name__ == "__main__":
    try:
        repolist = [sys.argv[1]]
    except IndexError:
        pass
    for dist in repolist:
        print('Processing package lists for %r.' % dist)
        plist(dist)
