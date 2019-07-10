import aenea.config
import aenea.configuration

from dragonfly import *

from SharedRules import *
from util import *
from SharedChromeRules import SharedChromeRepeatablesRule, SharedChromeFinishersRule


inbox_context = AppContext(executable='Chrome', title ='joep.moritz@gmail.com')
sheets_context = AppContext(executable='Chrome', title ='Google Sheets')
keep_context = AppContext(executable='Chrome', title ='Google Keep')
outlookweb_context = AppContext(executable='Chrome', title ='Mail - joep.moritz.13@ucl.ac.uk - Google Chrome')
chrome_context = AppContext(executable='Chrome')

other_chrome_context = chrome_context & ~inbox_context & ~outlookweb_context & ~sheets_context & ~keep_context
other_chrome_grammar = Grammar('chrome', context=other_chrome_context)
other_chrome_finishers_tags = ['other_chrome_finishers']



class OtherChromeRepeatablesRule(MappingCountRule):
    mapping = {
        'address [bar]': Key('a-d'),
        'top frame':     Key('g,s-f'),
        'next frame':    Key('g,f'),
        'add bookmark':  Key('c-d'),
        'copy address':  Key('a-d,c-c'),
        'open':          Key('enter'),
        'input':         Key('g,i'),
    }


class OtherChromeFinishersRule(MappingCountRule):
    mapping = aenea.configuration.make_grammar_commands('chrome', {
        'next':                              Key('rbracket') + Key('rbracket'),
        'pre':                               Key('lbracket') + Key('lbracket'),
        'back <nn>':                         Key('a-left:%(nn)d'),
        'forward <nn>':                      Key('a-right:%(nn)d'),
        'fish | serk [<text>]':   Key('c-f') + Text('%(text)s'),
    })



class OtherChromeRule(RepeatRule):
    repeatables = [
        RuleRef(rule=OtherChromeRepeatablesRule()),
        RuleRef(rule=SharedChromeRepeatablesRule()),
    ] + CommonRepeatables()
    finishers = [
        RuleRef(rule=OtherChromeFinishersRule()),
        RuleRef(rule=SharedChromeFinishersRule()),
        DictListRef('dynamic other chrome finishers', aenea.vocabulary.register_dynamic_vocabulary('other_chrome_finishers')),
    ] + CommonFinishers()




# other_chrome_grammar.add_rule(finishLinkRule)
other_chrome_grammar.add_rule(OtherChromeRule())
# other_chrome_grammar.add_rule(AllTabsChromeRule())
other_chrome_grammar.load()

aenea.vocabulary.add_window_title_tag('Overleaf', 'latex_file')
aenea.vocabulary.add_window_title_tag('LinkedIn', 'linked_in')


def unload():
    global other_chrome_grammar

    if other_chrome_grammar:
        other_chrome_grammar.unload()

    for tag in other_chrome_finishers_tags:
        aenea.vocabulary.unregister_dynamic_vocabulary(tag)

    other_chrome_grammar = None
