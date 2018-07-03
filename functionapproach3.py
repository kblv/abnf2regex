from exceptions import *
import binascii
import regex



abnfprimitives=dict()
abnfprimitives.update({"vchar":'[\x21-\x7E]'})
abnfprimitives.update({"cr":"\x0D"})
abnfprimitives.update({"lf":"\x0A"})
abnfprimitives.update({"alpha":'([\x41-\x5A]|[\x61-\x7A])'})
abnfprimitives.update({"sp":"\x20"})
abnfprimitives.update({"htab":"\x09"})
abnfprimitives.update({"dquote":'\x22'})
abnfprimitives.update({"prose-val":'(?:[\x20-\x3D] | [\x3F-\x7E])*'})
abnfprimitives.update({"digit":'[\x30-\x39]'})

def cleanup(abnf):
    abnf=regex.sub("^\s*","",abnf)
    return abnf


def __convertterminalvalue(prefix,value):
    if prefix == "b":
        char=b2a_qp(binvalue)
    if prefix == 'd':
        char=chr(charater)
    if prefix == 'x':
        print ("Value:", value)
        char=binascii.unhexlify(value).decode()
    return char

def __rulename(abnf):
    match=regex.match("<?(?<rulename>[A-Za-z][A-Za-z0-9\-]*)>?",abnf)
    if not match:
        raise NotMatchingABNFError("__rulename",abnf)
    print ("__rulename")
    rulename=match.group("rulename").lower()
    try:
        expression=abnfprimitives[rulename]
    except KeyError:
        #Here must be the lookup into the global tabel
        print("Key Error")
        pass
    return abnf[match.end():],expression

def __comment(abnf):
    match=regex.match(";.*",abnf)
    if not match:
        raise NotMatchingABNFError("__comment",abnf)
    print ("__comment")
    #Returning abnf empty and expression empty - as the comment is the
    #end of the abnf rule and it is not part of the rule
    return "",""

def __optionalsequence(abnf):
    match=regex.match("\[(?<content>.+)\]",abnf)
    if not match:
        raise NotMatchingABNFError("__optionalsequence",abnf)
    print ("__optionalsequence")
    notofinterest,expression=generalfunction(match.group("content"))
    return abnf[match.end():],"("+expression+")?"

def __variablerepetition(abnf):
    #Attention: The regex will match in every case, regardless of what is
    #in the string -> just the groups won't be there.
    #Reason is all expressions contain a * or ?, so they are all optional
    #in other words it even matches if nothing is there
    match=regex.match("(?<min>[0-9]*)((?<star>\*)(?<max>[0-9]*))?",abnf)
    min=0
    max=""
    if not match.group("min") and not match.group("star"):
        raise NotMatchingABNFError("__variablerepetition",abnf)
    print ("__variablerepetition")
    if match.group("min"):
        min=match.group("min")
    if match.group("max"):
        max=match.group("max")
    #In case of no star -> exact match -> min and max are same
    if not match.group("star"):
        max=match.group("min")
    #Get regular expression for next (foolow up) element -> the repetition is
    #in abnf before the elment, in regex after it
    print ("__variablerepetition before generalfunction",abnf[match.end():])
    abnf,expression=generalfunction(abnf[match.end():],chkhowmany=1)
    expression="("+expression+"){"+str(min)+","+str(max)+"}"
    return abnf, expression

def __sequencegroup(abnf):
    match=regex.match("\((?<content>.+)\)",abnf)
    if not match:
        raise NotMatchingABNFError("__sequencegroup",abnf)
    print ("__sequencegroup")
    notofinterest, expression=generalfunction(match.group("content"))
    expression="("+expression+")"
    return abnf[match.end():], expression

def __terminalvalue(abnf):
    expression=str()
    #match=regex.match('%(?<type>[bdx])(?<first>[0-9A-Z]+)(\.(?<more>([0-9A-Z])+))*',abnf)
    #match=regex.match('%(?<type>[bdx])(?<first>[0-9A-Z]+)(?<more>(\.[0-9A-Z]+)*)',abnf)
    match=regex.match('%(?<type>[bdx])(?<numbers>[0-9A-Z]+((\.[0-9A-Z]+)*))',abnf)
    if not match:
        raise NotMatchingABNFError("__terminalvalue",abnf)
    print ("__terminalvalue")
    #expression=__convertterminalvalue(match.group("type"),match.group("first"))
    #if match.group("more"):
    for value in regex.split('\.',match.group("numbers")):
        print(match.group("type"),value)
        expression+=__convertterminalvalue(match.group("type"),value)
    return abnf[match.end():], expression

def __valuerange(abnf):
    match=regex.match('%(?<type>[bdx])(?<first>[0-9A-Z]+)\-(?<second>[0-9A-Z]+)',abnf)
    if not match:
        raise NotMatchingABNFError("__valuerange",abnf)
    print ("__valuerange")
    firstchar=__convertterminalvalue(match.group("type"),match.group("first"))
    secondchar=__convertterminalvalue(match.group("type"),match.group("second"))
    return abnf[match.end():], '['+firstchar+'-'+secondchar+']'

def __alternative(abnf):
    match=regex.match("\=?/",abnf)
    if not match:
        raise NotMatchingABNFError("__alternative",abnf)
    print ("__alternative")
    return abnf[match.end():],"|"

def __dquote(abnf):
    print ("dquote abnf:",abnf)
    match=regex.match('\"(?<content>.+?)\"',abnf)
    if not match:
        raise NotMatchingABNFError("__dquote",abnf)
    print ("__dquote")
    print ("double quote", match.group("content"))
    print (match.end())
    return abnf[match.end():],match.group("content")

def starthere(abnf):
    name,abnf=seperatename(abnf)
    abnf,expression=generalfunction(abnf)
    #Here must be the update of the global abnflist
    #it needs to be checked whether the rule is already in the list
    #if yes append to the existing entry

def seperatename(rule):
    name,abnf=regex.split("=",rule,maxsplit=1)
    name=name.strip()
    name=regex.sub('/','',name)
    name=name.lower()
    return name,abnf

#Order matters, at least for valuerange and terminalvalue ->
#terminalvalue would match parts of valuerange
processfunctions=list()
processfunctions.append(__rulename)
processfunctions.append(__comment)
processfunctions.append(__optionalsequence)
processfunctions.append(__variablerepetition)
processfunctions.append(__sequencegroup)
processfunctions.append(__valuerange)
processfunctions.append(__terminalvalue)
processfunctions.append(__alternative)
processfunctions.append(__dquote)

def generalfunction(abnf,chkhowmany=0):
    checkedelements=0
    expression=str()
    origabnf=abnf
    abnf=cleanup(abnf)
    while len(abnf)>0:
        print (abnf)
        print ("Länge ABNF",len(abnf))
        for callnumber,function in enumerate(processfunctions):
            try:
                print ("abnf vor funktionsaufruf:",abnf)
                abnf, retexpression=function(abnf)
                expression+=retexpression
                break
            except NotMatchingABNFError:
                print("AbnfErrror in generalfunction")
                print("callnumber, len(processfunction)",callnumber,len(processfunctions)-1)
                if callnumber == len(processfunctions)-1:
                    raise InvalidABNFError(origabnf)
                continue
        checkedelements+=1
        print ("Expression",expression)
        if checkedelements==chkhowmany and chkhowmany:
            break
        abnf=cleanup(abnf)
    return abnf,expression
