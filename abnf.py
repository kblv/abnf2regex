class abnf(object):
    """Represents 1 abnf

    Methodes:
    - __init__(abnfname:abnfdef) - Initializes the object
    - get_regex() - Returns the regular expression (regular expressions as \
    supported by regex library)

    Attributes:
    - abnfname - Name of the abnf
    - abnfdef - Definition of the abnf
    - regularex - RegularExpression of the object (if compiled yet)
    """

    def __init__(self,fullstring=None,abnfname=None,abnfdef=None,getabnfmethod=None):
        """Initializes the object

        fullstring - instead of giving the name and definition of the abnf \
        it could be provided as one string -> name = definition
        abnfname - string; The name of the abnf
        abnfdef - string; The abnf-definition
        getabnfmethod - reference to the method from which to get other abnf
            needed to get other abnf objects which might be referenced of
            the abnf definition of the current one
        """

        #Contains the basic abnf rules
        #Assume that there are mistakes in here - at least the charater ranges
        #are defined differently in the abnf definition (not as x10-x20
        #as x10-20) - howevere probably this does not matter as it affects
        #just the basic expressions which will not needed to be matched
        #
        #repetition might not work: as repetition needs element and is part
        #of the definition of element
        self.baseabnf=dict()
        self.baseabnf.update({"prose-val":'<(?:[\x20-\x3D] | [\x3F-\x7E])*>'})
        self.baseabnf.update({"DIGIT":'[\x30-\x39]'})
        self.baseabnf.update({"HEXDIG":'(?:['+self.baseabnf["DIGIT"] +'|[A-F])'})
        self.baseabnf.update({"hex-val":'x(?:'+self.baseabnf["HEXDIG"]+')+'+'(?:(?:\.'+self.baseabnf["HEXDIG"]+'+)+|(?:-'+self.baseabnf["HEXDIG"]+'+))*'})
        self.baseabnf.update({"dec-val":'d(?:'+self.baseabnf["DIGIT"]+')+'+'(?:(?:\.'+self.baseabnf["DIGIT"]+'+)+|(?:-'+self.baseabnf["DIGIT"]+'+))*'})
        self.baseabnf.update({"BIT":'0|1'})
        self.baseabnf.update({"bin-val":'b(?:'+self.baseabnf["BIT"]+')+'+'(?:(?:\.'+self.baseabnf["BIT"]+'+)+|(?:-'+self.baseabnf["BIT"]+'+))*'})
        self.baseabnf.update({"num-val":'%(?:'+self.baseabnf["bin-val"]+'|'+self.baseabnf["hex-val"]+'|'+self.baseabnf["dec-val"]+')'})
        self.baseabnf.update({"DQUOTE":'\x22'})
        self.baseabnf.update({"char-val":self.baseabnf["DQUOTE"]+'(?:\x20-\x21|\x23-\x7E)*'+self.baseabnf["DQUOTE"]})
        self.baseabnf.update({"SP":"\x20"})
        self.baseabnf.update({"HTAB":"\x09"})
        self.baseabnf.update({"WSP":'(?:' + self.baseabnf["SP"] + '|' + self.baseabnf["HTAB"] + ')'})
        self.baseabnf.update({"repeat":'(?:' + self.baseabnf["DIGIT"]+"+" + "|" + "(?:" + self.baseabnf["DIGIT"] + "*" + "\*" + self.baseabnf["DIGIT"] + ')'})
        self.baseabnf.update({"ALPHA":'[\x41-\x5A]|[\x61-\x7A]'})
        self.baseabnf.update({"rulename":'(?: ' + self.baseabnf["ALPHA"] + '(:?' + self.baseabnf["ALPHA"] + '|' + self.baseabnf["DIGIT"] + "| - ))"})
        self.baseabnf.update({"CR":"\x0D"})
        self.baseabnf.update({"LF":"\x0A"})
        self.baseabnf.update({"CRLF":self.abnf["CR"] + self.abnf["LF"]})
        self.baseabnf.update({"VCHAR":'[\x21-\x7E]'})
        self.baseabnf.update({"comment":'(?: ;' + '(?:' + self.baseabnf["WS"] + '|' + self.baseabnf["VCHAR"] + ')*' + self.baseabnf['CRLF'] + ") "})
        self.baseabnf.update({"c-nl":'(?:' + self.baseabnf["comment"] + '|' + self.baseabnf["CRLF"] + ")"})
        self.baseabnf.update({"c-wsp":'?:' + self.baseabnf["WSP"] + '|' + '(:?' + self.abnf["c-nl"] + self.baseabnf["WSP"] + '))'})
        self.baseabnf.update({"concatenation":'(?:' + repetition + '(:?' + self.baseabnf["c-wsp"] + '+' + self.baseabnf["repetition"] + ')*)'})
        self.baseabnf.update({"alternation":'(?:' + self.baseabnf["concatenation"] + "(?:" + self.baseabnf["c-wsp"] + "* |" + self.baseabnf["c-wsp"] + "*" + self.baseabnf["concatenation"] + "))"})
        self.baseabnf.update({"group":'(?: \(' + self.baseabnf["c-wsp"]+"*"+self.baseabnf["alternation"] + self.baseabnf["c-wsp"]+"*\))"})
        self.baseabnf.update({"option":'(?: \[' + self.baseabnf["c-wsp"]+"*"+self.baseabnf["alternation"] + self.baseabnf["c-wsp"]+"*\])"})
        self.baseabnf.update({"element":self.baseabnf["rulename"] + "|" +  self.baseabnf["group"] + "|" + self.baseabnf["option"] + "|" + sef.baseabnf["char-val"] + "|" + self.baseabnf["num-val"] + "|" + self.baseabnf["prose-val"]})
        self.baseabnf.update({"repetition":self.baseabnf["repeat"] +"?" + self.baseabnf["element"]})
        self.baseabnf.update({"elements":self.baseabnf["alternation"]+ "?" + self.baseabnf["c-wsp"]+"*"})
        self.baseabnf.update({"defined-as":self.baseabnf["c-wsp"] + "* (?: = | =/)" + self.baseabnf["c-wsp"]})
        self.baseabnf.update({"rulename":self.baseabnf["ALPHA"] + "(?: " + self.baseabnf["ALPHA"] + "|" + self.baseabnf["DIGIT"] + "-)*"})
        self.baseabnf.update({"rule":self.baseabnf["rulename"] + self.baseabnf["defined-as"] + self.baseabnf["elements"] + self.baseabnf["c-nl"]})
        self.baseabnf.update({"rulelist":"(?:" + self.baseabnf["rule"] + "| (?:" + self.baseabnf["c-wsp"] + "*" + self.baseabnf["c-nl"] + "))+"})








        if (not fullstring and (not abnfname or not abnfdef)) or not getabnfmethod:
            raise TypeError("Missing argument. fullstring or abnfname or/and abnfdef and/or \
            getabnfmethod has not been provided")
        if fullstring:
            #self.abnfname=
            #self.abnfdef=
            pass
        else:
            self.abnfname=abnfname
            self.abnfdef=abnfdef
        self.__regex=None

    def get_regex(self,orceregen=False):
        """Returns the regex representation of the abnf.

        - forceregen - If true the regular expression is being recompiled
            -> makes sense if parts of the abnf have been changed since the
                last time the abnf has been compiled (by calling get_regex)
            -> if false it won't be just compiled in case get_regex hasn't be
                called for this abnf earlier -> else the earlier compiled one is
                returned
        """
