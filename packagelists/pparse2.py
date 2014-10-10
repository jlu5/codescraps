import fileinput, time
archs = ("amd64", "i386")

packagelist = []
unique = set()
for line in fileinput.input():
    if line.startswith(" "):
        s = line.strip().split("_")
        if s[2] == "all":
            for a in archs:
                packagelist.append({'pkg': s[0], 'ver': s[1], 
                            'arch': a})
        else:
            packagelist.append({'pkg': s[0], 'ver': s[1], 
                            'arch': s[2]})
        unique.add(s[0])
# Sort everything by package name
packagelist.sort(key=lambda k: k['pkg'])

print """<!DOCTYPE HTML>
<html>
<head><title>Package List for GLolol's Utopia Repository</title>
<meta charset="UTF-8">
<link rel="stylesheet" type="text/css" href="gstyle.css">
</head>
<body>
<table>
<tr>
<th>Package Name</th>
<th>Version</th>
<th>Architectures</th>
</tr>"""
for p in packagelist:
    print("""<tr><td>{}</td><td>{}</td><td>{}</td></tr>"""
        .format(p.get('pkg'), p.get('ver'), p.get('arch')))
print """</table>
<p><b>Total items:</b> {} ({} unique package names)</p>
<p>Last updated {}</p>
</body></html>""".format(len(packagelist), len(unique), time.strftime("%I:%M:%S %p, %b %d %Y +0000", time.gmtime()))
