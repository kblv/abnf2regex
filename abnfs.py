from abnf import abnf
from exceptions import *

class abnfs (object):
    """List of abnfs (abnf objects)- used by abnf class to lookup sub-abnfs
        /key words which are part of there abnf.

        Methodes:
            init -> Initializes the class
            add_abnf -> Add a abnf string (will result internally in a \
                appended abnf object)
            get_regex -> get the regex for a certain abnf with a name
            get_all_regex -> get all the abnf names and there regular expression \
                representation stored in this abnfs object
    """

    def __init__(self, abnflist=None):
        """Initializes the class

            Arguments:
                abnflist -> Optional list of abnf to be converted
        """
        self.__abnfobjectdict=dict()
        if abnflist:
            for entry in abnflist:
                self.add_abnf(entry)

    def get_regex(self,abnfname):
        """Returns the regular Expression for a certain abnfname

            Arguments:
                abnfname -> The name of the abnf
            Return values:
                expression -> The regular expression or None if it does not exists
            Exception:
                MissingABNFError -> The abnf which should be retrieved consists \
                    (probably besides others) of at least one sub-anf for which \
                    there is no definition in the abnfs object
        """

        abnfobject=self.__abnfobjectdict.get(abnfname)
        if not abnfobject:
            raise MissingABNFError(abnfname)
        return abnfobject.get_regex()

    def get_all_regex(self):
        """Returns the regular Expressions for all abnf of the object

            Return values:
                expression -> dictionary; name of abnf as key, regex as value \
                    or None if there are no ABNF in this object
            Exception:
                MissingABNFError -> The abnf which should be retrieved consists \
                    (probably besides others) of at least one sub-anf for which \
                    there is no definition in the abnfs object
        """
        resultdict=dict()
        if not len(self.__abnfobjectdict):
            resultdict=None
        else:
            for name in self.__abnfobjectdict:
                resultdict.update({name:self.get_regex(name)})
        return resultdict

    def add_abnf (self,abnfstring):
        """Adds a abnf to the abnfs object

            Arguments:
                abnfstring -> The abnf (including the rule name) \
                    It is expected that it is a one-line ABNF. \
                    The RFC allows that the ABNF is spread across multiple lines \
                    which even could have comments at there end per line. \
                    If that is the case that needs to be cleaned up before \
                    passing it
        """
        abnfobject=abnf(abnfstring,self.get_regex)
        self.__abnfobjectdict.update({abnfobject.get_name():abnfobject})
