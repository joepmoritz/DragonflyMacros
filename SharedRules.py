import aenea.format

from dragonfly import Key as DragonKey, Text as DragonText, Mouse as DragonMouse
from dragonfly import *
# from aenea.strict import Key as AeneaKey, Text as AeneaText, Mouse as AeneaMouse
# from aenea.strict import *

from SwapProgram import SwapProgramRule
from util import DictateWords, NoCompile, MappingCountRule, RepeatRule
# from tobii import *

DEFAULT_KEY = DragonKey
DEFAULT_TEXT = DragonText
DEFAULT_MOUSE = DragonMouse

def SwitchKey(text, win_text=None):
	def MakeKey(cls=DEFAULT_KEY):
		return cls(win_text if cls == DragonKey and win_text else text)
	return MakeKey

def ForceKey(text, cls=DEFAULT_KEY):
	def MakeKey(unused):
		return cls(text)
	return MakeKey




windows_commands = {
	'clove <nn>':        SwitchKey('w-w/100:%(nn)d', 'c-w/100:%(nn)d'),
	'clove window':      SwitchKey('sw-w', 'cs-w'),
	# 'preferences':       SwitchKey('w-comma'),
	# 'quit':              SwitchKey('w-q', 'a-f4'),
	'flick':             ForceKey('w-backtick'),
	'maximise':          SwitchKey('wa-up', 'alt:down,space/20,x/20,alt:up'),
	'minimise':          SwitchKey('w-m', 'a-space/10,alt:down,space/20,n/20,alt:up'),
	'left window':       ForceKey('w-left'),
	'right window':      ForceKey('w-right'),
	# 'top window':        'w-upSwitchKey('),
	# 'bottom window':     'w-downSwitchKey('),
	# 'woosh':             'w-tabSwitchKey('),
	'tapple':            ForceKey('a-tab'),
}


symbol_after_format_mapping = {
	'eke': 'equal',
	'plus': 'plus',
	'minus': 'minus',
	'dork': 'dot',
	'pax': 'lparen',
	'brackets': 'lbracket',
	'comma': 'comma',
	'ripe': 'right',
	'ace': 'space',
	'slash': 'slash',
	'colon': 'colon',
	'lex': 'end',
	'steak': 'w-s',
	'slap': 'enter',
}


