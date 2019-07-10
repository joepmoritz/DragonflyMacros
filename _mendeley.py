import aenea.configuration
import aenea.vocabulary

from dragonfly import AppContext, Grammar, Key
from dragonfly import MappingRule, Text, RuleRef, CompoundRule
from dragonfly import Function, Pause, DictListRef

from sikuli import dragonfly_proxy as sikuli

from util import MappingCountRule, RepeatRule
from SharedRules import CommonRepeatables, CommonFinishers



mendeley_context = AppContext(executable='MendeleyDesktop.exe')

mendeley_grammar = Grammar('Mendeley', context=mendeley_context)


class MendeleyRepeatablesRule(MappingCountRule):
	mapping = aenea.configuration.make_grammar_commands('finder', {
		'serk [<text>]':                Key('c-f') + Text('%(text)s'),
		})


class MendeleyRule(RepeatRule):
	repeatables = CommonRepeatables() + [
		RuleRef(rule=MendeleyRepeatablesRule()),
		DictListRef('mendeley_sikuli', sikuli.get_mapping('mendeley')),
	]
	finishers = CommonFinishers()


mendeley_grammar.add_rule(MendeleyRule())

mendeley_grammar.load()


def unload():
	global mendeley_grammar

	if mendeley_grammar:
		mendeley_grammar.unload()
	mendeley_grammar = None
