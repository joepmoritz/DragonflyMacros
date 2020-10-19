
LOWERCASE_LETTERS = {
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
}


UPPERCASE_LETTERS = dict(('cap ' + key, value.upper()) for (key, value) in LOWERCASE_LETTERS.iteritems())

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

SYMBOLS = {
    "ampersand": "ampersand",
    "(slash | divided [by])": "slash",
    "at sign": "at",
    "backslash": "backslash",
    "backtick": "backtick",
    "bang": "exclamation",
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
    "quest": "question",
    "single quote": "dquote",
    "under": "underscore",
    "semi": "semicolon",
    "single smote": "squote",
    "star | times": "asterisk",
    "tilde": "tilde",
    "colon": "colon",
    "left pax": "lparen",
    "right pax": "rparen",
    "left brace": "lbrace",
    "right brace": "rbrace",
    "left bracket": "lbracket",
    "right bracket": "rbracket",
    "left angle | langle": "langle",
    "right angle | rangle": "rangle"}

SHORT_SNIPPETS = {
    "quote": "dquote,dquote,left",
    "smote": "squote,squote,left",
    "pax": "lparen,rparen,left",
    "braces": "lbrace,rbrace,left",
    "brackets": "lbracket,rbracket,left",
    "angles": "langle,rangle,left",
    "ticky": "backtick,backtick,left",
}



ALPHANUMERIC = LOWERCASE_LETTERS.copy()
ALPHANUMERIC.update(DIGITS)


LETTERS = LOWERCASE_LETTERS.copy()
LETTERS.update(UPPERCASE_LETTERS)

ALPHANUMERIC_WITH_CAPS = LETTERS.copy()
ALPHANUMERIC_WITH_CAPS.update(DIGITS)

CHARACTERS = ALPHANUMERIC_WITH_CAPS.copy()
CHARACTERS.update(SYMBOLS)