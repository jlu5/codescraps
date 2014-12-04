#!/usr/bin/env python
import random
import json
try: # Python 3
    from urllib.parse import urlencode
    from urllib.request import urlopen, Request
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen, Request
from sys import version_info, argv

if version_info[0] < 3:
    print("This script works best with Python 3+, please use that if possible "
    "(Python 2 suffers unicode decoding errors.")

global langs
langs = ('sw', 'sv', 'is', 'et', 'te', 'tr', 'mr', 'nl', 'sl', 
    'id', 'gu', 'hi', 'az', 'hmn', 'ko', 'da', 'bg', 'lo', 'so', 'tl', 
    'hu', 'ca', 'cy', 'bs', 'ka', 'vi', 'eu', 'ms', 'fr', 'no', 'hy', 
    'ro', 'ru', 'th', 'it', 'ta', 'sq', 'ceb', 'bn', 'de', 'zh-CN', 
    'be', 'lt', 'ne', 'fi', 'pa', 'iw', 'km', 'mt', 'ht', 'mi', 'lv', 
    'jw', 'sr', 'ar', 'ig', 'ha', 'pt', 'ga', 'af', 'zu', 'la', 'el', 
    'cs', 'uk', 'ja', 'hr', 'kn', 'gl', 'mk', 'fa', 'sk', 'mn', 'es', 
    'ur', 'pl', 'eo', 'yo', 'en', 'yi')

def _encode(m):
    # Currently doesn't work:
    # return m.encode("ascii","ignore") \
    #    if version_info[0] < 3 else m
    return m

def _getTranslation(sourceLang, targetLang, text):
    args = {"client": "p", "sl": sourceLang, "tl": targetLang, 'text': text}
    url = "http://translate.google.com/translate_a/t?" + urlencode(args)
    url = _encode(url)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urlopen(req).read()
    data = json.loads(data.decode("utf-8"))
    if "dict" in data:
        return data["dict"][0]["entry"][0]["word"]
    else:
        return data["sentences"][0]["trans"]

def wte(text):
    """wte <text>
        
    Worst Translations Ever! plugin. Translates <text> through
    multiple rounds of Google Translate to get amazing results!
    """
    outlang = 'en'
    ll = random.sample(langs, random.randint(6,12))
    for targetlang in ll:
        text = _encode(_getTranslation("auto", targetlang, text))
    text = _encode(_getTranslation("auto", outlang, text))
    text = text.strip()
    return text
    
if __name__ == '__main__':
    if argv[1:]:
        s = ' '.join(argv[1:])
    else:
        if version_info[0] >= 3:
            raw_input = input
        s = raw_input("Enter text to translate: ")
    print(wte(_encode(s)))
