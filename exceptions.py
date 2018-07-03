class NotMatchingABNFError(Exception):
    """Exception to be raised if the selected ABNF method does not match the
    provided ABNF string"""
    def __init__(self,abnf,abnfstring):
        """Initalization of the Exception class

        Attributes:
            abnf -> The name of the abnf function which failed
            abnfstring -> abnf which has been tried to be matched
        """
        self.message="ABNF method " + str(abnf) + " does not match abnf string \
        " + abnfstring

    def __str__(self):
        """Called when the reason phrase should be printed"""
        return self.message


class InvalidABNFError(Exception):
    """Exception to be raised if the provided ABNF is invalid.
    To be exact it should be raised if all the possible match-functions have
    been checked and none of them matched -> so the ABNF must be invalid
    (or surely the match-functions)
    """

    def __init__(self,abnf):
        """Initalization method.

        Attributes:
            abnf -> abnf which failed to be matched
        """
        self.message=abnf + " is considered invalid ABNF."

    def __str__(self):
        """Called when the reason phrase should be printed"""
        return self.message
