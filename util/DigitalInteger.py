from dragonfly import Repetition, Choice

DIGITS = {
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}


class DigitalInteger(Repetition):
    '''An integer element spelled digit by digit (eg, enter 50 by saying
       'five zero'. Useful in places where Dragon would complain of the
       grammar's complexity if regular integers were used. min and max are
       number of digits, not value of the number.'''
    child = Choice('digit', DIGITS)

    def __init__(self, name, min, max, *args, **kw):
        Repetition.__init__(
            self,
            self.child,
            min,
            max,
            name=name,
            *args,
            **kw
            )

    def value(self, node):
        return int(''.join(Repetition.value(self, node)))
