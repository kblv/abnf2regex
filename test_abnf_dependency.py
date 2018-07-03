import regex


baseabnf=dict()

baseabnf.update({"DQUOTE":'\x22'})
baseabnf.update({"BIT":'0|1'})
baseabnf.update({"DIGIT":'[\x30-\x39]'})
baseabnf.update({"HEXDIG":'(?:['+baseabnf["DIGIT"] +'|[A-F])'})
baseabnf.update({"dec-val":'d(?:'+baseabnf["DIGIT"]+')+'+'(?:(?:\.'+baseabnf["DIGIT"]+'+)+|(?:-'+baseabnf["DIGIT"]+'+))*'})
baseabnf.update({"hex-val":'x(?:'+baseabnf["HEXDIG"]+')+'+'(?:(?:\.'+baseabnf["HEXDIG"]+'+)+|(?:-'+baseabnf["HEXDIG"]+'+))*'})
baseabnf.update({"bin-val":'b(?:'+baseabnf["BIT"]+')+'+'(?:(?:\.'+baseabnf["BIT"]+'+)+|(?:-'+baseabnf["BIT"]+'+))*'})
baseabnf.update({"prose-val":'<(?:[\x20-\x3D] | [\x3F-\x7E])*>'})
baseabnf.update({"num-val":'%(?:'+baseabnf["bin-val"]+'|'+baseabnf["hex-val"]+'|'+baseabnf["dec-val"]+')'})
baseabnf.update({"char-val":baseabnf["DQUOTE"]+'(?:\x20-\x21|\x23-\x7E)*'+baseabnf["DQUOTE"]})
baseabnf.update({"SP":"\x20"})
baseabnf.update({"HTAB":"\x09"})
baseabnf.update({"WSP":'(?:' + baseabnf["SP"] + '|' + baseabnf["HTAB"] + ')'})
baseabnf.update({"VCHAR":'[\x21-\x7E]'})
baseabnf.update({"CR":"\x0D"})
baseabnf.update({"LF":"\x0A"})
baseabnf.update({"CRLF":baseabnf["CR"] + baseabnf["LF"]})
baseabnf.update({"comment":'(?: ;' + '(?:' + baseabnf["WSP"] + '|' + baseabnf["VCHAR"] + ')*' + baseabnf['CRLF'] + ") "})
baseabnf.update({"c-nl":'(?:' + baseabnf["comment"] + '|' + baseabnf["CRLF"] + ")"})
baseabnf.update({"c-wsp":'?:' + baseabnf["WSP"] + '|' + '(:?' + baseabnf["c-nl"] + baseabnf["WSP"] + '))'})
baseabnf.update({"ALPHA":'[\x41-\x5A]|[\x61-\x7A]'})
baseabnf.update({"rulename":baseabnf["ALPHA"] + "(?: " + baseabnf["ALPHA"] + "|" + baseabnf["DIGIT"] + "-)*"})
baseabnf.update({"repeat":'(?:' + baseabnf["DIGIT"]+"+" + "|" + "(?:" + baseabnf["DIGIT"] + "*" + "\*" + baseabnf["DIGIT"] + ')'})



#Element without group - element goes to group
baseabnf.update({"element":'(?<"rulename">' + baseabnf["rulename"] + ')' + "|" + '(?<char_val>' + baseabnf["char-val"] + ")"+ "|" + '(?<num_val>' + baseabnf["num-val"] + ")" + "|" + '(?<prose_val>' + baseabnf["prose-val"] + ")"})
baseabnf.update({"repetition":baseabnf["repeat"] +"?" + baseabnf["element"]})

baseabnf.update({"concatenation":'(?:' + baseabnf["repetition"] + '(:?' + baseabnf["c-wsp"] + '+' + baseabnf["repetition"] + ')*)'})
#Wieso stehen die hier unten? die sind nicht abhängig, oder? -> doch, weil alternation concenation einbindet und das wiederum repetetion
baseabnf.update({"alternation":'(?:' + baseabnf["concatenation"] + "(?:" + baseabnf["c-wsp"] + "* |" + baseabnf["c-wsp"] + "*" + baseabnf["concatenation"] + "))"})
baseabnf.update({"option":'(?: \[' + baseabnf["c-wsp"]+"*"+baseabnf["alternation"] + baseabnf["c-wsp"]+"*\])"})
baseabnf.update({"group":'(?: \(' + baseabnf["c-wsp"]+"*"+baseabnf["alternation"] + baseabnf["c-wsp"]+"*\))"})
#


print ("elment", baseabnf["element"], "\n")
print ("group",baseabnf["group"], "\n")


