import aenea.config
import aenea.configuration
import aenea.misc
import aenea.vocabulary

from dragonfly import *
from dragonfly import Key as DragonKey
# from aenea.strict import *
# from aenea.proxy_contexts import *

from SharedRules import *
from SwapProgram import command_mode


# notepad_context = ProxyAppContext(executable='WinAppHelper') & AppContext(executable='notepad.exe')
notepad_context = AppContext(executable='notepad.exe')

notepad_grammar = Grammar('notepad', context=notepad_context)


class NotepadRepeatablesRule(MappingCountRule):
    mapping = aenea.configuration.make_grammar_commands('notepad', {
        # 'transfer that': DragonKey('c-a/3,c-c/3') + Pause('10') + Key('cwas-r') + Pause('50') + Key('w-v'),
        'transfer that': Key('c-a/3,c-c/3,cws-f3/50,c-v') + command_mode,
        'commit now': Key('c-s/5,cws-f3/50') + Text('git commit -F ~/.GIT_COMMIT_MSG') + Key('enter') + command_mode,
        'commit amend now': Key('c-s/5,cws-f3/50') + Text('git commit -F --amend ~/.GIT_COMMIT_MSG') + Key('enter') + command_mode,
        'word wrap': DragonKey('a-o/50,w'),
        'undo': DragonKey('c-z'),
    })


class NotepadRule(RepeatRule):
    repeatables = [
        RuleRef(rule=NotepadRepeatablesRule()),
        # DictListRef('dynamic notepad', aenea.vocabulary.register_dynamic_vocabulary('notepad')),
        RuleRef(rule=NumberRule(map_func=DragonKey)),
        RuleRef(rule=LetterRule(map_func=DragonKey)),
        RuleRef(rule=SymbolRule(map_func=DragonKey)),
        RuleRef(rule=CommonKeysRule(map_func=DragonKey)),
    ]
    finishers = [
        RuleRef(rule=FormatRule(map_func=DragonText)),
        RuleRef(rule=WindowsRule(map_func=DragonKey)),
        RuleRef(rule=ScrollRule()),
        RuleRef(rule=SwapProgramRule()),
    ]


notepad_grammar.add_rule(NotepadRule())

notepad_grammar.load()


def unload():
    global notepad_grammar

    aenea.vocabulary.unregister_dynamic_vocabulary('notepad')

    if notepad_grammar:
        notepad_grammar.unload()
    notepad_grammar = None
