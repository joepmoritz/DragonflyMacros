# -*- coding: utf-8 -*-
import aenea.config
import aenea.configuration
import aenea.misc
import aenea.vocabulary

from dragonfly import *
# from aenea.strict import *
# from aenea.proxy_contexts import *

from util import *
from SharedRules import *
from SwapProgram import SwapProgramRule
from SharedTerminalRules import TerminalContext
from CommonMappings import common_folders

import string


sublime_context = AppContext(executable='sublime_text') & ~AppContext(title='Save As') & ~AppContext(title='Select Folder')
# sublime_context = AppContext(executable='sublime_text') & ~AppContext(title='Save As') & ~AppContext(title='Select Folder') & ~TerminalContext()
sublime_grammar = Grammar('sublime', context=sublime_context)
sublime_tags = ['sublime', 'sublime_finishers', 'keywords', 'functions']

sublime_repeaters_vocabulary = DictListRef('sublime repeaters', aenea.vocabulary.register_dynamic_vocabulary('sublime'))
sublime_multiples_vocabulary = DictListRef('multiples', aenea.vocabulary.register_dynamic_vocabulary('sublime_multiples'))
sublime_keyword_vocabulary = DictListRef('keyword', aenea.vocabulary.register_dynamic_vocabulary('keywords'))
sublime_function_vocabulary = DictListRef('function', aenea.vocabulary.register_dynamic_vocabulary('functions'))
sublime_finishers_dynamic_vocabulary = DictListRef('sublime finishers', aenea.vocabulary.register_dynamic_vocabulary('sublime_finishers'))


sublime_common_keys_mapping = common_keys_mapping.copy()
sublime_common_keys_mapping['kill <nn>'] = SwitchKey('cs-k:%(nn)d')
sublime_common_keys_mapping['skive <nn>'] = SwitchKey('s-down:%(nn)d')
sublime_common_keys_mapping['chomp <nn>'] = SwitchKey('c-del:%(nn)d')
sublime_common_keys_mapping['smack <nn>'] = SwitchKey('c-backspace:%(nn)d')
sublime_common_keys_mapping['woloof <nn>'] = SwitchKey('c-left:%(nn)d')
sublime_common_keys_mapping['wolipe <nn>'] = SwitchKey('c-right:%(nn)d')
sublime_common_keys_mapping['subloof <nn>'] = SwitchKey('a-left:%(nn)d')
sublime_common_keys_mapping['sublipe <nn>'] = SwitchKey('a-right:%(nn)d')
sublime_common_keys_mapping['sewoloof <nn>'] = SwitchKey('sc-left:%(nn)d')
sublime_common_keys_mapping['sewolipe <nn>'] = SwitchKey('sc-right:%(nn)d')
sublime_common_keys_mapping['sesubloof <nn>'] = SwitchKey('sa-left:%(nn)d')
sublime_common_keys_mapping['sesublipe <nn>'] = SwitchKey('sa-right:%(nn)d')

sublime_symbol_mapping = symbol_mapping.copy()
sublime_symbol_mapping['smote'] = 'squote'
sublime_symbol_mapping['quote'] = 'dquote'
sublime_symbol_mapping['pax'] = 'lparen'
sublime_symbol_mapping['braces'] = 'lbrace'
sublime_symbol_mapping['brackets'] = 'lbracket'
sublime_symbol_mapping['angles'] = 'ac-dot,langle'

sublime_character_mapping = aenea.misc.CHARACTERS.copy()
sublime_character_mapping['smote'] = 'squote'
sublime_character_mapping['quote'] = 'dquote'
sublime_character_mapping['pax'] = 'lparen'
sublime_character_mapping['braces'] = 'lbrace'
sublime_character_mapping['brackets'] = 'lbracket'
sublime_character_mapping['angles'] = 'langle'


class CharacterRule(MappingRule):
    name = "Character mapping"
    exported = False
    mapping = sublime_character_mapping


class PriorityFinishersRule(MappingCountRule):
    exported = False
    mapping = {
        # 'open project [<text>]': Key('cs-n/5,w-up/2,a-p/2,s') + Text('%(text)s'),
    }

def Jeep(char, force_word_start=False):
    if char in string.ascii_lowercase or force_word_start:
        Key('ws-squote').execute()
    else:
        Key('w-squote').execute()
    Key(char).execute()


