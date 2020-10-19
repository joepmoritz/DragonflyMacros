import aenea.config
import aenea.configuration

from dragonfly import *
# from aenea.strict import *
# from aenea.proxy_contexts import *
from dragonfly import Key as DragonKey, Text as DragonText

from SharedRules import *
from util import *
from SharedChromeRules import SharedChromeRepeatablesRule, SharedChromeFinishersRule


inbox_context = AppContext(executable='Chrome', title='joep.moritz@gmail.com')
sheets_context = AppContext(executable='Chrome', title='Google Sheets')
keep_context = AppContext(executable='Chrome', title='Google Keep')
outlookweb_context = AppContext(executable='Chrome', title='Mail - joep.moritz.13@ucl.ac.uk - Google Chrome')
# chrome_context = AppContext(executable='WinAppHelper') & AppContext(executable='chrome.exe')
chrome_context = AppContext(executable='Chrome')

other_chrome_context = chrome_context & ~inbox_context & ~outlookweb_context & ~sheets_context & ~keep_context
other_chrome_grammar = Grammar('chrome', context=other_chrome_context)
other_chrome_finishers_tags = ['other_chrome_finishers']


class OtherChromeRepeatablesRule(MappingRule):
    mapping = {
        'address [bar]': DragonKey('a-d'), # 'w-l'
        # 'top frame':     DragonKey('g,s-f'),
        # 'next frame':    DragonKey('g,f'),
        'add bookmark':  DragonKey('c-d'), # 'w-d'
        'copy address':  DragonKey('a-d/10,c-c'), # 'w-l,w-c'
        'open':          DragonKey('enter'),
        'input':         DragonKey('g,i'),
    }


class OtherChromeFinishersRule(MappingCountRule):
    mapping = aenea.configuration.make_grammar_commands('chrome', {
        'next':                 DragonKey('rbracket:2'),
        'pre':                  DragonKey('lbracket:2'),
        'back <nn>':            DragonKey('a-left:%(nn)d'), # 'w-lbracket:%(nn)d'
        'forward <nn>':         DragonKey('a-right:%(nn)d'), # 'w-rbracket:%(nn)d'
        'fish | surf [<text>]': DragonKey('c-f') + DragonText('%(text)s'),
    })


class OtherChromeRule(RepeatRule):
    repeatables = [
        RuleRef(rule=OtherChromeRepeatablesRule()),
        RuleRef(rule=SharedChromeRepeatablesRule()),
        RuleRef(rule=NumberRule(map_func=DragonKey)),
        RuleRef(rule=LetterRule(map_func=DragonKey)),
        RuleRef(rule=SymbolRule(map_func=DragonKey)),
        RuleRef(rule=CommonKeysRule(map_func=DragonKey)),
    ]
    finishers = [
        RuleRef(rule=OtherChromeFinishersRule()),
        RuleRef(rule=SharedChromeFinishersRule()),
        DictListRef('dynamic other chrome finishers', aenea.vocabulary.register_dynamic_vocabulary('other_chrome_finishers')),
        RuleRef(rule=FormatRule(map_func=DragonText)),
        RuleRef(rule=WindowsRule(map_func=DragonKey)),
        RuleRef(rule=ScrollRule()),
        RuleRef(rule=SwapProgramRule()),
    ]


# other_chrome_grammar.add_rule(finishLinkRule)
other_chrome_grammar.add_rule(OtherChromeRule())
# other_chrome_grammar.add_rule(AllTabsChromeRule())
other_chrome_grammar.load()

aenea.vocabulary.add_window_title_tag('Overleaf', 'latex_file')
aenea.vocabulary.add_window_title_tag('LinkedIn', 'linked_in')
aenea.vocabulary.add_window_title_tag('- Quip', 'quip')


def unload():
    global other_chrome_grammar

    if other_chrome_grammar:
        other_chrome_grammar.unload()

    for tag in other_chrome_finishers_tags:
        aenea.vocabulary.unregister_dynamic_vocabulary(tag)

    other_chrome_grammar = None
