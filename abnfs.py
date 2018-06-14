class abnfs (object):
    #abnfdict -> dict containing dictionarie containing abnf
    #key of first dictionary is
    def __init__(self, abnfdict=None, nochanges=True):
        if abnfdict:
            self.abnfdict=abnfdict
        else:
            self.abnfdict=dict()