class FinisherRule(MappingRule):
    exported = False
    mapping = aenea.configuration.make_grammar_commands('sublime', {
        '(open | go to file | open file) [<text>]':         Key('c-p') + Text('%(text)s'),
        'stake as': Key('cs-s'),
        'go to symbol <text>':   Key('cs-r') + Text('%(text)s'),
        'reopen':                Key('cs-t'),
        'surf [<text>]':         Key('c-f') + Text('%(text)s'),
        'jeep <char>':           Function(Jeep),
        'seep <char>':           Key('wc-squote') + Function(Jeep),
        'keep <char>':           Key('wcs-squote') + Function(Jeep),
        'go to line <n>':        Key('c-g') + Text('%(n)d'),
        'go to line':            Key('c-g'),
        'definition | deafy':    Key('f12'),
        'references | revel':    Key('s-f12'),
        'next conflict':         Key('ca-f'),
        'next result':           Key('c-e'),
        'pre result':            Key('cs-e'),
        'keep ours':             Key('ca-o'),
        'keep theirs':           Key('ca-h'),
        'keep ancestor':         Key('ca-a'),
        'list conflict files':   Key('ca-c'),
        'find in files':         Key('cs-f'),
        'toggle wordwrap':       Key('csa-w'),
        'twink clove':           Key('c-pgup,c-w'),
        'trip clove':            Key('c-pgdown,c-w'),
        'teepee <n>':            Key('a-%(n)d'), # w-
        'twink [<n>]':           Key('c-pgup:%(n)d'),
        'trip [<n>]':            Key('c-pgdown:%(n)d'),
        '[go | next] mark':      Key('f2'),
        'pre mark':              Key('s-f2'),
        'split [into] lines':    Key('cs-l'),
        'dictate spar':          Key('s-pgdown,c-c/50,cw-f3/50,c-a,c-v'),
        'duplicate file':        Key('c-a/50,c-c/50,c-n/50,c-v'),
        '(show | hide) sidebar': Key('c-k,c-b'),
        'edit project':          Key('cs-p') + Text('edit project') + Key('enter'),
        'save project':          Key('cs-p') + Text('save project') + Key('enter'),
        'fold all':              Key('c-home,c-k,c-1'),
        'unfold all':            Key('c-k,c-j'),
        'fold this':             Key('sc-lbracket,home'),
        'unfold this':           Key('sc-rbracket,left'),
        'fold <small_n>':        Key('c-k,c-%(small_n)d'),
        'rename file':           Key('cs-p,r,f,enter'),
        'flip file':             Key('ca-up'),
        'new project':           Key('cs-p/3,p/3,m/3,space/3,a/3,d/3,d/3,enter'),
        'rename project':        Key('cs-p/3,p/3,m/3,space/3,r/3,e/3,n/3,p,enter'),
        'remove project':        Key('cs-p/3,p/3,m/3,space/3,r/3,e/3,m/3,p,enter'),
        'import project':        Key('cs-p/3,p/3,m/3,space/3,i/3,m/3,p/3,enter'),
        'term file':             Key('ca-t'),
        'term project':          Key('cas-t'),
        'preview pep 8':         Key('c-8'),
        'auto pep 8':            Key('sc-8'),
    })

    extras = [
        IntegerRef(min=1, max=5, name='small_n'),
        ShortIntegerRef(name='n', min=0, max=10000),
        DictateWords(name='text'),
        RuleRef(name='char', rule=CharacterRule()),
    ]

    defaults = {'n': 1, 'nn': 1}


class SmallSnippetsRule(MappingRule):
    exported = False
    mapping = aenea.configuration.make_grammar_commands('sublime', {
        'snip if':                                       Key('a-i'),
        'snip iffy':                                     Key('a-g'),
        'snip else if':                                  Key('a-l'),
        'snip else':                                     Key('a-s'),
        'snip for':                                      Key('a-f'),
        'snip function':                                 Key('a-d'),
        'snip while':                                    Key('a-w'),
        'snip class':                                    Key('a-c'),
        'snip try':                                      Key('a-y'),
        'snip braces':                                   Key('a-b'),
        'snip comment':                                  Key('a-m'),
        'snip with':                                     Key('a-h'),
        }, 'small_snippets1')


