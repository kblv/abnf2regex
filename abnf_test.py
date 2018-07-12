from functionapproach3 import *
from abnfs import abnfs

"""
handler=abnf('myname        =  *5("Hallo" %x45 1*88("Fasel" ["Optional"]))',"blubber")
print ("Haalo")
print("regex",handler.get_regex())
print("name",handler.get_name())
print (abnf.__doc__)
"""

a=abnfs()
a.add_abnf('Informational  =  "100"  /   "180"  /   "181"  /   "182"  /   "183"  ;  Session Progress')
a.add_abnf('extension-code  =  3DIGIT   ')
print (a.get_all_regex())
