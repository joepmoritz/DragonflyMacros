import aenea.config
import aenea.configuration

from dragonfly import *
# from aenea.strict import *

from util import *
from SharedChromeRules import SharedChromeRepeatablesRule, SharedChromeFinishersRule
from SharedRules import FormatRule, CommonKeysRule, CommonRepeatables, CommonFinishers
from SharedRules import SymbolRule, LetterRule, NumberRule, ScrollRule, WindowsRule


sheets_context = AppContext(executable='Chrome', title='Google Sheets')
sheets_grammar = Grammar('chrome', context=sheets_context)


class SheetsRepeatablesRule(MappingCountRule):
    mapping = aenea.configuration.make_grammar_commands('chrome', {
            'edit':                         Key('f2'),
            'delete row': Key('a-e/20,d'),
            'delete column': Key('a-e/20,e'),
            'make bold': Key('c-b'),
            'make italic': Key('c-i'),
            'make underline': Key('c-u'),
            'select row': Key('s-space'),
            'select column': Key('c-space'),
        })


class SheetsFinishersRule(MappingRule):
    mapping = aenea.configuration.make_grammar_commands('chrome', {
            'insert row above': Key('a-i/20,r'),
            'insert row below': Key('a-i/20,b'),
            'insert column left': Key('a-i/20,c'),
            'insert column right': Key('a-i/20,o'),
            'new sheet': Key('s-f11'),
            'rename file': Key('a-f/20,r'),
            'freeze row': Key('a-v/20,r/20,o'),
            'sheet left': Key('sc-pgup'),
            'sheet right': Key('sc-pgdown'),
            '[open | follow] link': Key('c-c/3,c-t/30,c-v,enter'),
        })


class SheetsRule(RepeatRule):
    repeatables = [
        RuleRef(rule=SheetsRepeatablesRule()),
        RuleRef(rule=SharedChromeRepeatablesRule()),
    ] + CommonRepeatables()
    finishers = [
        RuleRef(rule=SheetsFinishersRule()),
        RuleRef(rule=SharedChromeFinishersRule()),
    ] + CommonFinishers()


sheets_grammar.add_rule(SheetsRule())

sheets_grammar.load()


def unload():
    global sheets_grammar
    if sheets_grammar:
        sheets_grammar.unload()
    sheets_grammar = None
