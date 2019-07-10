import aenea.config
import aenea.configuration

from dragonfly import *

from SharedChromeRules import SharedChromeRepeatablesRule, SharedChromeFinishersRule
from SharedRules import MappingCountRule, RepeatRule, CommonRepeatables, CommonFinishers


inbox_context = AppContext(executable='Chrome', title='joep.moritz@gmail.com')
inbox_grammar = Grammar('chrome', context=inbox_context)
inbox_tags = ['inbox']


class InboxRepeatablesRule(MappingCountRule):
    mapping = aenea.configuration.make_grammar_commands('chrome', {
        'next [item] <nn>': Key('right:%(nn)d'),
        'pre [item] <nn>': Key('left:%(nn)d'),
        'next mess <nn>': Key('n:%(nn)d'),
        'pre mess <nn>': Key('p:%(nn)d'),
        # 'undo': Key('z'),
        'open': Key('o'),
        'close': Key('u'),
        'serk': Key('slash'),
        'done': Key('y'),
        'compose': Key('c'),
        'add reminder': Key('t'),
        'spam': Key('exclamation'),
        # 'send': Key('up,c-enter'),
        'trash': Key('hash'),
        'mark': Key('x'),
        'finish cheers': Text('\n\nCheers,\nJoep'),
        'finish thanks': Text('\n\nThanks,\nJoep'),
        'finish best': Text('\n\nBest,\nJoep'),
        'finish kind regards': Text('\n\nKind regards,\nJoep Moritz'),
    })


class InboxFinishersRule(MappingRule):
    mapping = aenea.configuration.make_grammar_commands('chrome', {
        'inbox': Key('i'),
        'reply all': Key('s-a'),
        'reply': Key('s-r'),
        'forward': Key('f'),
        'move to': Key('dot'),
        'bold that': Key('c-b'),
        'italics that': Key('c-i'),
        'underline that': Key('c-u'),
        '(hyperlink that | insert hyperlink)': Key('c-k'),
        'numbered list': Key('c-7'),
        'bulleted list': Key('c-8'),
        'remove formatting': Key('c-backslash'),
    })


class InboxRule(RepeatRule):
    repeatables = [
        RuleRef(rule=InboxRepeatablesRule()),
        RuleRef(rule=SharedChromeRepeatablesRule()),
    ] + CommonRepeatables()

    finishers = CommonFinishers() + [
        RuleRef(rule=InboxFinishersRule()),
        RuleRef(rule=SharedChromeFinishersRule()),
    ]


inbox_grammar.add_rule(InboxRule())
inbox_grammar.load()


def unload():
    global inbox_grammar

    if inbox_grammar:
        inbox_grammar.unload()

    for tag in inbox_tags:
        aenea.vocabulary.unregister_dynamic_vocabulary(tag)

    inbox_grammar = None
