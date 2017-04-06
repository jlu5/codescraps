"""
Makes Windows' window borders loop in rainbow colors. Supports Windows 7 and Windows 10.

On Windows 10, this script works best if the accent color is applied to regular program windows as well
(enable Personalize -> Colors -> Show color on Start, taskbar, action center, and title bar).
"""

# Tweak this: lower value = faster
DELAY = 0.1

import colorsys
import sys
import time
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


# A lot of the functions to get and set color info are unexported functions, but we can access them
# by their ordinal.
# From the dump at https://theroadtodelphi.com/2011/05/05/changing-the-glass-composition-color-dwm-using-delphi/
GetColorizationParameters = windll.dwmapi[127]
SetColorizationParameters = windll.dwmapi[131]

# From https://github.com/RaMMicHaeL/Windows-10-Color-Control/blob/master/WindowsThemeColorApi.cpp#L42
SetUserColorPreference = windll.uxtheme[122]

# Start off with a HSV value. Although Windows uses RGB internally,
# it's easier to increment values here and convert them later.
hsv_color = [0.0, 1, 1]

def newColor():
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
    #hexcolor = ['%02x' % int(n) for n in rgb_color]
    hexcolor = [format(int(min(255, round(n*255))), '02x') for n in rgb_color]
    colorstring = '0xEF%s' % ''.join(hexcolor)
    print(colorstring)
    return UINT(int(colorstring, base=16))

has_composition = c_bool()
windll.dwmapi.DwmIsCompositionEnabled(byref(has_composition))
if not has_composition.value:
    print('Composition is not enabled, aborting!')
    sys.exit(1)

win_version = sys.getwindowsversion()[0]
while True:
    next_color = newColor()

    current_params = DWM_COLORIZATION_PARAMS()
    # Get* functions for dwmapi, uxtheme, etc. take a pointer for the function to store its output in
    # We can use ctypes.byref to pass it this way.
    GetColorizationParameters(byref(current_params))

    # Debug: print all DWM_COLORIZATION_PARAMS fields
    for field in current_params._fields_:
        print(field[0], getattr(current_params, field[0]))

    # Update the color in our struct and pass it to SetColorizationParameters
    # XXX: find out what the boolean arg actually does?
    current_params.clrColor = next_color
    SetColorizationParameters(byref(current_params), byref(c_bool(1)))

    # On Windows 10, update the accent color as well
    if win_version >= 10:
        colorpref_params = IMMERSIVE_COLOR_PREFERENCES()
        windll.uxtheme.GetUserColorPreference(byref(colorpref_params), byref(c_bool(0)))
        print('uxtheme colors:', colorpref_params.color1, colorpref_params.color2)
        colorpref_params.color2 = next_color
        SetUserColorPreference(byref(colorpref_params), byref(c_bool(1)))

    time.sleep(DELAY)