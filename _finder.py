import aenea.config
import aenea.configuration
import aenea.misc
import aenea.vocabulary

from dragonfly import *
# from aenea.strict import *
# from aenea.proxy_contexts import *

from SharedRules import MappingCountRule, FormatRule, CommonKeysRule, RepeatRule, CommonRepeatables, CommonFinishers


# finder_context = ProxyAppContext(executable='Finder') | ProxyAppContext(title='Save As') | ProxyAppContext(title='Select Folder')
finder_context = AppContext(executable='Explorer') | AppContext(title='Save As') | AppContext(title='Select Folder')

finder_grammar = Grammar('finder', context=finder_context)


class FinderRepeatablesRule(MappingCountRule):
    mapping = aenea.configuration.make_grammar_commands('finder', {
        'fish [<text>]':     Key('w-f') + Text('%(text)s'),
        'punk <nn>':         Key('w-up/50:%(nn)d'),

        'open':              Key('w-o'),
        'properties':        Key('w-i'),
        'delete':            Key('w-backspace'),
        'kill':              Key('w-backspace'),
        'back':              Key('w-lbracket'),
        'foreward':          Key('w-rbracket'),
        'address bar':       Key('a-d'),
        'new window':        Key('w-n'),
        'new folder':        Key('ws-n'),
        'rename':            Key('enter'),
        'preview':           Key('space'),
        'dope':              Key('w-c/10,w-v'),
        'copy filename':     Key('enter,w-c,escape'),
        # 'open with sublime': Key('w-apps,o,o,enter'),
        # 'extract here':      Key('w-apps/10,x/50,a-h/10,enter'),
    })


class FinderRule(RepeatRule):
    repeatables = [
        RuleRef(rule=FinderRepeatablesRule()),
        # DictListRef('dynamic finder', aenea.vocabulary.register_dynamic_vocabulary('finder')),
    ] + CommonRepeatables()
    finishers = CommonFinishers()


finder_grammar.add_rule(FinderRule())

finder_grammar.load()


def unload():
    global finder_grammar

    aenea.vocabulary.unregister_dynamic_vocabulary('finder')

    if finder_grammar:
        finder_grammar.unload()
    finder_grammar = None