class EditActionsRule(MappingCountRule):
    exported = False
    mapping = aenea.configuration.make_grammar_commands('sublime', {
        'clove':                                    Key('c-w'), # w-w
        'new (file | tab)':                         Key('c-n'),
        'new window':                               Key('sc-n'),
        'go back':                                  Key('w-lbracket'),
        'go forward':                               Key('w-rbracket'),
        'fish':                                     Key('f3'),
        'pre fish | bird':                          Key('s-f3'), # sw-g
        'fox':                                      Key('c-f3'), # w-g
        # 'replace':                                  Key('c-h'),
        # 'replace all':                              Key('ca-enter'),
        'next field':                               Key('backtick'),
        'dope <nn>':                                Key('cs-d:%(nn)d'),
        'stupid dope <nn>':                         Key('wcs-d:%(nn)d'),
        'join lines':                               Key('c-j'),
        'mopup <nn>':                               Key('cs-up:%(nn)d'),
        'modos <nn>':                               Key('cs-down:%(nn)d'),
        'curpup <nn>':                              Key('c-up:%(nn)d'),
        'curdos <nn>':                              Key('c-down:%(nn)d'),
        'comment':                                  Key('c-slash'),
        'uncomment':                                Key('c-slash'),
        'indent <nn>':                              Key('c-rbracket:%(nn)d'),
        'unindent <nn>':                            Key('c-lbracket:%(nn)d'),
        'worm <nn>':                                Key('c-d:%(nn)d'),
        'skip worm':                                Key('c-k,c-d'),
        'skip next worm':                           Key('c-d,c-k,c-d'),
        'worms':                                    Key('ca-d'),
        'make upper | upper case':                  Key('c-k,c-u'),
        'make lower | lower case':                  Key('c-k,c-l'),
        'make title | title case':                  Key('c-k,c-t'),
        'lice <nn>':                                Key('c-enter:%(nn)d'),
        'lice (pup | up) <nn>':                     Key('sc-enter:%(nn)d'),
        'spur <nn>':                                Key('s-pgup:%(nn)d'),
        'spar <nn>':                                Key('s-pgdown:%(nn)d'),
        'stitch':                                   Key('cwa-i'),
        'stouch':                                   Key('cwa-d'),
        'swap quotes':                              Key('cwa-q'),
        'swap brackets':                            Key('cwa-e'),
        'remove brackets':                          Key('cwa-r'),
        'show console':                             Key('c-backtick'),
        'auto align':                               Key('cs-p') + Text('aligntablpm') +              Key('enter/100') + Text('/l(lu)*5') + Key('home'),
        # 'stark':                                    Key('cwa-a'),
        # 'lark | leet ark':                          Key('cwa-a,delete'),
        # '(nark | add ark) [after]':                 Key('cwa-a,right,comma,space'),
        # '(nark | add ark) before':                  Key('cwa-a,left:2,comma,left,space'),
        # 'test action <nn>':                       Key('enter') * Repeat(count = -1, extra = "nn"),

        '[set | toggle] mark': Key('c-f2'),
        '[see | stick] marks': Key('a-f2'),
        'clear marks': Key('ac-f2'),
        }, 'edit_actions')


# This should use only the current file keywords
quick_jump_keys = NoCompile(Choice(None, choices=aenea.misc.CHARACTERS), name = 'what')
quick_jump_keywords = NoCompile(sublime_repeaters_vocabulary, name = 'what')
quick_jump_rule = Alternative(
    children=[
        # Compound('bird <what>', [quick_jump_keys], value_func = lambda n, e: Key('left,c-f,del,%s,escape,sw-g,left' % e['what'])),
        Compound('bird <what>', [quick_jump_keys], value_func = lambda n, e: Key('left,c-f,del,%s,escape,s-f3,left' % e['what'])),
        # Compound('fox <what>', [quick_jump_keywords], value_func = lambda n, e: Key('c-f') + e['what'] + Key('enter')),
        Compound('fox <what>', [quick_jump_keys], value_func = lambda n, e: Key('right,c-f,del,%s,escape,left' % e['what'])),
    ])


keyword_value_function = lambda n, e: Key('sw-semicolon') + e['keyword'] + Key('enter/10')
keyword_rule = Compound('key <keyword>', [sublime_keyword_vocabulary], value_func = keyword_value_function)

function_value_function = lambda n, e: Key('cw-semicolon') + e['function'] + Key('enter/10')
function_rule = Compound('<function>', [sublime_function_vocabulary], value_func = function_value_function)

multiples_function = lambda n, e: e['multiples'] * e['n']
short_integer = ShortIntegerRef(name='n', min=1, max=10, default=1)
multiples_rule = Compound('<multiples> [<n>]', [sublime_multiples_vocabulary, short_integer], value_func=multiples_function)


# class SublimeFormatRule(FormatRule):
#     def value(self, node):
#         text = FormatRule.value(self, node)
#         return Key('wa-n') + text + Key('wa-u')

