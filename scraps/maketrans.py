# www.pythonchallenge.com/pc/def/map.html

import string

blah = string.lowercase
blah2 = string.lowercase[2:] + "ab"

print string.translate("g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj.", string.maketrans(blah, blah2))
print blah, blah2
print string.translate("map", string.maketrans(blah, blah2))