common_keys_mapping = {
	# Keys
	'slap <nn>' :                         SwitchKey('enter:%(nn)d'),
	'ace <nn>' :                          SwitchKey('space:%(nn)d'),
	'act' :                               SwitchKey('escape'),
	'(tab | tap) <nn>' :                  SwitchKey('tab/20:%(nn)d/20'),
	'backtab <nn>' :                      SwitchKey('s-tab/20:%(nn)d/20'),
	'cop' :                               SwitchKey('w-c', 'c-c'),
	'cut' :                               SwitchKey('w-x', 'c-x'),
	'paste' :                             SwitchKey('w-v', 'c-v'),
	'plain paste':                        SwitchKey('ws-v', 'cs-v'),
	'select all' :                        SwitchKey('w-a', 'c-a'),
	'delete all' :                        SwitchKey('w-a,del', 'c-a,del'),
	'copy all' :                          SwitchKey('w-a,w-c', 'c-a,c-c'),
	'undo <nn>':                          SwitchKey('w-z:%(nn)d','c-z:%(nn)d'),
	'redo <nn>':                          SwitchKey('ws-z:%(nn)d','c-y:%(nn)d'),
	'steak':                              SwitchKey('w-s','c-s'),
	# 'don\'t save':                        SwitchKey('w-d'),

	# Movement:
	# The delay is to fix bug in sublime using command chain of open X dunce N slap
	'pup <nn>' :                          SwitchKey('up/3:%(nn)d/4'),
	'(DOS | dunce) <nn>' :                SwitchKey('down/3:%(nn)d/4'),
	'loof <nn>' :                         SwitchKey('left/3:%(nn)d/4'),
	'ripe <nn>' :                         SwitchKey('right/3:%(nn)d/4'),
	'woloof <nn>' :                       SwitchKey('a-left:%(nn)d', 'c-left:%(nn)d'),
	'wolipe <nn>' :                       SwitchKey('a-right:%(nn)d', 'c-right:%(nn)d'),
	'lin' :                               SwitchKey('w-left', 'home'),
	'lex' :                               SwitchKey('w-right', 'end'),
	'win lin':                            SwitchKey('w-up', 'c-home'),
	'win lex':                            SwitchKey('w-down', 'c-end'),
	'grip <nn>':                          SwitchKey('pgup/10:%(nn)d'),
	'drop <nn>':                          SwitchKey('pgdown/10:%(nn)d'),

	# selection:
	'seloof <nn>' :                       SwitchKey('s-left/2:%(nn)d/2'),
	'selipe <nn>' :                       SwitchKey('s-right/2:%(nn)d/2'),
	'sewoloof <nn>' :                     SwitchKey('sa-left:%(nn)d','sc-left:%(nn)d'),
	'sewolipe <nn>' :                     SwitchKey('sa-right:%(nn)d','sc-right:%(nn)d'),
	'skive up <nn>' :                     SwitchKey('w-left,s-up:%(nn)d','home,s-up:%(nn)d'),
	'skive <nn>' :                        SwitchKey('w-left,s-down:%(nn)d','home,s-down:%(nn)d'),
	'stick lin' :                         SwitchKey('sw-left', 's-home'),
	'stick lex' :                         SwitchKey('sw-right', 's-end'),

	# deletion:
	'leet <nn>' :                        SwitchKey('del:%(nn)d'),
	'sack <nn>' :                        SwitchKey('backspace:%(nn)d'),
	'chomp <nn>':                        SwitchKey('sa-right:%(nn)d, del','sc-right:%(nn)d, del'),
	'smack <nn>':                        SwitchKey('sa-left:%(nn)d, del','sc-left:%(nn)d, del'),
	'kill <nn>':                         SwitchKey('w-left,s-down:%(nn)d,del','home,s-down:%(nn)d,del'),

	# idea: split into prefix and suffix for action and subject
	# movement: m
	# selection: ch or sl or st
	# delete: d
	# up: up
	# down: unce
	# left: oof
	# right: yke
	# word left: ilk
	# word right: irk
	# line start: in
	# line and: ex
	# page up: ip
	# page down: op

	# # Movement:
	# # The delay is to fix bug in sublime using command chain of open X dunce N slap
	# 'mup <nn>' :                          'up:%(nn)d/3',
	# 'munce <nn>' :                        'down:%(nn)d/3',
	# 'moof <nn>' :                         'left:%(nn)d',
	# 'myke <nn>' :                         'right:%(nn)d',
	# 'milk <nn>' :                         'c-left:%(nn)d',
	# 'murk <nn>' :                         'c-right:%(nn)d',
	# 'mince' :                               'home',
	# 'mandy' :                               'end',
	# 'mip <nn>':                          'pgup/10:%(nn)d',
	# 'mop <nn>':                          'pgdown/10:%(nn)d',

	# # selection:
	# 'chup <nn>' :                     's-up:%(nn)d',
	# 'chunce <nn>' :                        's-down:%(nn)d',
	# 'choof <nn>' :                       's-left:%(nn)d',
	# 'chyke <nn>' :                       's-right:%(nn)d',
	# 'chilk <nn>' :                        'sc-left:%(nn)d',
	# 'churk <nn>' :                        'sc-right:%(nn)d',
	# 'chince' :                      's-home',
	# 'chandy' :                             's-end',
	# 'chip <nn>':                          's-pgup/10:%(nn)d',
	# 'chop <nn>':                          's-pgdown/10:%(nn)d',

	# # delete:
	# 'dup <nn>' :   'up:%(nn)d/3',
	# 'dunce <nn>' : 'down:%(nn)d/3',
	# 'doof <nn>' :  'backspace:%(nn)d',
	# 'dyke <nn>' :  'del:%(nn)d',
	# 'dilk <nn>' :  'c-backspace:%(nn)d',
	# 'durk <nn>' :  'c-del:%(nn)d',
	# 'dince' :      's-home,del',
	# 'dandy' :      's-end,del',
	# 'dip <nn>':    's-pgup/10:%(nn)d,del',
	# 'dop <nn>':    's-pgdown/10:%(nn)d,del',
}

letter_mapping = aenea.misc.LETTERS
symbol_mapping = aenea.misc.SYMBOLS

format_mapping = {
	'score <score_text>': '%(score_text)s',
	'titan <titan_text>': '%(titan_text)s',
	'camel <camel_text>': '%(camel_text)s',
	'dash word <dash_word_text>': '%(dash_word_text)s',
	'constant <constant_text>': '%(constant_text)s',
	'jumble <jumble_text>': '%(jumble_text)s',
	'sentence <sentence_text>': '%(sentence_text)s',
	'say <say_text>': '%(say_text)s',
}

format_extras = [
	Dictation(name='score_text').lower().replace(" ", "_"),
	Dictation(name='titan_text').title().replace(" ", ""),
	Dictation(name='camel_text').lower().camel(),
	Dictation(name='dash_word_text').lower().replace(" ", "-"),
	Dictation(name='constant_text').upper().replace(" ", "_"),
	Dictation(name='jumble_text').replace(" ", ""),
	Dictation(name='sentence_text').capitalize(),
	Dictation(name='say_text'),
]


