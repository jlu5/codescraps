#!/bin/bash
# Adds a new display resolution in TigerVNC using XRandr.
# TODO: validate that we're actually running in VNC

if [[ -z "$2" ]]; then
	echo "Needs two arguments: screen width and screen height."
	exit 1
fi

DISPLAYNAME="$(xrandr|sed -n 2p|cut -d ' ' -f 1)"

# Get the modeline info for the desired resolution.
CVT_OUTPUT="$(cvt $1 $2|tail -n 1)"

# Cut off the initial "Modeline" argument and send the rest to xrandr
XRANDR_ARGS=$(sed s/\\\"//g <<< "${CVT_OUTPUT[@]:9}")
echo "Sending $XRANDR_ARGS to XRandr..."
echo $XRANDR_ARGS
xrandr --newmode $XRANDR_ARGS  # No quotes here, it's not one big argument

# Add the new mode to the current display. This is the first argument
# of $XRANDR_ARGS
MODENAME="$(cut -f 1 -d ' ' <<< $XRANDR_ARGS)"
echo "Adding $MODENAME to display modes of $DISPLAYNAME"
xrandr --addmode "$DISPLAYNAME" "$MODENAME"

# Now, set the display to that resolution
xrandr -s "$MODENAME"
