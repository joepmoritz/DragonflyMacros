# This file is part of Aenea
#
# Aenea is free software: you can redistribute it and/or modify it under
# the terms of version 3 of the GNU Lesser General Public License as
# published by the Free Software Foundation.
#
# Aenea is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with Aenea.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (2014) Alex Roper
# Alex Roper <alex@aroper.net>

'''Contains generic utility data and functions useful when writing grammars.'''

try:
    import dragonfly
except ImportError:
    import dragonfly_mock as dragonfly

import configuration

LOWERCASE_LETTERS = configuration.make_grammar_commands('misc', {
    'arch': 'a',
    'broth': 'b',
    'chimp': 'c',
    'dell': 'd',
    'etch': 'e',
    'fomp': 'f',
    'golf': 'g',
    '(hark | harp)': 'h',
    'ico': 'i',
    'jinx': 'j',
    'kilo': 'k',
    'lamb': 'l',
    'mike': 'm',
    'nerb': 'n',
    'ork': 'o',
    'pooch': 'p',
    'quiche': 'q',
    'rosh': 'r',
    'souk': 's',
    'teek': 't',
    'unks': 'u',
    'verge': 'v',
    'womp': 'w',
    'trex': 'x',
    'yang': 'y',
    'zooch': 'z'
    }, 'letters.lower')


UPPERCASE_LETTERS = dict(('cap ' + key, value.upper()) for (key, value) in LOWERCASE_LETTERS.iteritems())

DIGITS = configuration.make_grammar_commands('misc', {
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
    }, 'digits')

SYMBOLS = {
    "ampersand": "ampersand",
    "(slash | divided [by])": "slash",
    "at sign": "at",
    "backslash": "backslash",
    "backtick": "backtick",
    "exclamation | bang": "exclamation",
    "pipe": "bar",
    "plus": "plus",
    "dollar": "dollar",
    "dork": "dot",
    "comma": "comma",
    "eke": "equal",
    "caret": "caret",
    "minus | dash": "minus",
    "percy": "percent",
    "hash | pound": "s-3",
    "question [mark] | quest": "question",
    "(single | one) quote": "dquote",
    "quote": "dquote,dquote,left",
    "under": "underscore",
    "semicolon | semi": "semicolon",
    "(single | one) smote": "squote",
    "smote": "squote,squote,left",
    "star | times": "asterisk",
    "tilde": "tilde",
    "colon": "colon",
    "right pax": "rparen",
    "left pax": "lparen",
    "pax": "lparen,rparen,left",
    "left brace": "lbrace",
    "right brace": "rbrace",
    "braces": "lbrace,rbrace,left",
    "left bracket": "lbracket",
    "right bracket": "rbracket",
    "brackets": "lbracket,rbracket,left",
    "left angle | langle": "langle",
    "right angle | rangle": "rangle",
    "angles": "langle,rangle,left",
}



ALPHANUMERIC = LOWERCASE_LETTERS.copy()
ALPHANUMERIC.update(DIGITS)


LETTERS = LOWERCASE_LETTERS.copy()
LETTERS.update(UPPERCASE_LETTERS)

ALPHANUMERIC_WITH_CAPS = LETTERS.copy()
ALPHANUMERIC_WITH_CAPS.update(DIGITS)

CHARACTERS = ALPHANUMERIC_WITH_CAPS.copy()
CHARACTERS.update(SYMBOLS)

class DigitalInteger(dragonfly.Repetition):
    '''An integer element spelled digit by digit (eg, enter 50 by saying
       'five zero'. Useful in places where Dragon would complain of the
       grammar's complexity if regular integers were used. min and max are
       number of digits, not value of the number.'''
    child = dragonfly.Choice('digit', DIGITS)

    def __init__(self, name, min, max, *args, **kw):
        dragonfly.Repetition.__init__(
            self,
            self.child,
            min,
            max,
            name=name,
            *args,
            **kw
            )

    def value(self, node):
        return int(''.join(dragonfly.Repetition.value(self, node)))
