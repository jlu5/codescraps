# version 0.2
# nsidentify.tcl script by d1g1t > sandeep[at]d1g1t[dot]net <
# Modified 2013 by GLolol > GLolol1[at]hotmail[dot]com <
# This script identifies your bot to NickServ whenever Nickserv asks it to identify
# useful when services go down and come back again in the absense of the owner

# Changes in v0.2: -GLolol
# Script now prints in console when it receives a request to identify and when identification is successful

# What NickServ says when it wants you to Identify
set nsrequest "*This?nickname?is?registered*Please?choose?a?different?nickname*or?identify?via*"

# NickServ's hostmask. To stop the bot from messaging fake people with pass
set nsmask "NickServ@services.overdrive.pw"

# Nickserv Pass
set nspass "RaZb0t-1001"

# If services allows you to identify to a nick you aren't on
# services like SurrealServices allow this
# Helpful when your nick is taken and you can be identified to it even before its release
# Yes - 1, No - 0
set idtomain 1

# If yes, What is the root nick
# Leave blank if idtomain is 0
set rootnick "RaZoR"

# What NickServ says when you identify successfully (optional really) -GLolol
set nsidsuccess "You?are?now?identified?for*"

## Don't really need to edit below this
# I assume nickserv interacts using notices
bind notc - * nsidentify
proc nsidentify {nick uhost hand text {dest ""}} {
	global botnick nsrequest nsmask nspass idtomain rootnick nsidsuccess
	if {$dest == ""} {set dest $botnick}
        if {[string match -nocase $nsrequest $text] && $nick == "NickServ" && $uhost == $nsmask} {
		putlog "Received NickServ request to identify, identifying with nsidentify.tcl..."
        if {$idtomain == 1 } { putmsg NickServ "IDENTIFY $rootnick $nspass" 
        } else { putmsg NickServ "IDENTIFY $nspass"} }
		if {[string match -nocase $nsidsuccess $text] && $nick == "NickServ" && $uhost == $nsmask} {
		putlog "Received NickServ identification successful. :)" }
}

putlog "\[LOADED\] nsidentify.tcl by d1g1t, modified by GLolol (v0.2)"
