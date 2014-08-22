#!/usr/bin/python2
### Configuration ###

import datetime, glob, argparse, os, sys, re

yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
#filelist = glob.glob('/home/gl/pisglog/ovd_#chat_*.log')
filelist = ['/home/gl/pisglog/ovd_#chat_%s.log' % \
    s.strftime('%Y%m%d') for s in (datetime.datetime.now(), yesterday)]
outfile_dir = '/home/gl/pisglog'
outfile_prefix = ''
outfile_suffix = '.conv'

### Converter ###
convmsg = re.compile(r"<(Nebulae.*?|Lily.*?)>.*?<-\x03\d\d(.*?)\x03>", re.IGNORECASE)
convme = re.compile(r"<(Nebulae.*?|Lily.*?)>.*?-\x03\d\d(.*?)\x03", re.IGNORECASE)
convmode = re.compile(r"<(Nebulae.*?|Lily.*?)>.*?\].*? \x03\d\d(.*?)\x03 \(.*?\) set mode (.*?) on .*", re.IGNORECASE)
convmode2 = re.compile(r"<(Nebulae.*?|Lily.*?)>.*?\].*? -?(.*?) set mode (.*?) on .*", re.IGNORECASE)
convjoin = re.compile(r"<(Nebulae.*?|Lily.*?)>.*?\].*? \x03\d\d-?(.*?)\x03 \((.*?)\) has joined .*", re.IGNORECASE)
convpart = re.compile(r"<(Nebulae.*?|Lily.*?)>.*?\].*? \x03\d\d-?(.*?)\x03 \((.*?)\) has parted .*", re.IGNORECASE)
convquit = re.compile(r"<(Nebulae.*?|Lily.*?)>.*?\].*? \x03\d\d-?(.*?)\x03 has quit .*", re.IGNORECASE)
convnick = re.compile(r"<(Nebulae.*?|Lily.*?)>.*?\].*? \x03\d\d-?(.*?)\x03 is now known as \x03\d\d(.*?)\x03", re.IGNORECASE)
convkick = re.compile(r"<(Nebulae.*?|Lily.*?)>.*?\].*? \x03\d\d-?(.*?)\x03 \(.*?\) has been kicked from .*? by (.*?) \((.*?)\)", re.IGNORECASE)

def _conv(infile):
    inread = open(infile)
    os.chdir(outfile_dir)
    outfilename = '%s%s%s' % (outfile_prefix, infile, outfile_suffix)
    outfile = open(outfilename, 'w')
    for line in inread:
        line = convmsg.sub(r"<\2>", line)
        line = convme.sub(r"* \2", line)
        line = convmode.sub(r"*** \2 sets mode: \3", line)
        line = convmode2.sub(r"*** \2 sets mode: \3", line)
        line = convjoin.sub(r"*** Joins: \2 (\3)", line)
        line = convpart.sub(r"*** Parts: \2 (\3) ()", line)
        line = convquit.sub(r"*** Quits: \2 (generic@placeholder.host) ()", line)
        line = convnick.sub(r"*** \2 is now known as \3", line)
        line = convkick.sub(r"*** \2 was kicked by \3 (\4)", line)
        outfile.write(line)
    inread.close()
    outfile.close()

for file in sorted(filelist):
    _conv(file)
    print('Converted file: %s' % file)
print('Finished, converted a total of %s file(s).' % len(filelist))
