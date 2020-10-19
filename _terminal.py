import aenea.config
import aenea.configuration
import aenea.vocabulary

from dragonfly import *
# from aenea.strict import *

from SharedTerminalRules import *
from util import *
from SharedRules import *
from SwapProgram import SwapProgramRule
from SharedGitRules import GitRule, GitRuleNew

terminal_context = TerminalContext()
terminal_grammar = Grammar('terminal', context=terminal_context)



list_choices = {'all': '-a', 'long': '-l', 'latest': '-tr'}


class OtherTerminalRepeatablesRule(MappingRule):
    exported = False
    mapping = aenea.configuration.make_grammar_commands('terminal', {
        # 'list [<ls_opt>]':                   Text('l %(ls_opt)s') + Key('enter'),
        '[long] list': Key('l,enter'),
        'quick list': Key('l,s,enter'),
        # 'dear':                        Text('cd '),
        'punk <nn>':                         Key('dot,dot:%(nn)d,enter'),
        'dodo <nn>':                         Text('../') * Repeat(extra = "nn"),
        # 'stab':        Key('tab,enter'),
        'break':      Key('c-c'),
        # '<terminal_words>': Text('%(terminal_words)s', pause = 0),

        'move': Text('mv '),
        'M V': Text('mv '),
        'make dear': Text('mkd '),
        'M K dear': Text('mkd '),
        'remove recurse': Text('rm -rf '),
        'remove dear': Text('rmdir '),
        'remove': Text('rm '),
        'make link': Text('ln -s '),
        'symlink': Text('ln -s '),
        'C H own': Text('chown '),
        'change owner': Text('chown '),
        'C H group': Text('chgrp '),
        'change group': Text('chgrp '),
        'C H mod': Text('chmod '),
        'change mod': Text('chmod '),

        '[create | go] branch [<dash_word_text>]': Text('g go jm/%(dash_word_text)s'),
        'check out branch [<dash_word_text>]': Text('gco jm/%(dash_word_text)s'),
        'show commit <nn>': Text('gsi %(nn)d'),
    })

    extras = [
        JoinList(Repetition(Choice(None, choices = list_choices), name='ls_opt', min=0, max=2)),
        NoCompile(Optional(Integer(min = 1, max = 100), default = 1), name = 'nn'),
        Choice(name='terminal_words', choices=common_terminal_words),
        Dictation(name='dash_word_text').lower().replace(" ", "-"),
    ]
    defaults = {'nn': 1, 'dash_word_text': ''}




class OtherTerminalFinishersRule(MappingCountRule):
    exported = False
    mapping = aenea.configuration.make_grammar_commands('terminal_finishers', {
        'sublime here': Text('subl.exe .\n'),
    })


class TerminalRule(RepeatRule):
    repeatables = [
        RuleRef(rule=TerminalRepeatablesRule()),
        RuleRef(rule= OtherTerminalRepeatablesRule()),
        DictListRef('dynamic terminal', aenea.vocabulary.register_dynamic_vocabulary('terminal_repeaters')),
        # RuleRef(rule = GitRule()),
        # RuleRef(rule = GitRuleNew()),
        RuleRef(rule = ChainFormatRule()),
    ] + CommonRepeatables()
    finishers = [
        DictListRef('dynamic terminal', aenea.vocabulary.register_dynamic_vocabulary('terminal_finishers')),
        RuleRef(rule=OtherTerminalFinishersRule()),
        # RuleRef(rule=TerminalFinishersRule()),
        # RuleRef(rule=TerminalQuickFinishersRule()),
    ] + CommonFinishers()


terminal_grammar.add_rule(TerminalRule())
terminal_grammar.load()



def unload():
    global terminal_grammar
    
    if terminal_grammar:
        terminal_grammar.unload()
    terminal_grammar = None



