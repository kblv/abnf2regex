import regex

class abnfserializer (object):
    """Serializes abnf rules which are stretching over multiple lines und \
        returns them as one line (one per abnf)-> so they could be processed \
        by abnf/abnfs- \objects.

        Example 1:
            You are reading a file line by line which contains abnf rules. \
            Within this file lines may appear this way (there are likely even \
            multiple of such lines):
            via-params        =  via-ttl / via-maddr
                     / via-received / via-branch
                     / via-extension
            Supported  =  ( "Supported" / "k" ) HCOLON
                    [option-tag *(COMMA option-tag)]
            In this case the first abnf rule stretches across 3 lines.
            The abnf/abnfs class expects one line = exactly one abnf rule.
            So the above needs to be converted to one single line - this is
            what the class does, it takes it line by line and creates one
            single line for each rule -> so in the example above the output
            would be:
            via-params        =  via-ttl / via-maddr / via-received / via-branch \
            / via-extension
            Supported  =  ( "Supported" / "k" ) HCOLON [option-tag *(COMMA \
            option-tag)]
            As 2 seperate lines.

        Example 2:
            You are reading one file into one string/or as blocks (not careing)
            about line breaks.
            So you have something like:
            via-params        =  via-ttl / via-maddr \r\n         / \
            via-received / via-branch         / via-extension \r\n  Supported  \
            =  ( "Supported" / "k" ) HCOLON        [option-tag *(COMMA \
            option-tag)]
            as one continues string.
            In the above case you have line breaks within the string, because \
            there are 2 rules and both are even scattered over multiple lines.
            abnf and abnfs will require one abnf rule at one line.
            This class takes the one-liner and converts it into one line per \
            abnf -> removing all the new lines and and intends.

        In every case those rules apply:
            - a new rule (or the part where the rule begins if split across \
                lines) starts at "the beginning" of the line (in case of \
                everything being one string, there should be no space after \n \
                or \r\n before the rule follows)-> so there are \
                no spaces or any other blanks at the beginning
            - follow up parts of the same rule need to be intended -> so there \
                needs to be at least be one space in front of the "beginning of
                the line" (in case of everything is one string, there should be \
                a space after \n or \r\n of the previouse entry)
            - parts of the same rule need to follow up immediately after the \
                beginning of the rule. In case of everything is one string \
                this means that after a rule starts within the string, all \
                addtional parts of the same rule need to follow directly \
                after the \n or \r\n of the beginning of the rule. In case of
                multiple lines, after the line that starts the abnf, the follow \
                up lines need to be the additional parts.

        Some names used in parameters of the methods:
            - line -> Single line; One abnf/part of a abnf in one line/string \
                Example 1 is such a case
            - oneline -> Everything is one line; Multiple abnf or parts of it \
                in one line/string. Example 2 is such a case.

        Methods:
            __init__ -> Initiating the object
    """

    def __init__(self,linelist=None,onelinelist=None):
        """Initiating the object

            Parameters:
                linelist -> Optional list of lines containing abnf/parts \
                    -> one entry could be just part of one abnf (there could ) \
                    not be parts of multiple abnf at one entry. Abnf parts \
                    splitted across lines need to be in the lines/entries \
                    follow to the begin of the abnf. Also entries being part of \
                    abnf need to intended (start with at least one space) -> \
                    except the first part. \
                onelinelist -> Optional list of lines where one line contains \
                    multiple abnf\parts of multiple abnf  - single abnf or \
                    parts of abnf need to \
                    to be terminated by \n or \r\n; Parts of abnf must \
                    follow directly after the begin of the abnf and start \
                    with at least one space (need to be intended).
        """
        self._changed=False
        self._linelist=list()
        self._onelinelist=list()
        self._abnflines=list()

        if linelist:
            self._linelist.extend(linelist)
        elif onelinelist:
            self._onelinelist.append(oneline)

    def add_line(self,line=None,oneline=None):
        """Add lines to the list

            Parameters:
                line -> Single line containing a part of a abnf/ a abnf - \
                    but not multiple parts or multiple abnf. \
                    Abnf parts splitted across lines need to be passed directly \
                    after the beginning of the passed abnf rule. \
                    Also entries being part of abnf need to intended \
                    (start with at least one space) -> except the first part.  \
                oneline -> Optional one list containing one or multiple string \
                    containing multiple abnf\parts \
                    of multiple abnf - single abnf or parts of abnf need to \
                    to be terminated by \n or \r\n; Parts of abnf must \
                    follow directly after the begin of the abnf and start \
                    with at least one space (need to be intended).
        """
        if line:
            self._linelist.append(line)
        elif oneline:
            self._onelinelist.extend(oneline)
        else:
            raise ValueError("Either line or oneline needs to be given.")

    def _oneline_to_seperatelines(self,onelinelist=None):
        """Converts online-abnf (mulitple abnf or multiple parts of one abnf \
            at the same line) to one abnf per line

            Parameter:
                onelinelist -> optional list with one-line-abnf entries; when \
                    not provided the global _onelinelist of the object will be \
                    used

            Return values:
                seperate_abnf_list -> list where one abnf or one part of a \
                    abnf is represented each by one line
        """

        seperatelines=list()
        if onelinelist:
            onelinetoprocess=onelinelist
        else:
            onelinetoprocess=self._onelinelist
        for line in onelinetoprocess:
            for entry in regex.split('\r\n|\n',line):
                seperatelines.append(entry)
        return seperatelines

    def _processlines(self):
        """Processes the scattered abnf across multiple lines or the lines
        containing multiple abnf/abnf parts in one line stored in the object \
        and stores a list where one entry is one abnf -> so that it could be \
        provided to abnf or abnfs class for processing"""

        self._linelist.extend(self._oneline_to_seperatelines())
        for line in self._linelist:
            line=regex.sub('\r\n|\n','',line)
            line=regex.sub(';.*','',line)
            if regex.match('\s',line):
                self._abnflines[len(self._abnflines)-1]+=line
            else:
                self._abnflines.append(line)

    def getabnf(self):
        """Returns the abnf stored in the object one line = one abnf

            Return values:
                abnflist -> list of the abnf of this object - one entry = \
                    abnf
        """
        self._processlines()
        return self._abnflines
