from abnfserializer import *
from abnfs import abnfs


fhandle=open("infile.txt","r")
serializer=abnfserializer()
for line in fhandle:
    serializer.add_line(line)
abnflist=serializer.getabnf()
print(serializer.getabnf())

abnfo=abnfs()
for abnf in abnflist:
    abnfo.add_abnf(abnf)

resultdict=abnfo.get_all_regex()

for element,abnf in resultdict.items():
    print (element,":",abnf)
