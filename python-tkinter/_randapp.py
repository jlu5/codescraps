import random
import string

def randapp():
    """Generates a random Windows-like application name.
    Please excuse the ridiculousness of this, it's merely a joke."""
    # Portions of below list taken from 
    # http://download.cnet.com/windows/most-popular/3101-20_4-0.html
    appPrefixes = ("GoogleChrome","FirefoxBrowser","Windows",
            "WindowsMediaPlayer","MicrosoftOffice","Antivirus",
            "SystemCleaner","YouTubeDownloader","DriverBoost",
            "SystemBooster","Virtual","InternetDownloader",
            "WindowsShield","3DMax","GamerBoostPro","AOLToolbar",
            "VLCMediaPlayer","WinRAR","IrfanView","VideoConverter",
            "UniversalDriverManager")
    appSuffixes = ("FreeDownloader","Installer","Free")
    s = string.ascii_letters+'aeiouAEIUO'
    s = ''.join(random.sample(s,random.randint(2,4)))
    appnames = ("svchost.exe","winlogon.exe","lsass.exe","explorer.exe",
            "iexplore.exe","taskhost.exe","smss.exe","spoolsv.exe",
            "wininit.exe","rundll32.exe","iexplorer.exe",
            "rundll16.com","windowsdownloadFree.exe","K"+"eygen.exe",
            "Setup.exe","csrss.exe", "System.exe","VLCMediaPlay.exe",
            "wmplayer.exe","dllhost.exe","WINWORD.exe","EXCEL.exe",
            "_ISDEL.exe","anttiviruspro.exe","chrome.exe", "_%ss.tmp"%s,
            "firefox.exe","winSecure.exe","wmiprvse.exe","agent.exe")
    r = random.random()

    if r >= 0.86:
        s = '%smgr' % s
    elif r >= 0.8:
        s = '%smon' % s
    elif r >= 0.77:
        s = '%sinit' % s
    elif r >= 0.62:
        s = 'winnt%s'%s
    elif r >= 0.55:
        s = '%sahost'%s
    elif r >= 0.46:
        s = '%ssvc' % s
    elif r >= 0.19: return random.choice(appnames)
    else: return '%s.exe' % (random.choice(appPrefixes)+random.choice(appSuffixes))[:random.randint(25,30)]
    return s[-8:]+'.exe'

if __name__ == "__main__": 
    for _ in range(10): print randapp()