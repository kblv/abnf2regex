from functionapproach3 import *
from abnf import abnf

handler=abnf('myname        =  *5("Hallo" %x45 1*88("Fasel" ["Optional"]))',"blubber")
print ("Haalo")
print("regex",handler.get_regex())
print("name",handler.get_name())
