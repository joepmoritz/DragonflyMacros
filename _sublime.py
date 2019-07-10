import aenea.config
import aenea.configuration
import aenea.misc
import aenea.vocabulary

from dragonfly import *

from util import *
from SharedRules import *
from SwapProgram import SwapProgramRule



sublime_context = AppContext(executable='sublime') & AppContext(title ='Save As', exclude = True) & AppContext(title ='Select Folder', exclude = True)
sublime_grammar = Grammar('sublime', context=sublime_context)
sublime_tags = ['sublime', 'sublime_finishers', 'keywords', 'functions']

sublime_dynamic_vocabulary = DictListRef('sublime repeaters', aenea.vocabulary.register_dynamic_vocabulary('sublime'))
sublime_keyword_vocabulary = DictListRef('keyword', aenea.vocabulary.register_dynamic_vocabulary('keywords'))
sublime_function_vocabulary = DictListRef('function', aenea.vocabulary.register_dynamic_vocabulary('functions'))
sublime_finishers_dynamic_vocabulary = DictListRef('sublime finishers', aenea.vocabulary.register_dynamic_vocabulary('sublime_finishers'))




sublime_common_keys_mapping = common_keys_mapping.copy()
sublime_common_keys_mapping['grip <nn>'] = Key('pgup/10:%(nn)d/0,c-k/0,c-c')
sublime_common_keys_mapping['drop <nn>'] = Key('pgdown/10:%(nn)d/0,c-k/0,c-c')
sublime_common_keys_mapping['kill <nn>'] = Key('cs-k:%(nn)d')
sublime_common_keys_mapping['skive <nn>'] = Key('s-down:%(nn)d')
sublime_common_keys_mapping['chomp <nn>'] = Key('c-del:%(nn)d')
sublime_common_keys_mapping['smack <nn>'] = Key('c-backspace:%(nn)d')
# 'smack <nn>':                        Key('sc-left:%(nn)d, del')

sublime_symbol_mapping = symbol_mapping.copy()
sublime_symbol_mapping['smote'] = Key('c-squote')
sublime_symbol_mapping['quote'] = Key('c-dquote')
sublime_symbol_mapping['pax'] = Key('c-lparen')
sublime_symbol_mapping['braces'] = Key('c-lbrace')
sublime_symbol_mapping['brax'] = Key('c-lbracket')
sublime_symbol_mapping['angles'] = Key('c-langle')

sublime_character_mapping = aenea.misc.CHARACTERS.copy()
sublime_character_mapping['smote'] = 'squote'
sublime_character_mapping['quote'] = 'dquote'
sublime_character_mapping['pax'] = 'lparen'
sublime_character_mapping['braces'] = 'lbrace'
sublime_character_mapping['brax'] = 'lbracket'
sublime_character_mapping['angles'] = 'langle'


class CharacterRule(MappingRule):
    name="Character mapping"
    exported=False
    mapping=sublime_character_mapping


class PriorityFinishersRule(MappingCountRule):
    exported = False
    mapping = {
        'open project [<text>]': Key('cs-n/5,w-up/2,a-p/2,s') + Text('%(text)s'),
    }

class FinisherRule(MappingRule):
    exported = False
    mapping = aenea.configuration.make_grammar_commands('sublime', {
        'open [<text>]':       Key('c-p') + Text('%(text)s'),
        'go to symbol <text>': Key('cs-r') + Text('%(text)s'),
        'reopen':              Key('cs-t'),
        'serk [<text>]':       Key('c-f') + Text('%(text)s'),
        'jeep <char>':         Key('c-semicolon,%(char)s'),
        'seep <char>':         Key('cs-semicolon,%(char)s'),
        'go to line <n>':      Key('c-g') + Text('%(n)d'),
        'go to line':          Key('c-g'),
        'definition | deafy':  Key('f12'),
        'next conflict':       Key('ca-f'),
        'next result':         Key('c-e'),
        'pre result':          Key('cs-e'),
        'keep ours':           Key('ca-o'),
        'keep theirs':         Key('ca-t'),
        'keep ancestor':       Key('ca-a'),
        'list conflict files': Key('ca-c'),
        'find in files':       Key('cs-f'),
        'toggle wordwrap':     Key('csa-w'),
        'twink clove':         Key('c-pgup,c-w'),
        'trip clove':          Key('c-pgdown,c-w'),
        'teepee <n>':          Key('a-%(n)d'),
        'twink [<n>]':         Key('c-pgup:%(n)d'),
        'trip [<n>]':          Key('c-pgdown:%(n)d'),
        '[go | next] mark':    Key('f2'),
        'pre mark':            Key('s-f2'),
        'split [into] lines':  Key('cs-l'),
        'dictate spar':        Key('s-pgdown,c-c/50,cw-f3/50,c-a,c-v'),
        'duplicate file':      Key('c-a/50,c-c,c-n/50,c-v'),
        'show sidebar':        Key('c-k,c-b'),
        'save project':        Key('a-p/2,a,enter'),
        'edit project':        Key('a-p/2,down:6,enter'),
        'exit':                Key('a-e,left,x'),
        'fold all':            Key('c-home,c-k,c-1'),
        'unfold all':          Key('c-k,c-j'),
        'fold this':           Key('sc-lbracket,home'),
        'unfold this':         Key('sc-rbracket,right'),
        'fold <small_n>':      Key('c-k,c-%(small_n)d'),
        'rename file':         Key('cs-p,r,f,enter'),
    })

    extras = [
        Integer(min = 1, max = 5, name = 'small_n'),
        DictInteger(name = 'n'),
        DictateWords(name = 'text'),
        RuleRef(name='char', rule=CharacterRule()),
    ]

    defaults = {'n': 1, 'nn': 1}