n = ShortIntegerRef(name='n', min=0, max=10000)
n1 = {'n': 1}
nn = NoCompile(Optional(Integer(min=0, max=99), default=1), name='nn')
nn1 = {'nn': 1}


def map_values(l, d):
	return {k: l(v) for k, v in d.iteritems()}

def create_mapping_rule(mapping, map_func=DEFAULT_KEY, extras=None, defaults=None, **kwargs):
	return MappingRule(exported=False, mapping=map_values(map_func, mapping), extras=extras, defaults=defaults, **kwargs)


def CommonKeysRule(mapping=common_keys_mapping, extras=[nn], defaults=nn1, map_func=DEFAULT_KEY, **kwargs):
	return create_mapping_rule(mapping=mapping, map_func=lambda f: f(map_func), extras=extras, defaults=defaults, **kwargs)


def LetterRule(mapping=letter_mapping, map_func=DEFAULT_KEY, **kwargs):
	return create_mapping_rule(mapping=mapping, map_func=map_func, **kwargs)


def SymbolRule(mapping=symbol_mapping, map_func=DEFAULT_KEY, **kwargs):
	return create_mapping_rule(mapping=mapping, map_func=map_func, **kwargs)


def NumberRule(extras=[n], map_func=DEFAULT_TEXT, **kwargs):
	return create_mapping_rule(mapping={'[num] <n>': '%(n)d'}, extras=extras, defaults=n1, map_func=map_func, **kwargs)


def WindowsRule(mapping=windows_commands, extras=[nn], defaults=nn1, map_func=DEFAULT_KEY, **kwargs):
	return create_mapping_rule(mapping=mapping, map_func=lambda f: f(map_func), extras=extras, defaults=defaults, **kwargs)



class ScrollRule(MappingCountRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('shared', {
		# scrolling
		# 'scone <nn>' :            Function(eye_tracker_phantom_mouse).bind({"action": Mouse('wheeldown:%(nn)d/30') * 3}),
		# 'scup <nn>' :             Function(eye_tracker_phantom_mouse).bind({"action": Mouse('wheelup:%(nn)d/30') * 3}),
		# '(I|eye) print position': Function(eye_tracker_print_position),
		'scone <nn>' :            DEFAULT_MOUSE('wheeldown:%(nn)d/30') * 3,
		'scup <nn>' :             DEFAULT_MOUSE('wheelup:%(nn)d/30') * 3,
	})


class MouseRule(MappingCountRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('mouse', {
		# '(I|eye) kick' :        Function(eye_tracker_phantom_mouse).bind({"action": Mouse('left')}),
		'kick':                 DEFAULT_MOUSE('left'),
		'rick':                 DEFAULT_MOUSE('right'),
		'dub':                  DEFAULT_MOUSE('left:2'),
	})


def FormatRule(mapping=format_mapping, map_func=DEFAULT_TEXT, extras=format_extras, **kwargs):
	return create_mapping_rule(mapping=mapping, map_func=map_func, extras=extras, **kwargs)


def SymbolAfterFormatRule(mapping=symbol_after_format_mapping, map_func=DEFAULT_KEY, **kwargs):
	return create_mapping_rule(mapping=mapping, map_func=map_func, **kwargs)


def DoubleRule(rule1, rule2):
	def Execute(rule1, rule2):
		rule1.execute()
		rule2.execute()

	mapping = {
		'<rule1> <rule2>': Function(Execute),
	}

	extras = [
		RuleRef(name='rule1', rule=rule1),
		RuleRef(name='rule2', rule=rule2),
	]

	return MappingRule(exported=False, mapping=mapping, extras=extras)


def ChainFormatRule(format_rule=FormatRule, symbol_after_format_rule=SymbolAfterFormatRule):
	return DoubleRule(format_rule(), symbol_after_format_rule())



def create_rules(rules):
	return [RuleRef(rule=r) for r in rules]

common_repeatable_rules = [
	NumberRule(),
	LetterRule(),
	SymbolRule(),
	CommonKeysRule(),
]

common_finishers_rules = [
	FormatRule(),
	WindowsRule(),
	ScrollRule(),
	SwapProgramRule(),
]

def CommonRepeatables(repeatables=common_repeatable_rules):
	return create_rules(repeatables)

def CommonFinishers(finishers=common_finishers_rules):
	return create_rules(finishers)

class CommonRepeatRule(RepeatRule):
	repeatables = CommonRepeatables()
	finishers = CommonFinishers()


