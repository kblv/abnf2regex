class abnfs (object):
    """Gets a dictionary of abnf dictionary and returns the regular expression
    (regular expression supported by the regex module) for abnf in the abnf

    __init__(abnfdict,nochanges)
    addabnf (abnfdict) - adds a abnf to the dict of abnfs
    """

    def __init__(self, abnfdict=None, nochanges=True):
    """Initializes the class

    abnd 
        if abnfdict:
            self.abnfdict=abnfdict
        else:
            self.abnfdict=dict()
        self.nochanges=nochanges
