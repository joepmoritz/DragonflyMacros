import aenea.format

from dragonfly import *

from SwapProgram import SwapProgramRule
from util import DictateWords, NoCompile, MappingCountRule, RepeatRule
# from tobii import *




windows_commands = {
	'clove <nn>':        Key('c-w/100:%(nn)d'),
	'quit':              Key('a-f4'),
	'flick':             Key('w-squote'),
	'maximise':          Key('a-space/20,r/20,a-space/100,x'),
	'minimise':          Key('a-space/20,r/20,a-space/100,n'),
	'left window':       Key('a-space/5,x/10,w-left'),
	'right window':      Key('a-space/5,x/10,w-right'),
	'top window':        Key('w-up'),
	'bottom window':     Key('w-down'),
	'woosh':             Key('w-tab'),
	'tapple':            Key('a-tab'),
}


symbol_after_format_mapping = {
	'eke': Key('equal'),
	'plus': Key('plus'),
	'minus': Key('minus'),
	'dork': Key('dot'),
	'pax': Key('lparen'),
	'brax': Key('lbracket'),
	'comma': Key('comma'),
	'rike': Key('right'),
	'ace': Key('space'),
	'slash': Key('slash'),
	'colon': Key('colon'),
	'lex': Key('end'),
	'steak': Key('c-s'),
	'slap': Key('enter'),
}


common_keys_mapping = {
	# Keys
	'slap <nn>' :                         Key('enter:%(nn)d'),
	'ace <nn>' :                          Key('space:%(nn)d'),
	'act' :                               Key('escape'),
	'(tab | tap) <nn>' :                  Key('tab/20:%(nn)d/20'),
	'backtab <nn>' :                      Key('s-tab/20:%(nn)d/20'),
	'cop' :                               Key('c-c'),
	'cut' :                               Key('c-x'),
	'pake' :                              Key('c-v'),
	'plain pake':                         Key('sc-v'),
	'select all' :                        Key('c-a'),
	'delete all' :                        Key('c-a,del'),
	'copy all' :                          Key('c-a,c-c'),
	'undo <nn>':                          Key('c-z:%(nn)d'),
	'redo <nn>':                          Key('c-y:%(nn)d'),
	'steak':                              Key('c-s'),

	# Movement:
	# The delay is to fix bug in sublime using command chain of open X dunce N slap
	'pup <nn>' :                          Key('up/3:%(nn)d/4'),
	'dos <nn>' :                          Key('down/3:%(nn)d/4'),
	'loof <nn>' :                         Key('left/3:%(nn)d/4'),
	'rike <nn>' :                         Key('right/3:%(nn)d/4'),
	'woloof <nn>' :                       Key('c-left:%(nn)d'),
	'wolike <nn>' :                       Key('c-right:%(nn)d'),
	'subloof <nn>' :                      Key('a-left:%(nn)d'),
	'sublike <nn>' :                      Key('a-right:%(nn)d'),
	'lin' :                               Key('home'),
	'lex' :                               Key('end'),
	'win lin':                            Key('c-home'),
	'win lex':                            Key('c-end'),
	'grip <nn>':                          Key('pgup/10:%(nn)d'),
	'drop <nn>':                          Key('pgdown/10:%(nn)d'),

	# selection:
	'seloof <nn>' :                       Key('s-left/2:%(nn)d/2'),
	'selike <nn>' :                       Key('s-right/2:%(nn)d/2'),
	'sewoloof <nn>' :                     Key('sc-left:%(nn)d'),
	'sewolike <nn>' :                     Key('sc-right:%(nn)d'),
	'sesubloof <nn>' :                    Key('sa-left:%(nn)d'),
	'sesublike <nn>' :                    Key('sa-right:%(nn)d'),
	'skive up <nn>' :                     Key('home,s-up:%(nn)d'),
	'skive <nn>' :                        Key('home,s-down:%(nn)d'),
	'stick lin' :                         Key('s-home'),
	'stick lex' :                         Key('s-end'),

	# deletion:
	'leet <nn>' :                        Key('del:%(nn)d'),
	'sack <nn>' :                        Key('backspace:%(nn)d'),
	'chomp <nn>':                        Key('sc-right:%(nn)d, del'),
	'smack <nn>':                        Key('sc-left:%(nn)d, del'),
	'kill <nn>':                         Key('home,s-down:%(nn)d,del'),

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
	# 'mup <nn>' :                          Key('up:%(nn)d/3'),
	# 'munce <nn>' :                        Key('down:%(nn)d/3'),
	# 'moof <nn>' :                         Key('left:%(nn)d'),
	# 'myke <nn>' :                         Key('right:%(nn)d'),
	# 'milk <nn>' :                         Key('c-left:%(nn)d'),
	# 'murk <nn>' :                         Key('c-right:%(nn)d'),
	# 'mince' :                               Key('home'),
	# 'mandy' :                               Key('end'),
	# 'mip <nn>':                          Key('pgup/10:%(nn)d'),
	# 'mop <nn>':                          Key('pgdown/10:%(nn)d'),

	# # selection:
	# 'chup <nn>' :                     Key('s-up:%(nn)d'),
	# 'chunce <nn>' :                        Key('s-down:%(nn)d'),
	# 'choof <nn>' :                       Key('s-left:%(nn)d'),
	# 'chyke <nn>' :                       Key('s-right:%(nn)d'),
	# 'chilk <nn>' :                        Key('sc-left:%(nn)d'),
	# 'churk <nn>' :                        Key('sc-right:%(nn)d'),
	# 'chince' :                      Key('s-home'),
	# 'chandy' :                             Key('s-end'),
	# 'chip <nn>':                          Key('s-pgup/10:%(nn)d'),
	# 'chop <nn>':                          Key('s-pgdown/10:%(nn)d'),

	# # delete:
	# 'dup <nn>' :   Key('up:%(nn)d/3'),
	# 'dunce <nn>' : Key('down:%(nn)d/3'),
	# 'doof <nn>' :  Key('backspace:%(nn)d'),
	# 'dyke <nn>' :  Key('del:%(nn)d'),
	# 'dilk <nn>' :  Key('c-backspace:%(nn)d'),
	# 'durk <nn>' :  Key('c-del:%(nn)d'),
	# 'dince' :      Key('s-home,del'),
	# 'dandy' :      Key('s-end,del'),
	# 'dip <nn>':    Key('s-pgup/10:%(nn)d,del'),
	# 'dop <nn>':    Key('s-pgdown/10:%(nn)d,del'),


}










