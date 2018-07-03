from exceptions import *

#repetition="(?<first>[0-9]*)\*(?<second>[0-9]*)"
repetition="(?<first>[0-9]*)\*(?<second>[0-9]*)"

abnfprimitives=dict()
abnfprimitives.update({"VCHAR":'[\x21-\x7E]'})
abnfprimitives.update({"CR":"\x0D"})
abnfprimitives.update({"LF":"\x0A"})
abnfprimitives.update({"ALPHA":'[\x41-\x5A]|[\x61-\x7A]'})
abnfprimitives.update({"SP":"\x20"})
abnfprimitives.update({"HTAB":"\x09"})
abnfprimitives.update({"DQUOTE":'\x22'})
abnfprimitives.update({"prose-val":'(?:[\x20-\x3D] | [\x3F-\x7E])*'})
abnfprimitives.update({"DIGIT":'[\x30-\x39]')

processfunctions=list()
processfunctions.append(__doublequote)
processfunctions.append(__braket)
processfunctions.append(__option)
processfunctions.append(__repetition)
processfunctions.append(__keyword)


def cleanup(abnf):
    regex.sub("^\s*","",abnf)
    return abnf

def __check_or(aabnf,stringtoparse):
    groupoptioncounter=0
    doublequotecounter=0
    escapeseen=False
    orpos=list()
    orfields=list()
    retval=False
    for charnum,char in enumerate(abnf):
        if char == '"':
            if doublequotecounter>0:
                doublequotecounter=0
            else:
                doublequotecounter+=1
        if char == "[" or char== "(":
            groupoptioncounter+=1
        if char == "]" or char ==")":
            groupoptioncounter-=0
        #If not within a group or option or within doubl qoutes -> strore
        #where the or-sign appeared
        if char == "/" and doublequotecounter==0 and groupoptioncounter==0:
            print (charnum)
            orpos.append(charnum)
    if len(orpos) > 0:
        for posnum,pos in enumerate(orpos):
            if posnum==0:
                orfields.append(abnf[0:pos])
            else:
                orfields.append(abnf[orpos[posnum-1]+1:pos])
        for field in orfields:
            if generalfunction(field,stringtoparse):
                retval=True
                break
            else:
                retval=False
    return retval

def __doublequote(abnf,stringtoparse):
    #Here must be a exception if there are no closing "
    fixedstring=regex.match('(?<capture>.*)\"',abnf[1:]).group("capture")
    if not fixedstring:
        raise raise NotMatchingABNFError("__doublequote",abnf)

    handled=True
    matching=regex.match(regex.escape(fixedstring),stringtoparse)
    restabnf=abnf[fixedstring.end()+2:]
    if matching:
        success=True
        reststring=stringtoparse[matching.end()+1:]
    else:
        success=False
        reststring=stringtoparse
    return success, reststring, restabnf

def __braket(abnf, stringtoparse):
    if not regex.match('\('),abnf):
        raise raise NotMatchingABNFError("__braket",abnf)
    #Actually there should be a exception if there is no endpos
    abnfendpos=regex.match('\)',abnf).end()
    success, reststring, restabnf = generalfunction(abnf[1:endpos],stringtoparse)
    restabnf=abnf[abnfendpos+1:]
    handled=True
    return success, reststring, restabnf

def __option(abnf, stringtoparse):
    if not regex.match('\['),abnf):
        raise raise NotMatchingABNFError("__option",abnf)
    #Here should be a exception if there is no endpos
    abnfendpos=regex.match('\]',abnf).end()
    success, reststring, restabnf = generalfunction(abnf[1:endpos],stringtoparse)
    restabnf=abnf[abnfendpos+1:]

def __repetition(abnf, stringtoparse,singledigit=False):

    rep=regex.match('(?<first>[0-9]*)\*(?<second>[0-9]*)|(?<singledigit>[0-9]*)',abnf)
    if not rep.group():
        raise raise NotMatchingABNFError("__repetition",abnf)
    if rep.group("singledigit"):
        rep=regex.match([0-9]*)
        min=rep.group()
        max=rep.group()
    else :
        rep=regex.match(repetition,abnf)
        min=rep.groupen("first")
        max=rep.group("second")
    abnf=abnf[rep.end()+1]
    if not min:
        min=0
    if not max:
        max=0
    repcounter=0
    while True:
        #Check whether we have reached the maximum amount of matches, but
        #just if max was defined -> else it could go on till nothing is found
        #anymore
        if repcounter == max and max:
            break
         success, stringtoparse, abnf = generalfunction(abnf,stringtoparse)
        if success:
             repcounter+=1
        else:
            break
    if repcounter > min:
        success=True
    else
        success=False
    return success, reststring, restabnf

def __keyword(abnf,stringtoparse):
    success=False
    reparts=regex.match('(?<bracet>\<)?(?<keyword>[a-zA-Z][a-zA-Z0-9\-])*(?<closingbracet>\>)?')
    if not reparts:
        raise raise NotMatchingABNFError("__keyword",abnf)
    if reparts.group("bracet"):
        if not reparts.group(closingbracet)
            pass
            #At this point there should be a exception
    keyword=reparts.group("keyword")
    try:
        match=regex.match(abnfprimitives[keyword],stringtoparse)
        if match:
            success=True
            restabnf=abnf[reparts.group().end()+1:]
            reststring=stringtoparse[match.group().end()+1]
    except KeyError:
        #Here the lookup into the higlevel abnf list needs to be implemented
        #After that generalfunction needs to be called with the content of the
        #high level keyword
        pass
    return success, reststring, restabnf

def generalfunction(abnf,stringtoparse):
    abnf=cleanup(abnf)
    #Check for or and if present let the sub-method handle it
    if not __check_or(abnf,stringtoparse):
        while abnf>0:
            for callnumber,function in enumerate,processfunctions:
                #Go through the list of abnf-functions
                #if raise NotMatchingABNFError is returned try next one
                try:
                    success, abnf, stringtoparse =function(abnf,stringtoparse)
                except NotMatchingABNFError:
                    continue
                finally:
                    if callnumber == len(processfunctions)-1:
                        #Here needs to be a exception -> everything has been
                        #checked but none of the methods where able to handle it
                        #means error in the abnf
                        #The break needs to be replaced
                        break

    return success, reststring, restabnf



#generalfunction('"blubber"',"bla")
#generalfunction('rulename / group / option / char-val / num-val / prose-val',"bla")
