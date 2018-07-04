from functionapproach3 import *
from abnfs import abnfs

"""
handler=abnf('myname        =  *5("Hallo" %x45 1*88("Fasel" ["Optional"]))',"blubber")
print ("Haalo")
print("regex",handler.get_regex())
print("name",handler.get_name())
print (abnf.__doc__)
"""

a=abnfs(['myname        =  *5("Hallo" %x45 1*88("Fasel" ["Optional"]))','ElonMusk="tesla"'])
a.add_abnf('myname        =  *5("Hallo" %x45 1*88("Fasel" ["Optional"])) ElonMusk')
print ("Endgültiger ausdruch:", a.get_regex('myname'))

print (a.get_all_regex())
