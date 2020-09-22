import aenea.config
import aenea.configuration

from dragonfly import *
# from aenea.strict import *
# from aenea.proxy_contexts import *
from dragonfly import Key as DragonKey, Text as DragonText

from SharedChromeRules import SharedChromeRepeatablesRule, SharedChromeFinishersRule
from SharedRules import *


# chrome_context = ProxyAppContext(executable='WinAppHelper') & AppContext(executable='chrome.exe')
chrome_context = AppContext(executable='chrome')
inbox_context = chrome_context & (AppContext(title='joep.moritz@gmail.com') | AppContext(title='jmoritz@snapchat.com'))
inbox_grammar = Grammar('gmail', context=inbox_context)
inbox_tags = ['inbox']


class InboxRepeatablesRule(MappingCountRule):
    mapping = {
        'next [item] <nn>': DragonKey('right:%(nn)d'),
        'pre [item] <nn>': DragonKey('left:%(nn)d'),
        'next mess <nn>': DragonKey('n:%(nn)d'),
        'pre mess <nn>': DragonKey('p:%(nn)d'),
        # 'undo': DragonKey('z'),
        'open': DragonKey('o'),
        'close': DragonKey('u'),
        'surf': DragonKey('slash'),
        'done | archive': DragonKey('e'),
        'compose': DragonKey('c'),
        'add reminder': DragonKey('t'),
        'spam': DragonKey('exclamation'),
        'send': DragonKey('c-enter'),
        'trash': DragonKey('hash'),
        'mark <nn>': DragonKey('x/20,down') * Repeat(extra = "nn"),
        'finish cheers': DragonText('\r\rCheers,\rJoep'),
        'finish thanks': DragonText('\r\rThanks,\rJoep'),
        'finish best': DragonText('\r\rBest,\rJoep'),
        'finish kind regards': DragonText('\r\rKind regards,\rJoep Moritz'),
    }


class InboxFinishersRule(MappingRule):
    mapping = {
        'inbox': DragonKey('g,i'),
        'reply all': DragonKey('a'),
        'reply': DragonKey('r'),
        'forward': DragonKey('f'),
        'move to': DragonKey('dot'),
        'bold that': DragonKey('w-b'),
        'italics that': DragonKey('w-i'),
        'underline that': DragonKey('w-u'),
        'indent': DragonKey('w-['),
        'unindent': DragonKey('w-]'),
        '(hyperlink that | insert hyperlink)': DragonKey('w-k'),
        'numbered list': DragonKey('w-7'),
        'bulleted list': DragonKey('w-8'),
        'remove formatting': DragonKey('w-backslash'),
    }


class InboxRule(RepeatRule):
    repeatables = [
        RuleRef(rule=InboxRepeatablesRule()),
        RuleRef(rule=SharedChromeRepeatablesRule()),
        RuleRef(rule=NumberRule(map_func=DragonKey)),
        RuleRef(rule=LetterRule(map_func=DragonKey)),
        RuleRef(rule=SymbolRule(map_func=DragonKey)),
        RuleRef(rule=CommonKeysRule(map_func=DragonKey)),
    ]

    finishers = [
        RuleRef(rule=InboxFinishersRule()),
        RuleRef(rule=SharedChromeFinishersRule()),
        RuleRef(rule=FormatRule(map_func=DragonText)),
        RuleRef(rule=WindowsRule(map_func=DragonKey)),
        RuleRef(rule=ScrollRule()),
        RuleRef(rule=SwapProgramRule()),
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