#Element with group in it - but without group(element) in it
#Group with Element + group in it
baseabnf.update({"element":'(?<"rulename">' + baseabnf["rulename"] + ')' + "(?<group>" + baseabnf["group"] + ")" + "(?<option>" + baseabnf["option"] + ")" + "|" + '(?<char_val>' + baseabnf["char-val"] + ")"+ "|" + '(?<num_val>' + baseabnf["num-val"] + ")" + "|" + '(?<prose_val>' + baseabnf["prose-val"] + ")"})
baseabnf.update({"repetition":baseabnf["repeat"] +"?" + baseabnf["element"]})

baseabnf.update({"concatenation":'(?:' + baseabnf["repetition"] + '(:?' + baseabnf["c-wsp"] + '+' + baseabnf["repetition"] + ')*)'})
#Wieso stehen die hier unten? die sind nicht abhängig, oder? -> doch, weil alternation concenation einbindet und das wiederum repetetion
baseabnf.update({"alternation":'(?:' + baseabnf["concatenation"] + "(?:" + baseabnf["c-wsp"] + "* |" + baseabnf["c-wsp"] + "*" + baseabnf["concatenation"] + "))"})
baseabnf.update({"option":'(?: \[' + baseabnf["c-wsp"]+"*"+baseabnf["alternation"] + baseabnf["c-wsp"]+"*\])"})
baseabnf.update({"group":'(?: \(' + baseabnf["c-wsp"]+"*"+baseabnf["alternation"] + baseabnf["c-wsp"]+"*\))"})
#

print ("elment", baseabnf["element"], "\n")
print ("group",baseabnf["group"], "\n")


#Element with group in it - with group(element) in it
#Group with Element in it - Element containing Group  - but Element has no Group with Element in it
baseabnf.update({"element":'(?<"rulename">' + baseabnf["rulename"] + ')' + "(?<group>" + baseabnf["group"] + ")" + "(?<option>" + baseabnf["option"] + ")" + "|" + '(?<char_val>' + baseabnf["char-val"] + ")"+ "|" + '(?<num_val>' + baseabnf["num-val"] + ")" + "|" + '(?<prose_val>' + baseabnf["prose-val"] + ")"})
baseabnf.update({"repetition":baseabnf["repeat"] +"?" + baseabnf["element"]})

baseabnf.update({"concatenation":'(?:' + baseabnf["repetition"] + '(:?' + baseabnf["c-wsp"] + '+' + baseabnf["repetition"] + ')*)'})
#Wieso stehen die hier unten? die sind nicht abhängig, oder? -> doch, weil alternation concenation einbindet und das wiederum repetetion
baseabnf.update({"alternation":'(?:' + baseabnf["concatenation"] + "(?:" + baseabnf["c-wsp"] + "* |" + baseabnf["c-wsp"] + "*" + baseabnf["concatenation"] + "))"})
baseabnf.update({"option":'(?: \[' + baseabnf["c-wsp"]+"*"+baseabnf["alternation"] + baseabnf["c-wsp"]+"*\])"})
baseabnf.update({"group":'(?: \(' + baseabnf["c-wsp"]+"*"+baseabnf["alternation"] + baseabnf["c-wsp"]+"*\))"})
#

print ("elment", baseabnf["element"], "\n")
print ("group",baseabnf["group"], "\n")


#Group with Element in it - Element containing Group  - but Element has no Group with Element in it
baseabnf.update({"element":'(?<"rulename">' + baseabnf["rulename"] + ')' + "(?<group>" + baseabnf["group"] + ")" + "(?<option>" + baseabnf["option"] + ")" + "|" + '(?<char_val>' + baseabnf["char-val"] + ")"+ "|" + '(?<num_val>' + baseabnf["num-val"] + ")" + "|" + '(?<prose_val>' + baseabnf["prose-val"] + ")"})
baseabnf.update({"repetition":baseabnf["repeat"] +"?" + baseabnf["element"]})

baseabnf.update({"concatenation":'(?:' + baseabnf["repetition"] + '(:?' + baseabnf["c-wsp"] + '+' + baseabnf["repetition"] + ')*)'})
#Wieso stehen die hier unten? die sind nicht abhängig, oder? -> doch, weil alternation concenation einbindet und das wiederum repetetion
baseabnf.update({"alternation":'(?:' + baseabnf["concatenation"] + "(?:" + baseabnf["c-wsp"] + "* |" + baseabnf["c-wsp"] + "*" + baseabnf["concatenation"] + "))"})
baseabnf.update({"option":'(?: \[' + baseabnf["c-wsp"]+"*"+baseabnf["alternation"] + baseabnf["c-wsp"]+"*\])"})
baseabnf.update({"group":'(?: \(' + baseabnf["c-wsp"]+"*"+baseabnf["alternation"] + baseabnf["c-wsp"]+"*\))"})
#

print ("elment", baseabnf["element"], "\n")
print ("group",baseabnf["group"], "\n")
