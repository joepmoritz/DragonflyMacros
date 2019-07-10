import aenea.config
import aenea.configuration
import aenea.misc
import aenea.vocabulary

from dragonfly import AppContext, Dictation, Grammar, IntegerRef, Key, Mouse
from dragonfly import MappingRule, Text, RuleRef, CompoundRule, Alternative
from dragonfly import Repetition, Sequence, Optional, Function, Pause, Empty, Integer, DictListRef

from SharedRules import MappingCountRule, FormatRule, CommonKeysRule, RepeatRule, CommonRepeatables, CommonFinishers



finder_context = AppContext(executable='explorer') | AppContext(title ='Save As') | AppContext(title ='Select Folder')

finder_grammar = Grammar('finder', context=finder_context)


class FinderRepeatablesRule(MappingCountRule):
    mapping = aenea.configuration.make_grammar_commands('finder', {
        'fish [<text>]':                                   Key('c-f') + Text('%(text)s'),
        'punk <nn>':                Key('a-up/50:%(nn)d'),

        'open':              Key('enter'),
        'properties':        Key('a-enter'),
        'delete':            Key('delete'),
        'kill':              Key('delete'),
        'back':              Key('a-left'),
        'foreward':          Key('a-right'),
        'address bar':       Key('a-d'),
        'new window':        Key('c-n'),
        'new folder':        Key('cs-n'),
        'rename':            Key('f2'),
        'preview pane':      Key('a-v/10,p'),
        'dupe':              Key('c-c/10,c-v'),
        'copy filename':     Key('f2,s-end,c-c,escape'),
        'open with sublime': Key('w-apps,o,o,enter'),
        'extract here':      Key('w-apps/10,x/50,a-h/10,enter'),
        'subset':            Key('w-apps/10,n/10,m/10,m/10,m/10,enter'),
        'fit columns':       Key('a-v,s,f'),
        'column date':       Key('a-v/10,a/10,enter'),
        'column type':       Key('a-v/10,a/10,down/10,enter'),
        'column size':       Key('a-v/10,a/10,down/10:2,enter'),
        'column tags':       Key('a-v/10,a/10,down/10:3,enter'),
        'column dimensions': Key('a-v/10,a/10,down/10:7,enter'),
        'details':           Key('a-v/10,l/10,pgup/10,right/10,right/10,down/10,enter'),
        'list view':         Key('a-v/10,l/10,pgup/10,right/10,down/10,enter'),
        'extra large icons': Key('a-v/50,l/50,pgup/20,enter')
        })


class FinderRule(RepeatRule):
    repeatables = CommonRepeatables() + [
        RuleRef(rule=FinderRepeatablesRule()),
        # DictListRef('dynamic finder', aenea.vocabulary.register_dynamic_vocabulary('finder')),
    ]
    finishers = CommonFinishers()


finder_grammar.add_rule(FinderRule())

finder_grammar.load()


def unload():
    global finder_grammar

    aenea.vocabulary.unregister_dynamic_vocabulary('finder')

    if finder_grammar:
        finder_grammar.unload()
    finder_grammar = None