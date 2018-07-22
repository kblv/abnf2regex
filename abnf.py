from exceptions import *
import binascii
import regex

class abnf(object):
    """Represents 1 abnf

    Methodes:
    - __init__(abnfname:abnfdef) - Initializes the object
    - get_regex() - Returns the regular expression (regular expressions as \
    supported by regex library)
    - get_name() - Returns the name of the abnf (the name will be in lower case)

    Attributes:
    - abnf - Definition of the abnf
    """

    def __init__(self,abnf,getabnfmethod):
        """Initializes the object

        abnf - name and definition of the abnf
        abnfdef - string; The abnf-definition
        getabnfmethod - reference to the method from which to get other abnf
            needed to get other abnf objects which might be referenced of
            the abnf definition of the current one
        """
        self.__abnf=abnf
        self.__regex=None
        self.__name=None
        self.__getababnfmethod=getabnfmethod

        self.__abnfprimitives=dict()
        self.__abnfprimitives.update({"vchar":'[\x21-\x7E]'})
        self.__abnfprimitives.update({"cr":"\x0D"})
        self.__abnfprimitives.update({"lf":"\x0A"})
        self.__abnfprimitives.update({"alpha":'([\x41-\x5A]|[\x61-\x7A])'})
        self.__abnfprimitives.update({"sp":"\x20"})
        self.__abnfprimitives.update({"htab":"\x09"})
        self.__abnfprimitives.update({"dquote":'\x22'})
        self.__abnfprimitives.update({"prose-val":'(?:[\x20-\x3D] | [\x3F-\x7E])*'})
        self.__abnfprimitives.update({"digit":'[\x30-\x39]'})

        #Order matters, at least for valuerange and terminalvalue ->
        #terminalvalue would match parts of valuerange
        self.__processfunctions=list()
        self.__processfunctions.append(self.__rulename)
        self.__processfunctions.append(self.__comment)
        self.__processfunctions.append(self.__optionalsequence)
        self.__processfunctions.append(self.__variablerepetition)
        self.__processfunctions.append(self.__sequencegroup)
        self.__processfunctions.append(self.__valuerange)
        self.__processfunctions.append(self.__terminalvalue)
        self.__processfunctions.append(self.__alternative)
        self.__processfunctions.append(self.__dquote)

    def __seperatename(self,rule):
        """Internal method separating the rulename from the rest of the abnf

            Parameters:
                rule -> The complete abnf rule
            Return value:
                name -> The name of the abnf rule
                abnf -> The actual abnf (without the rulename)
        """
        name,abnf=regex.split("=",rule,maxsplit=1)
        name=name.strip()
        name=regex.sub('/','',name)
        name=name.lower()
        return name,abnf

    def __abnfupdate(self,abnf):
        """Internal method called whenever the regex needs to be build from the
        abnf

        Parameter:
            abnf -> The raw abnf (including the name)
        """
        self.__name,abnf=self.__seperatename(self.__abnf)
        abnf,self.__regex=self.__generalfunction(abnf)

    def get_regex(self,forceregen=False):
        """Returns the regex representation of the abnf.

        Parameter:
            - forceregen - If true the regular expression is being recompiled
                -> makes sense if parts of the abnf have been changed since the
                    last time the abnf has been compiled (by calling get_regex)
                -> if false it won't be just compiled in case get_regex hasn't be
                    called for this abnf earlier -> else the earlier compiled one is
                    returned
        Return values:
            regex -> The regular expression of the abnf
        """

        if not self.__regex or forceregen:
            self.__abnfupdate(self.__abnf)
        return self.__regex

    def get_name(self):
        """Returns the name of the abnf represented by this abnf object

            Return:
                name -> the name of the abnf in lower case
        """
        if not self.__name:
            self.__name, notofinterest=self.__seperatename(self.__abnf)
        return self.__name

    def __cleanup(self,abnf):
        """Internal method cleaning up not needed characters.

            Currently the leading white spaces are removed

            Parameter:
                abnf -> the abnf to clean (string)
            Return:
                abnf -> The cleaned up abnf as string
        """
        abnf=regex.sub("^\s*","",abnf)
        return abnf

    def __convertterminalvalue(self,prefix,value,**kwargs):
        """Internal method converts "terminal values" to characters

            Parameters:
                prefix -> The prefix (like x for hex, b for binary, d for decimal)
                value -> The actual number (without the prefix and the %)
            Returns:
                char -> The character representation of the terminalvalue \
                    as string (escaped if needed)
        """
        if prefix == "b":
            char=b2a_qp(binvalue)
        if prefix == 'd':
            char=chr(charater)
        if prefix == 'x':
            print ("Value:", value)
            char=binascii.unhexlify(value).decode()
        return regex.escape(char)

    def __rulename(self,abnf):
        """Internal method translating rulenames into the content of the rules
            by looking them up.

            Parameters:
                abnf -> The abnf beginning with the rulename
            Return value:
                abnf -> The remaining abnf to be parsed (the incoming abnf \
                    - the rulename)
                expression -> the regular expression resulted from resolving \
                    the rulename
        """
        match=regex.match("<?(?<rulename>[A-Za-z][A-Za-z0-9\-]+)>?",abnf)
        if not match:
            raise NotMatchingABNFError("__rulename",abnf)
        print ("__rulename")
        rulename=match.group("rulename").lower()
        expression=self.__abnfprimitives.get(rulename)
        if not expression:
            #Here must be the lookup into the global tabel
            expression=self.__getababnfmethod(rulename)
        return abnf[match.end():],expression

    def __comment(self,abnf,**kwargs):
        """Internal method removing comments from the abnf.

            Parameters:
                abnf -> The abnf beginning with the comment (;)
            Return value:
                abnf -> Empty string as there is no abnf remaining to be parsed \
                after a commend (comments are at the end of abnf)
                expression -> empty string as there is no regex needed for comment
        """
        match=regex.match(";.*",abnf)
        if not match:
            raise NotMatchingABNFError("__comment",abnf)
        print ("__comment")
        #Returning abnf empty and expression empty - as the comment is the
        #end of the abnf rule and it is not part of the rule
        return "",""

    def __optionalsequence(self,abnf,**kwargs):
        """Internal method handling optionalsequence from the RFC.

            Sequences enclosed in [].

            Parameters:
                abnf -> The abnf beginning with the optionalsequence ([)
            Return value:
                abnf -> The remaining abnf to be parsed (the incoming abnf \
                    - the optionalsequence)
                expression -> the regular expression for the optionalsequence
        """
        match=regex.match("\[(?<content>.+)\]",abnf)
        if not match:
            raise NotMatchingABNFError("__optionalsequence",abnf)
        print ("__optionalsequence")
        notofinterest,expression=self.__generalfunction(match.group("content"),**kwargs)
        return abnf[match.end():],"("+expression+")?"

    def __variablerepetition(self,abnf,**kwargs):
        """Internal method handling variablerepetition from the RFC.

            Element prefixed with a number, or *, or number*number, or \
            *number, number*

            Parameters:
                abnf -> The abnf beginning with the variablerepetition
            Return value:
                abnf -> The remaining abnf to be parsed (the incoming abnf \
                    - the variablerepetition)
                expression -> the regular expression for the variablerepetition \
                    including the element to be repeatet
        """
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
        print ("__variablerepetition before self.__generalfunction",abnf[match.end():])
        abnf,expression=self.__generalfunction(abnf[match.end():],chkhowmany=1,**kwargs)
        expression="("+expression+"){"+str(min)+","+str(max)+"}"
        return abnf, expression

    def __sequencegroup(self,abnf,**kwargs):
        """Internal method handling sequencegroups from the RFC.

            Actual groups - elements grouped in ()

            Parameters:
                abnf -> The abnf beginning with the sequencegroup - with a (
            Return value:
                abnf -> The remaining abnf to be parsed (the incoming abnf \
                    - the sequencegroup)
                expression -> the regular expression for the sequencegroup \
                    including the elements within the sequencegroup
        """
        match=regex.match("\((?<content>.+)\)",abnf)
        if not match:
            raise NotMatchingABNFError("__sequencegroup",abnf)
        print ("__sequencegroup")
        notofinterest, expression=self.__generalfunction(match.group("content"),**kwargs)
        expression="("+expression+")"
        return abnf[match.end():], expression

    #kwargs has no function in this case
    def _terminalvalue_check_completestring(self,abnf,requiretype=None,**kwargs):
        """Sub-Method of __terminalvalue - Checks the abnf for a terminalvalue \

         Terminalvalue in the sense of this method is a string starting with
         b, d or x followed by one or more digits

         Parameter:
            - abnf -> The abnf to be parsed
            - requiretype -> Optional the expected type. If the terminalvalue \
                is not of the expected type return value "terminalvalue" will \
                be None -> as there was no terminalvalue found
        Return-value:
            - restabnf -> The rest of the abnf - everything except the \
                terminalvalue / everything which has been passed to the method \
                if no terminalvalue has been found
            - terminalvalue -> list containing at first position the type \
                (b,d,x) and at second position the terminalvalue (the number). \
                Is of type None in case there is no terminalvalue at the \
                beginning of the string
        """
        match=regex.match('%(?<type>[bdx])(?<numbers>[0-9A-Z]+)',abnf)
        if match and ((requiretype and match.group("type")==requiretype) or  \
            not requiretype):
            terminalvalue=list([match.group("type"),match.group("numbers")])
            restabnf=abnf[match.end():]
        else:
            terminalvalue=None
            restabnf=abnf
        return restabnf,terminalvalue

    #kwargs has no function in this case
    def _terminalvalue_check_dot(self,abnf,**kwargs):
        """Sub-Method of __terminalvalue - Checks for extended termvalue (.xy) \

         Extended terminalvalue in the sense of the method is when a \
         terminalvalue has another one appended by "." -> like %45.46

         Parameter:
            - abnf -> The abnf to be parsed
        Return-value:
            - restabnf -> The rest of the abnf - everything except the \
                terminalvalue / everything which has been passed to the method \
                if no terminalvalue has been found
            - terminalvalue -> containing the terminalvalue (just the hex \
                digits) or None if nothing has been found
        """
        match=regex.match('\.[0-9A-Z]+',restabnf)
        if match:
            terminalvalue=match.group()
            restabnf=abnf[match.end():]
        else:
            terminalvalue=None
            restabnf=abnf
        return restabnf, terminalvalue

    def _terminalvalue_check_rule(self,abnf,**kwargs):
        """Sub-Method of __terminalvalue - Checks for termvalue in rule \

         Some RFC (for exapmle RFC 3261) putting parts of the terminal value
         into own rule names. This method "resolves" the rulenames and checks
         for terminalvalues.
         The method returns a terminalvalue just in case that the keyword
         definition is a terminalvalue and in addition it is a complete \
         terminalvalue (starting with %) starting with the prefix defined in \
         parameter "requiredprefix" or if it is a partial or a extended \
         terminalvalue (in the last both cases there is no prefix)

         Parameter:
            - abnf -> The abnf to be parsed
            - named parameter (kwargs) "requiredprefix" -> The prefix (b,d or x) the"tesla model 3" wltp
                terminalvalue needs to have.
        Return-value:
            - restabnf -> The rest of the abnf - everything except the \
                terminalvalue / everything which has been passed to the method \
                if no terminalvalue has been found
            - terminalvalue -> containing the terminalvalue (just the hex \
                digits) or None if nothing has been found
        """
        checkmethods=list()
        checkmethods.append(self._terminalvalue_check_dot)
        checkmethods.append(self._terminalvalue_check_completestring)
        if not kwargs["requiredprefix"]:
            raise ValueError('Parameter \"requiredprefix\" required when \
                calling \"_terminalvalue_check_rule\"')
        restabnf,expression=self.__rulename(self,abnf,terminalvaluenoparse=True,**kwargs)
        for method in checkmethods:
            restabnf,terminalvalue=method(expression,**kwargs)
            if terminalvalue:
                break
        #In case it was not resolveable into a terminal value
        #or it has a different prefix than required
        if not terminalvalue or (type(terminalvalue)==dict and \
            terminalvalue["type"] != kwargs["requiredprefix"]):
            return abnf, None
        if type(terminalvalue)==dict:
            terminalvalue=terminalvalue["numbers"]
        return restabnf, terminalvalue

    def __terminalvalue(self,abnf,**kwargs):
        """Internal method handling terminalvalues from the RFC.

            Hex value, bin values, decimal values which needs to be chars

            Parameters:
                abnf -> The abnf beginning with the terminalvalue - with a %
            Return value:
                abnf -> The remaining abnf to be parsed (the incoming abnf \
                    - the terminalvalue)
                expression -> the character represented by the terminalvalue
        """
        terminalvalue=str()
        type=str()
        checkmethods=list()
        checkmethods.append(self._terminalvalue_check_rule)
        checkmethods.append(self._terminalvalue_check_dot)
        checkmethods.append(self._terminalvalue_check_completestring)
        restabnf,value=self._terminalvalue_check_completestring(abnf,**kwargs)
        if not value:
            raise NotMatchingABNFError("__terminalvalue",abnf)
        type=value[0]
        terminalvalue=value[1]
        #This is for detecting when we have checked all methods and none
        #matched -> we have reached the end of the terminalvalue
        print (restabnf)
        print (value)
        try:
            while len(restabnf) > 0:
                for looprun,checkmethod in enumerate,checkmethods:
                    restabnf,value=checkmethod(restabnf,requiredprefix,**kwargs)
                    if value:
                        if type(value) == dict:
                            value=value["numbers"]
                        terminalvalue+=value
                        break
                    if looprun == len(checkmethods)-1:
                        raise NotMatchingABNFError("__terminalvalue-submethods",restabnf)
        except NotMatchingABNFError:
            pass
        if kwargs.get(terminalvaluenoparse):
            terminalvaluecharacters=terminalvalue
        else:
            terminalvaluecharacters=self.__convertterminalvalue(type,terminalvalue,**kwargs)
        return restabnf, terminalvaluecharacters

    def __valuerange(self,abnf,**kwargs):
        """Internal method handling valueranges from the RFC.

            Ranges of terminalvalues

            Parameters:
                abnf -> The abnf beginning with the valuerange (%)
            Return value:
                abnf -> The remaining abnf to be parsed (the incoming abnf \
                    - the valuerange)
                expression -> the regular expression for the valuerange
        """
        match=regex.match('%(?<type>[bdx])(?<first>[0-9A-Z]+)\-(?<second>[0-9A-Z]+)',abnf)
        if not match:
            raise NotMatchingABNFError("__valuerange",abnf)
        print ("__valuerange")
        firstchar=self.__convertterminalvalue(match.group("type"),match.group("first"),**kwargs)
        secondchar=self.__convertterminalvalue(match.group("type"),match.group("second"),**kwargs)
        return abnf[match.end():], '['+firstchar+'-'+secondchar+']'

    def __alternative(self,abnf,**kwargs):
        match=regex.match("\=?/",abnf)
        if not match:
            raise NotMatchingABNFError("__alternative",abnf)
        print ("__alternative")
        return abnf[match.end():],"|"

    def __dquote(self,abnf,**kwargs):
        """Internal method handling dquotes/double quotes from the RFC.

            raw strings enclosed in ""

            Parameters:
                abnf -> The abnf beginning with the dquote - with a "
            Return value:
                abnf -> The remaining abnf to be parsed (the incoming abnf \
                    - the dquote)
                expression -> the regular expression for the dquote including \
                    the raw string
        """
        print ("dquote abnf:",abnf)
        match=regex.match('\"(?<content>.+?)\"',abnf)
        if not match:
            raise NotMatchingABNFError("__dquote",abnf)
        print ("__dquote")
        print ("double quote", match.group("content"))
        print (match.end())
        return abnf[match.end():],regex.escape(match.group("content"))

    def __generalfunction(self,abnf,chkhowmany=0,**kwargs):
        """Internal main processing function - calls all the abnf processing \
        functions

            Parameter:
                abnf -> The abnf to be processed
                chkhowmany -> How many elements within the abnf should be \
                    processed. By default (0) the whole abnf. Integer.
            Return:
                abnf -> Remaining abnf to be parsed
                expression -> The regular expression which is the result of \
                    parsing the abnf
        """

        checkedelements=0
        expression=str()
        origabnf=abnf
        abnf=self.__cleanup(abnf)
        while len(abnf)>0:
            print (abnf)
            print ("Lange ABNF",len(abnf))
            for callnumber,function in enumerate(self.__processfunctions):
                try:
                    print ("abnf vor funktionsaufruf:",abnf)
                    abnf, retexpression=function(abnf,**kwargs)
                    expression+=retexpression
                    break
                except NotMatchingABNFError:
                    print("AbnfErrror in generalfunction")
                    print("callnumber, len(processfunction)",callnumber,len(self.__processfunctions)-1)
                    if callnumber == len(self.__processfunctions)-1:
                        raise InvalidABNFError(origabnf)
                    continue
            checkedelements+=1
            print ("Expression",expression)
            if checkedelements==chkhowmany and chkhowmany:
                break
            abnf=self.__cleanup(abnf)
        return abnf,expression
