# What it is
Library/Tool to convert ABNF elements (used in RFCs) into python regex library regular expressions

# Known issues/limitations
Terminal values are not fully supported - some RFC (3261 - SIP for example) are using unicode codes for which no characters are specified (yet).
Using ABNF including such terminal values will result in a exception.

The issue is being worked on!

# What it could do
Taking a complete (the list includes all element definitions which are part of other definitions - except the ones from RFC 5234 -> those are known to the library) list of ABNF, resolve them and translate them to python regex library regular expressions.

# How to use

* include abnfs.py
* instanciate a object of type abnfs
* at instanciation you could provide a list of abnf as argument
* or you provide the abnf as single entries (one rule) by calling the add_abnf method after instanciation multiple times and providing it as parameter

Please note: The abnf need to be provided completely -> in the form rulename=ruledefinition
Further note: The abnf needs to be provided as one-liner -> line breaks and so on - althoug permitted by the RFC are not supported -> see "Sanitize" section for help

After you have provided all necessary abnf:

* call get_regex providing the name of the abnf rule you want to get the regex for
* or call get_all_regex and you will get a dictionary (key=rulename, key=regex) containing all abnf regex


# Sanitize

* import abnfserializer
* instanciate a object of abnfserializer
* on instanziation you could provide these 2 named parameters
  * linelist - list of lines -> every line containing exactly one rule or one part of a rule
  * oneleline - list of lines -> every line/stream contains multiple rules/parts of rules - the parts and rules are separated by \r or \r\n
* after instanciation you could call add_line and append these 2 named parameters:
  * line (see linelist above - in this case it accepts just a single line per call)
  * oneline (see above, list expected as above)


After all lines have been passed:

* call getabnf()
* it returns the abnf as list (one rule per entry) as expected by abnfs 
  
