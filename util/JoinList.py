from dragonfly import Modifier

class JoinList(Modifier):
    """
        Converts the list output of another element to a string by joining values together

        Constructor arguments:
            - *element* (*Element*) -- The element to be recognised, e.g.
              :class:`Dictation` or :class:`Repetition`, with appropriate
              arguments passed.
            - *join_with* (*string*) -- The string to use as joiner
              value of this element when it is recognised.

        Examples:

        .. code:: python

            # Recognises an integer, returns the integer plus one
            Modifier(IntegerRef("plus1", 1, 20), lambda n: n+1)

            # Recognises a series of integers, returns them separated by
            # commas as a string
            int_rep = Repetition(IntegerRef("", 0, 10), min=1, max=5,
                                 name="num_seq")
            Modifier(int_rep, lambda r: ", ".join(map(str, r)))

    """
    def __init__(self, element, join_with=' '):
        Modifier.__init__(self, element=element, modifier=lambda r: join_with.join(map(str, r)))
