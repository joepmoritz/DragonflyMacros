import aenea.config
import aenea.configuration

from dragonfly import AppContext, Dictation, Grammar, IntegerRef, Key, Mouse
from dragonfly import MappingRule, Text, RuleRef, CompoundRule, Alternative
from dragonfly import Repetition, Sequence, Optional, Function, Pause, Empty, Integer, DictListRef
# from aenea.strict import *

from util import *
from SharedChromeRules import SharedChromeRepeatablesRule, SharedChromeFinishersRule
from SharedRules import FormatRule, CommonKeysRule, CommonRepeatables, CommonFinishers
from SharedRules import SymbolRule, LetterRule, NumberRule, ScrollRule, WindowsRule



keep_context = AppContext(executable='Chrome', title='Google Keep')
keep_grammar = Grammar('chrome', context=keep_context)


class KeepRepeatablesRule(MappingCountRule):
    mapping = aenea.configuration.make_grammar_commands('chrome', {
        'next': Key('j'),
        'previous': Key('k'),
        'next item': Key('n'),
        'previous item': Key('p'),
        'new note': Key('c'),
        'new list': Key('l'),
        'search': Key('slash'),
        'archive | done': Key('e'),
        'delete | bin': Key('hash'),
        'select': Key('x'),
        'toggle (checkboxes | list)': Key('ws-8'),
        })


class KeepFinishersRule(MappingRule):
    mapping = aenea.configuration.make_grammar_commands('chrome', {
        'forward':                         Key('f'),
        })


class KeepRule(RepeatRule):
    repeatables = CommonRepeatables() + [
        RuleRef(rule=KeepRepeatablesRule()),
        RuleRef(rule=SharedChromeRepeatablesRule()),
    ]
    finishers = CommonFinishers() + [
        # RuleRef(rule=KeepFinishersRule()),
        RuleRef(rule=SharedChromeFinishersRule()),
    ]


keep_grammar.add_rule(KeepRule())

keep_grammar.load()


def unload():
    global keep_grammar
    if keep_grammar:
        keep_grammar.unload()
    keep_grammar = None