class SmallSnippetsRule(MappingRule):
    exported = False
    mapping = aenea.configuration.make_grammar_commands('sublime', {
        'snip iffy':                                     Key('a-i'),
        'snip if':                                       Key('a-g'),
        'snip for':                                      Key('a-f'),
        'snip else if':                                  Key('a-l'),
        'snip else':                                     Key('a-e'),
        'snip while':                                    Key('a-w'),
        'snip function':                                 Key('a-d'),
        'snip class':                                    Key('a-c'),
        'snip try':                                      Key('a-y'),
        }, 'small_snippets1')

class EditActionsRule(MappingCountRule):
    exported = False
    mapping = aenea.configuration.make_grammar_commands('sublime', {
        'new (file | tab)' :                        Key('c-n'),
        'new window' :                              Key('sc-n'),
        'go back':                                  Key('a-minus'),
        'go forward':                               Key('as-minus'),
        'fish':                                     Key('f3'),
        'pre fish | bird':                          Key('s-f3'),
        'fox':                                      Key('c-f3'),
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
        'indent <nn>':                              Key('numpad3:%(nn)d'),
        'unindent <nn>':                            Key('numpad1:%(nn)d'),
        'worm <nn>':                                Key('c-d:%(nn)d'),
        'skip worm':                                Key('c-k,c-d'),
        'skip next worm':                           Key('c-d,c-k,c-d'),
        'worms':                                    Key('ca-d'),
        # 'make upper | upper case':                Key('c-k') + Pause("1") +                        Key('c-u'),
        # 'make lower | lower case':                Key('c-k') + Pause("1") +                        Key('c-l'),
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
quick_jump_keys = NoCompile(Choice(choices = aenea.misc.CHARACTERS), name = 'what')
quick_jump_keywords = NoCompile(sublime_dynamic_vocabulary, name = 'what')
quick_jump_rule = Alternative(
    children = [
        # Compound('bird <what>', [quick_jump_keywords], value_func = lambda n, e: Key('c-f') + e['what'] + Key('s-f3,enter')),
        # Compound('fox <what>', [quick_jump_keywords], value_func = lambda n, e: Key('c-f') + e['what'] + Key('enter')),
        Compound('bird <what>', [quick_jump_keys], value_func = lambda n, e: Key('c-semicolon,%s,a' % e['what'])),
        Compound('fox <what>', [quick_jump_keys], value_func = lambda n, e: Key('c-semicolon,%s,b' % e['what'])),
    ])


keyword_value_function = lambda n, e: Key('sw-semicolon') + e['keyword'] + Key('enter/10')
keyword_rule = Compound('key <keyword>', [sublime_keyword_vocabulary], value_func = keyword_value_function)

function_value_function = lambda n, e: Key('cw-semicolon') + e['function'] + Key('enter/10')
function_rule = Compound('<function>', [sublime_function_vocabulary], value_func = function_value_function)


class SublimeFormatRule(FormatRule):
    def value(self, node):
        text = FormatRule.value(self, node)
        return Key('wa-n') + text + Key('wa-u')

function_format_value_func = lambda n, e: Key('cw-semicolon') + e['format'] + Key('enter/10')
function_format_rule = Compound('func <format>', [RuleRef(rule = SublimeFormatRule(name = '123'), name = 'format')], value_func = function_format_value_func)

class SublimeRepeatRule(RepeatRule):
    repeatables = [
        quick_jump_rule,
        sublime_dynamic_vocabulary,
        keyword_rule,
        function_rule,
        RuleRef(rule=EditActionsRule()),
        RuleRef(rule=MappingRule(exported = False, mapping = sublime_symbol_mapping)),
        RuleRef(rule=SmallSnippetsRule()),
        RuleRef(rule=NumberRule()),
        RuleRef(rule=LetterRule()),
        RuleRef(rule= MappingCountRule(exported = False, mapping = sublime_common_keys_mapping)),
        # RuleRef(rule = MouseRule()),
        RuleRef(rule = ChainFormatRule()),
    ]
    finishers = [
        RuleRef(rule =PriorityFinishersRule()),
        sublime_finishers_dynamic_vocabulary,
        function_format_rule,
        RuleRef(rule=SublimeFormatRule()),
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
aenea.vocabulary.add_window_title_tag('.m', 'matlab_file')
aenea.vocabulary.add_window_title_tag('.json', 'json_file')
aenea.vocabulary.add_window_title_tag('.tex', 'latex_file')
aenea.vocabulary.add_window_title_tag('.js', 'js_file')
aenea.vocabulary.add_window_title_tag('(SpeechCoding)', 'sublime_addon')



def unload():
    global sublime_grammar

    for tag in sublime_tags:
        aenea.vocabulary.unregister_dynamic_vocabulary(tag)

    if sublime_grammar:
        sublime_grammar.unload()

    sublime_grammar = None


