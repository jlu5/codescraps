from HTMLParser import HTMLParser

class metarefreshParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            L = dict(attrs)
            try:
                if L['http-equiv'] == "refresh":
                    ct = L['content'].lower().split("url=", 1)
                    print("Meta refresh target: {} (after {} seconds)".format(ct[1], int(ct[0].split(";")[0])))
            except KeyError: pass
            except ValueError: 
                print "Meta-refresh detected, but there was an error parsing it (non-standard HTML?)"
            except IndexError:
                print "Meta-refresh detected: current page (after {} seconds)".format(L['content'])

parser = metarefreshParser()
parser.feed("""
<html><head><title>Test</title></head>

<meta http-equiv="refresh" content="5; url=http://example.com/">
<meta http-equiv="refresh" content="url=http://example.com/; 77">
<meta>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="80;">
<meta http-equiv="refresh" content="5">
<meta http-equiv="refresh" content="0; url=http://example.com/">

<body><h1>Parse me!</h1></body></html>""")