"""
Implementation of Prefix Hash Tree.
"""


class PrefixHashTree:
    """
    Implementation of Prefix Hash Tree.

    Contains a dictionary where the keys are the prefixes that are typed by the user and teh value is the set of
    suggestions that start with the prefix passed in.
    https://prefixy.github.io
    """
    def __init__(self):
        """
        The initializer.
        """
        # The dictionary that stores all the data
        self.map = dict()

    def insert(self, to_insert):
        """
        Break to_insert down into substrings where they begin at the start of to_insert and go from len = 1 to len =
        len(to_insert - 1).

        The substrings will act as keys to and the suggestion will be added to value which is a set.
        Returns nothing.

        :param to_insert:
        :return:
        """
        # To generate the substring from to_insert, beginning from the start with len = 1 to len = len(to_insert - 1) to
        # create the keys that will act as the keys.
        for l in range(1, len(to_insert)):
            substr = to_insert[0: l]

            if substr in self.map:
                self.map[substr].add(to_insert)
            else:
                s = set()
                s.add(to_insert)
                self.map[substr] = s

    def query(self, prefix):
        """
        Check if the prefix is a key in the stored map, if yes, return the set, it is the suggestions, otherwise return
        an empty set because there are no suggestion for the prefix.

        :param prefix:
        :return:
        """
        return self.map.get(prefix, set())
