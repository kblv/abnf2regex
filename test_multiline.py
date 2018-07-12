import regex

fhandle=open("infile.txt","r")

abnflist=list()
for line in fhandle:
	print ("line", line)
	line=(line.rsplit(';',1)[0])
	if regex.match('\s',line):
		line=regex.sub('$(\n|\r\n)','',line)
		abnflist[len(abnflist)-1]+=line
	else:
		abnflist.append(line)	

print abnflist
