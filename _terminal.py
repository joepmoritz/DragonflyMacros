import aenea.config
import aenea.configuration
import aenea.misc
import aenea.vocabulary

from dragonfly import *

from SharedTerminalRules import *
from util import *
from SharedRules import *
from SwapProgram import SwapProgramRule
from SharedGitRules import GitRule, GitRuleNew

midnight_commander_context = AppContext(executable='ConEmu64.exe', title = 'mc - ')
other_terminal_context = TerminalContext() & ~midnight_commander_context
terminal_grammar = Grammar('terminal', context=other_terminal_context)



list_choices = {'all': '-a', 'long': '-l'}


class OtherTerminalRepeatablesRule(MappingRule):
    exported = False
    mapping = aenea.configuration.make_grammar_commands('terminal', {
        'list [<ls_opt>]':                   Text('ls %(ls_opt)s') + Key('enter'),
        'dear':                        Text('cd '),
        'punk <nn>':                         Text('cd ..\n') * Repeat(extra = "nn"),
        'dodo <nn>':                         Text('../') * Repeat(extra = "nn"),
        'stab':        Key('tab,enter'),
        'break':      Key('c-c'),
        '<terminal_words>': Text(' %(terminal_words)s', pause = 0),

        'move': Text('mv '),
        'M V': Text('mv '),
        'make dear': Text('mkdir '),
        'M K dear': Text('mkdir '),
        'remove': Text('rm '),
        'remove recurse': Text('rm -rf '),
        'remove dear': Text('rmdir '),
        'make link': Text('ln -s '),
        'C H own': Text('chown '),
        'change owner': Text('chown '),
        'C H group': Text('chgrp '),
        'change group': Text('chgrp '),
        'C H mod': Text('chmod '),
        'change mod': Text('chmod '),

    })

    extras = [
        Repetition(Choice(choices = list_choices), name='ls_opt', joinWith=' ', min=0, max=2),
        NoCompile(Optional(Integer(min = 1, max = 100), default = 1), name = 'nn'),
        Choice(name = 'terminal_words', choices = common_terminal_words),
    ]
    defaults = {'nn': 1}




class OtherTerminalFinishersRule(MappingCountRule):
    exported = False
    mapping = aenea.configuration.make_grammar_commands('midnight_commander', {
        # 'mid com': Text('mc\n'),
        # 'SSH jingyi': Text('ssh joep@jingyi') + Key('enter/50') + Text('source activate py27\ncd psgan\n'),
        'sublime here': Text('subl.exe .\n'),
        # 'sync spatial gan': Key('w-1/10') + Text('rsync -av /mnt/d/MyDocuments/Skin/special_gan joep@jingyi:~/\n', pause = 0),
    })


class TerminalRule(RepeatRule):
    repeatables = [
        RuleRef(rule=TerminalRepeatablesRule()),
        RuleRef(rule= OtherTerminalRepeatablesRule()),
        DictListRef('dynamic terminal', aenea.vocabulary.register_dynamic_vocabulary('terminal')),
        RuleRef(rule = GitRule()),
        RuleRef(rule = GitRuleNew()),
        RuleRef(rule = ChainFormatRule()),
    ] + CommonRepeatables()
    finishers = [
        RuleRef(rule=OtherTerminalFinishersRule()),
        RuleRef(rule=TerminalWindowsCommandsRule()),
        RuleRef(rule=TerminalFinishersRule()),
        RuleRef(rule =TerminalQuickFinishersRule()),
        RuleRef(rule = FormatRule()),
        RuleRef(rule = ScrollRule()),
        RuleRef(rule = SwapProgramRule()),
    ]


terminal_grammar.add_rule(TerminalRule())
terminal_grammar.load()

aenea.vocabulary.add_window_executable_tag('ConEmu64.exe', 'terminal')


def unload():
    global terminal_grammar
    
    if terminal_grammar:
        terminal_grammar.unload()
    terminal_grammar = None



