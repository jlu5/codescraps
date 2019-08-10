#!/usr/bin/env python3
"""
Makes Windows' window borders loop in rainbow colors. Supports Windows 7 and Windows 10.

On Windows 10, this script works best if the accent color is applied to regular program windows as well
(enable Personalize -> Colors -> Show color on Start, taskbar, action center, and title bar).
"""

# Tweak this: lower value = faster
DELAY = 0.01
# Set this to true to also change the accent color on Windows 10. Note: this is VERY SLOW compared to changing
# the glass composition color, so it's recommended to bump DELAY to at least 0.1 seconds.
CHANGE_ACCENT_COLOR = True

import colorsys
import sys
import time

if sys.platform != 'win32':
    print('Sorry, this only works on Windows.', file=sys.stderr)
    sys.exit(1)

from ctypes import *
from ctypes.wintypes import *

# From http://www.pinvoke.net/default.aspx/dwmapi.DwmSetColorizationParameters
class DWM_COLORIZATION_PARAMS(Structure):
     _fields_ = [('clrColor', UINT), ('clrAfterGlow', UINT), ('nIntensity', UINT),
                 ('clrAfterGlowBalance', UINT), ('clrBlurBalance', UINT), ('clrGlassReflectionIntensity', UINT),
                 ('fOpaque', c_bool), ('AccentColor', UINT)]


# From https://github.com/RaMMicHaeL/Windows-10-Color-Control/blob/master/WindowsThemeColorApi.h
class IMMERSIVE_COLOR_PREFERENCES(Structure):
     _fields_ = [('color1', UINT), ('color2', UINT)]


# A lot of the functions to get and set color info are undocumented functions, but we can access them
# by their ordinal.
# From the dump at https://theroadtodelphi.com/2011/05/05/changing-the-glass-composition-color-dwm-using-delphi/
GetColorizationParameters = windll.dwmapi[127]
SetColorizationParameters = windll.dwmapi[131]

# From https://github.com/RaMMicHaeL/Windows-10-Color-Control/blob/master/WindowsThemeColorApi.cpp#L42
SetUserColorPreference = windll.uxtheme[122]

def hex_to_rgb(hexcolor):
    # Take a hex color in the form "0xefff5c00" to r, g, b value pairs
    # Note: we ignore the first two hex digits since we don't need the intensity/transparency value yet.
    r, g, b = hexcolor[4:6], hexcolor[6:8], hexcolor[8:10]
    r, g, b = map(lambda num: int(num, 16), (r, g, b))
    print('hex_to_rgb of %s: %s, %s, %s' % (hexcolor, r, g, b))
    return (r, g, b)

current_params = DWM_COLORIZATION_PARAMS()
# Get* functions for dwmapi, uxtheme, etc. take a pointer for the function to store its output in
# We can use ctypes.byref to pass it this way.
GetColorizationParameters(byref(current_params))
current_color = hex_to_rgb(hex(current_params.clrColor))

# Start off with a HSV value which will be incrimented. Although Windows uses RGB internally,
# it's easier to increment values here and convert them later.
# Start the rainbow at the hue the system is currently using.
hsv_color = [colorsys.rgb_to_hsv(*current_color)[0], 1, 1]

def new_color():
    global hsv_color
    rgb_color = colorsys.hsv_to_rgb(*hsv_color)
    # Increment the hsv color for the next call.
    if hsv_color[0] < 1:
        hsv_color[0] += 0.01
    else:
        hsv_color[0] = 0.0
    print(hsv_color)
    print(rgb_color)

    # Convert the decimal color space value to one between 0-255.
    hexcolor = [format(int(min(255, round(n*255))), '02x') for n in rgb_color]

    # For Windows 10, the accent color has to be reversed for some reason...
    # https://github.com/RaMMicHaeL/Windows-10-Color-Control/blob/master/WindowsThemeColorApi.cpp#L54
    hexcolor_reversed = [format(int(min(255, round(n*255))), '02x') for n in reversed(rgb_color)]

    # TODO: make intensity configurable
    colorstring = '0xEF%s' % ''.join(hexcolor)
    colorstring_reversed = '0xEF%s' % ''.join(hexcolor_reversed)
    print(colorstring, colorstring_reversed)
    return (int(colorstring, base=16), int(colorstring_reversed, base=16))

if __name__ == '__main__':
    has_composition = c_bool()
    windll.dwmapi.DwmIsCompositionEnabled(byref(has_composition))
    if not has_composition.value:
        print('Composition is not enabled, aborting!', file=sys.stderr)
        sys.exit(1)

    win_version = sys.getwindowsversion()[0]
    while True:
        next_colors = new_color()

        current_params = DWM_COLORIZATION_PARAMS()
        GetColorizationParameters(byref(current_params))

        # Debug: print all DWM_COLORIZATION_PARAMS fields
        for field in current_params._fields_:
            print(field[0], getattr(current_params, field[0]))

        # Update the color in our struct and pass it to SetColorizationParameters
        # XXX: find out what the boolean arg actually does?
        current_params.clrColor = next_colors[0]
        SetColorizationParameters(byref(current_params), byref(c_bool(1)))

        # On Windows 10, update the accent color as well
        if win_version >= 10 and CHANGE_ACCENT_COLOR:
            colorpref_params = IMMERSIVE_COLOR_PREFERENCES()
            windll.uxtheme.GetUserColorPreference(byref(colorpref_params), byref(c_bool(0)))
            print('uxtheme colors:', colorpref_params.color1, colorpref_params.color2)
            colorpref_params.color2 = next_colors[1]
            SetUserColorPreference(byref(colorpref_params), byref(c_bool(1)))

        time.sleep(DELAY)