class CommonKeysRule(MappingCountRule):
	exported = False
	mapping = common_keys_mapping



letter_mapping = dict((key, Key(value)) for (key, value) in aenea.misc.LETTERS.iteritems())
class LetterRule(MappingRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('shared', letter_mapping)


symbol_mapping = dict((key, Key(value)) for (key, value) in aenea.misc.SYMBOLS.iteritems())
class SymbolRule(MappingRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('shared', symbol_mapping)


class NumberRule(MappingRule):
	exported = False
	extras = [IntegerRef(name = 'n', min = 0, max = 49)]
	defaults = {'n': 1}
	mapping = aenea.configuration.make_grammar_commands('shared', {
		'[num] <n>':     Text('%(n)d'),
	})


class CommonCommandsRule(MappingRule):
	mapping = aenea.configuration.make_grammar_commands('shared', {
		'save' :                              Key('c-s'),
		'open' :                              Key('c-o'),
		'new' :                               Key('c-n'),
		'new window' :                        Key('sc-n'),
		'print' :                             Key('c-p'),
	})



class WindowsRule(MappingCountRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('shared', windows_commands)


class ScrollRule(MappingCountRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('shared', {
		# scrolling
		# 'scone <nn>' :            Function(eye_tracker_phantom_mouse).bind({"action": Mouse('wheeldown:%(nn)d/30') * 3}),
		# 'scup <nn>' :             Function(eye_tracker_phantom_mouse).bind({"action": Mouse('wheelup:%(nn)d/30') * 3}),
		# '(I|eye) print position': Function(eye_tracker_print_position),
		'scone <nn>' :            Mouse('wheeldown:%(nn)d/30') * 3,
		'scup <nn>' :             Mouse('wheelup:%(nn)d/30') * 3,
	})


class MouseRule(MappingCountRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('mouse', {
		# '(I|eye) kick' :        Function(eye_tracker_phantom_mouse).bind({"action": Mouse('left')}),
		'kick':                 Mouse('left'),
		'rick':                 Mouse('right'),
		'dub':                  Mouse('left:2'),
	})


class SayRule(MappingRule):
	mapping = aenea.configuration.make_grammar_commands('say', {
		'say <text>': Text('%(text)s'),
	})
	extras = [DictateWords(name='text')]


class FormatRule(CompoundRule):
	exported = False
	spec = ('[upper | natural | lower] ( constant | titan | camel | rel-path | abs-path | score | sentence | '
		'scope-resolve | jumble | dotword | dashword | natword | snake | brooding-narrative) <dictation>')
	extras = [DictateWords(name='dictation')]

	def value(self, node):
		words = node.words()

		uppercase = words[0] == 'upper'
		lowercase = words[0] == 'lower'
		natural = words[0] == 'natural'

		if not uppercase and not lowercase and not natural and words[0] == 'score':
			lowercase = True

		if words[0].lower() in ('upper', 'natural', 'lower'):
			del words[0]

		format_word = words[0].lower()
		del words[0]

		text_words = []
		for w in words:
			text_words += w.split('\\', 1)[0].split('-')

		if lowercase:
			text_words = [word.lower() for word in text_words]
		if uppercase:
			text_words = [word.upper() for word in text_words]

		if format_word == 'constant':
			format_word = 'score';
			text_words = [word.upper() for word in text_words]

		function = getattr(aenea.format, 'format_%s' % format_word)
		formatted = function(text_words)

		return Text(formatted)

class SymbolAfterFormatRule(MappingCountRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('shared', symbol_after_format_mapping)



class ChainFormatRule(MappingRule):
	def Execute(format_rule_before_symbol_rule, symbol_after_format_rule):
		format_rule_before_symbol_rule.execute()
		symbol_after_format_rule.execute()

	mapping = {
		'<format_rule_before_symbol_rule> <symbol_after_format_rule>': Function(Execute),
	}

	extras = [
		RuleRef(name = 'format_rule_before_symbol_rule', rule = FormatRule(name = 'FormatRuleBeforeSymbolRule')),
		RuleRef(name = 'symbol_after_format_rule', rule = SymbolAfterFormatRule()),
	]


def CommonRepeatables():
	return [
		RuleRef(rule = NumberRule()),
		RuleRef(rule = LetterRule()),
		RuleRef(rule = SymbolRule()),
		RuleRef(rule = CommonKeysRule()),
		# RuleRef(rule = MouseRule()),
		# RuleRef(rule = ChainFormatRule()),
		# dictRule,
	]

def CommonFinishers():
	return [
		# RuleRef(rule = SayRule()),
		RuleRef(rule = FormatRule()),
		RuleRef(rule = WindowsRule(), name='windows'),
		RuleRef(rule = ScrollRule()),
		RuleRef(rule = SwapProgramRule()),
	]

class CommonRepeatRule(RepeatRule):
	repeatables = CommonRepeatables()
	finishers = CommonFinishers()