sublime_format_rule = FormatRule()
function_format_value_func = lambda n, e: Key('cw-semicolon') + e['txt'] + Key('enter/10')
function_format_rule = Compound('func <txt>', [RuleRef(rule=sublime_format_rule, name='txt')], value_func=function_format_value_func)

method_format_value_func = lambda n, e: Key('cw-semicolon,dot') + e['txt'] + Key('enter/10')
method_format_rule = Compound('met <txt>', [RuleRef(rule=sublime_format_rule, name='txt')], value_func=method_format_value_func)


# Browse common folders
browse_folder_mapping = {
    'browse ' + f['speech']: Key('c-m,c-d,s-home,del') + Text(f['path_win'] + '\n') for f in common_folders
}
browse_common_folder_rule = Choice(choices=browse_folder_mapping, name=None)

class SublimeRepeatRule(RepeatRule):
    repeatables = [
        quick_jump_rule,
        sublime_repeaters_vocabulary,
        multiples_rule,
        keyword_rule,
        function_rule,
        RuleRef(rule=EditActionsRule()),
        RuleRef(rule=SymbolRule(mapping=sublime_symbol_mapping)),
        RuleRef(rule=SmallSnippetsRule()),
        RuleRef(rule=NumberRule()),
        RuleRef(rule=LetterRule()),
        RuleRef(rule=CommonKeysRule(mapping=sublime_common_keys_mapping)),
        # RuleRef(rule = MouseRule()),
        RuleRef(rule = ChainFormatRule()),
    ]
    finishers = [
        # RuleRef(rule =PriorityFinishersRule()),
        browse_common_folder_rule,
        sublime_finishers_dynamic_vocabulary,
        function_format_rule,
        method_format_rule,
        RuleRef(rule=sublime_format_rule),
        RuleRef(rule=FinisherRule(), name='finisher'),
        RuleRef(rule=ScrollRule()),
        RuleRef(rule=WindowsRule()),
        RuleRef(rule = SwapProgramRule()),
    ]


sublime_grammar.add_rule(SublimeRepeatRule(name = 'main_repeat_rule'))
sublime_grammar.load()


# class DictationRule(MappingRule):
#     mapping = aenea.configuration.make_grammar_commands('sublime', {
#         '<text>': Text('%(text)s'),
#     })
#     extras = [Dictation(name='text')]
# dictRule = RuleRef(name = 'text', rule = DictationRule())

# sublime_dictation_grammar.add_rule(DictationRule())
# sublime_dictation_grammar.load()


aenea.vocabulary.add_window_title_tag('.py', 'python_file')
aenea.vocabulary.add_window_title_tag('.c', 'cpp_file')
aenea.vocabulary.add_window_title_tag('.cpp', 'cpp_file')
aenea.vocabulary.add_window_title_tag('.h', 'cpp_file')
aenea.vocabulary.add_window_title_tag('.ipp', 'cpp_file')
aenea.vocabulary.add_window_title_tag('.hpp', 'cpp_file')
aenea.vocabulary.add_window_title_tag('.m', 'matlab_file')
aenea.vocabulary.add_window_title_tag('.json', 'json_file')
aenea.vocabulary.add_window_title_tag('.sublime-keymap', 'json_file')
aenea.vocabulary.add_window_title_tag('.sublime-settings', 'json_file')
aenea.vocabulary.add_window_title_tag('.sublime-project', 'json_file')
aenea.vocabulary.add_window_title_tag('.tex', 'latex_file')
aenea.vocabulary.add_window_title_tag('.js', 'js_file')
aenea.vocabulary.add_window_title_tag('.lua', 'lua_file')
aenea.vocabulary.add_window_title_tag(u'(DragonWords)', 'sublime_addon')
aenea.vocabulary.add_window_title_tag(u'(Terminus)', 'sublime_addon')
aenea.vocabulary.add_window_title_tag(u'(SublimeFileBrowser)', 'sublime_addon')
aenea.vocabulary.add_window_title_tag(u'(CleverCoder)', 'sublime_addon')
aenea.vocabulary.add_window_title_tag(u'𝌆', 'sublime_file_browser')
aenea.vocabulary.add_window_title_tag(u'[=]', 'sublime_file_browser')
# aenea.vocabulary.add_window_title_tag(WINDOW_TITLE_IDENTIFIER, 'sublime_terminus')



def unload():
    global sublime_grammar

    for tag in sublime_tags:
        aenea.vocabulary.unregister_dynamic_vocabulary(tag)

    if sublime_grammar:
        sublime_grammar.unload()

    sublime_grammar = None


