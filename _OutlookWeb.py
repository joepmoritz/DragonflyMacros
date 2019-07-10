import aenea.config
import aenea.configuration

from dragonfly import AppContext, Dictation, Grammar, IntegerRef, Key, Mouse
from dragonfly import MappingRule, Text, RuleRef, CompoundRule, Alternative
from dragonfly import Repetition, Sequence, Optional, Function, Pause, Empty, Integer, DictListRef

from util import *
from SharedChromeRules import SharedChromeRepeatablesRule, SharedChromeFinishersRule
from SharedRules import FormatRule, CommonKeysRule, CommonRepeatables, CommonFinishers
from SharedRules import SymbolRule, LetterRule, NumberRule, ScrollRule, WindowsRule



outlookweb_context = AppContext(executable='Chrome', title ='Mail - joep.moritz.13@ucl.ac.uk - Google Chrome')
outlookweb_grammar = Grammar('chrome', context=outlookweb_context)
outlookweb_tags = ['outlookweb', 'outlookweb.count']


class OutlookWebRepeatablesRule(MappingCountRule):
	mapping = aenea.configuration.make_grammar_commands('chrome', {
		'next [item] <nn>':       Key('c-dot:%(nn)d'),
		'pre [item] <nn>':        Key('c-comma:%(nn)d'),
		})


class OutlookWebFinishersRule(MappingRule):
	mapping = aenea.configuration.make_grammar_commands('chrome', {
		'inbox':      Key('g,i'),
		'drafts':     Key('g,d'),
		'sent items': Key('g,s'),
		'reply all':  Key('s-r'),
		'reply':      Key('r'),
		'forward':    Key('s-f'),
		'move to':    Key('v'),


		'open': Key('o'),
		'clove': Key('escape'),
		'close': Key('escape'),
		'serk': Key('slash'),
		'search': Key('slash'),
		'archive': Key('e'),
		'done': Key('e'),
		'compose': Key('n'),
		'new mail': Key('n'),
		'undo': Key('c-z'),
		'spam': Key('j'),
		'send': Key('a-s'),
		'trash': Key('delete'),
		'delete': Key('delete'),
		'expand': Key('x'),
		'collapse': Key('x'),

		'hi tim':              Text('Hi Tim,\n\n'),
		'hi guys':             Text('Hi guys,\n\n'),
		'hi stuart':           Text('Hi Stuart,\n\n'),
		'hi Tobias':           Text('Hi Tobias,\n\n'),
		'hi Paul':             Text('Hi Paul,\n\n'),
		'finish cheers':       Text('\n\nCheers,\nJoep'),
		'finish thanks':       Text('\n\nThanks,\nJoep'),
		'finish best':         Text('\n\nBest,\nJoep'),
		'finish kind regards': Text('\n\nKind regards,\nJoep Moritz'),
		'tom':                 Text('Tom'),
		'stuart':              Text('Stuart'),
		'tim':                 Text('Tim'),
		})




class OutlookWebRule(RepeatRule):
	repeatables = [
		RuleRef(rule=OutlookWebRepeatablesRule()),
		RuleRef(rule=SharedChromeRepeatablesRule()),
		DictListRef('dynamic outlookweb', aenea.vocabulary.register_dynamic_vocabulary('outlookweb')),
	] + CommonRepeatables()
	finishers = [
		RuleRef(rule=OutlookWebFinishersRule()),
		RuleRef(rule=SharedChromeFinishersRule()),
	] + CommonFinishers()

outlookweb_grammar.add_rule(OutlookWebRule())
outlookweb_grammar.load()


def unload():
	global outlookweb_grammar

	for tag in outlookweb_tags:
		aenea.vocabulary.unregister_dynamic_vocabulary(tag)

	if outlookweb_grammar:
		outlookweb_grammar.unload()
	outlookweb_grammar = None
