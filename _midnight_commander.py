import aenea.config
import aenea.configuration
import aenea.misc
import aenea.vocabulary

from dragonfly import *

from SharedRules import *
from util import *
from SwapProgram import SwapProgramRule
from SharedGitRules import GitRule, GitRuleNew
from SharedTerminalRules import *
from CommonMappings import common_folders

midnight_commander_context = AppContext(executable='ConEmu64.exe', title = 'mc - ')
midnight_commander_grammar = Grammar('midnight_commander', context=midnight_commander_context)
midnight_commander_tags = ['midnight_commander', 'midnight_commander.count']

common_folders['home'] = '~'



jump_letters_one = {'lay': 0, 'bay': 1, 'may': 2, 'gay': 3, 'ray': 4, }
# jump_letters_one = {'lay': 0, 'bay': 1, 'may': 2, 'gay': 3, 'ray': 4, 'day': 5, 'yay': 6, 'nay': 7, 'way': 8, 'jay': 9}
jump_letters_two = {'low': 0, 'bow': 1, 'mow': 2, 'go': 3, 'rho': 4, }
# jump_letters_two = {'low': 0, 'bow': 1, 'mow': 2, 'go': 3, 'rho': 4, 'dow': 5, 'yo': 6, 'no': 7, 'woe': 8, 'Joe': 9}
jump_letters_three = {'lee': 0, 'bee': 1, 'me': 2, 'ghee': 3, 're': 4, 'dee': 5, 'ye': 6, 'knee': 7, 'wee': 8, 'gee': 9}
jump_letters_four = {'lear': 0, 'beer': 1, 'mere': 2, 'gear': 3, 'rear': 4, 'dear': 5, 'year': 6, 'near': 7, 'we\'re': 8, 'jeer': 9}
jump_letters_five = {'lore': 0, 'bore': 1, 'more': 2, 'gore': 3, 'roar': 4, 'door': 5, 'yore': 6, 'nor': 7, 'wore': 8}
jump_letters_six = {'lie': 0, 'bye': 1, 'my': 2, 'guy': 3, 'rye': 4, 'die': 5, 'aye': 6, 'nigh': 7, 'why': 8, 'jie': 9}

jump_letters_name = {'lame': 0, 'bame': 1, 'maim': 2, 'game': 3, 'raim': 4, 'dame': 5, 'yaim': 6, 'name': 7, 'wame': 8, 'jaim': 9}
# jump_letters_explorer = {'lexecute': 0, 'bexecute': 1, 'mexecute': 2, 'gexecute': 3, 'rexecute': 4, 'dexecute': 5, 'yexecute': 6, 'nexecute': 7, 'wexecute': 8, 'jexecute': 9}


# jump_letters_name = {'l': 0, 'b': 1, 'm': 2, 'g': 3, 'r': 4, 'd': 5, 'y': 6, 'n': 7, 'w': 8, 'j': 9}

# Not a real word: d g ch j v z ch ng y
# Not so bad: t p f l n
# Definitely not: b k th s sh h m w r

# a o ee e u oo ei ai oi ou ur ar or ear are ure i
#
# Just do it: b d g j v m n y w r l
#
#  1   1   1    3            2    1
# low lay lea  lie  loo lar lore lear  lair
# bow bay bee  bye  boo bar bore beer  bare
# mow may me   my   moo mar more mere  mare
# go  gay ghee guy  goo gar gore gear
# rho ray re   rye  Roo     roar rear  rare
# dow day D    die  do      door dear  dare
# yo  yay ye                yore year
# no  nay knee nigh         nor  near  nair
# woe way we   why  woo     wore we're ware
# Joe jay gee           jar      jeer

def JumpLetter1(jl1, letter):
	number = jl1 * 26 + ord(letter) - ord('a')
	# print "number: %d" % number
	# action = Key('a-g,down:%d' % number)
	Key('a-g,down:%d' % number).execute()

def JumpLetter2(jl2, letter):
	JumpLetter1(jl2, letter)

def JumpLetter3(jl3, letter):
	JumpLetter1(jl3, letter)


def JumpLetterName(jlname, letter):
	JumpLetter1(jlname, letter)

def JumpLetterExplorer(jlexplorer, letter):
	JumpLetter1(jlexplorer, letter)

class MidnightCommanderRepeatablesRule(MappingRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('midnight_commander', {
		'<jl1> <letter>': Function(JumpLetter1),
		'sync <jl2> <letter>': Function(JumpLetter2) + Key('c-p'),
		'<jl2> <letter>': Function(JumpLetter2) + Key('enter'),
		'<jl3> <letter>': Function(JumpLetter3) + Key('c-t'),
		'<jlname> <letter>': Function(JumpLetterName) + Key('f9,f,r'),
		# 'open <jl1> <letter>': Function(JumpLetter1) + Text('explorer.exe ') + Key('escape,enter,enter'),


		'sync panels': Key('sa-i'),
		'(switch | swap) panels': Key('f9,c,w'),
		'show other | sync here': Key('c-p'),
		'cancel': Key('escape:2'),
		'back': Key('sa-y'),
		'forward': Key('sa-u'),
		'help': Key('f1'),
		'reload': Key('c-r'),
		'new file': Key('f14'),
		'new init file': Key('f14') + Text('__init__.py') + Key('enter/50,c-s,c-w'),
		'serk | find file': Key('f9,c,f'),
		'rename': Key('f9,f,r'),
		'move': Key('f9,f,r'),
		'copy': Key('f9,f,c'),
		'remove | delete': Key('f9,f,d'),
		'punk <nn>': Key('c-pageup:%(nn)d'),
		'(make | new) (folder | dear)': Key('f9,f,m'),
		'mark <nn>': Key('c-t:%(nn)d'),
		'mark pattern': Key('f9,f,g'),
		'mark all': Key('f9,f,g,star,enter'),
		'unmark all': Key('f9,f,n,star,enter'),
		'copy file name': Text('clip.exe <<< ') + Key('escape,enter,enter'),
		'copy path': Text('pwd | clip.exe\n'),
		'copy (contents | file)': Text('cat ') + Key('escape,enter') + Text(' | clip.exe\n'),
		'copy file path': Text('clip.exe <<< ') + Key('escape,a,escape,enter,enter'),
		'add [current] folder to (lime | sublime)': Text('subl.exe -a .\n'),
	})

	extras = [
		NoCompile(Optional(Integer(min = 0, max = 100), default = 1), name = 'nn'),
		Choice(name = 'jl1', choices = jump_letters_one),
		Choice(name = 'jl2', choices = jump_letters_two),
		Choice(name = 'jl3', choices = jump_letters_three),
		Choice(name = 'jlname', choices = jump_letters_name),
		# Choice(name = 'jlexplorer', choices = jump_letters_explorer),
		NoCompile(Choice(choices = aenea.misc.LETTERS), name = 'letter'),
	]


class MidnightCommanderFinishersRule(MappingCountRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('midnight_commander', {
		'help': Key('f1'),
		'show [term | terminal | console]': Key('c-o'),
		'restart': Key('f10/20,m,c,enter'),
		'execute': Text('/mnt/c/Windows/explorer.exe ') + Key('escape,enter,enter'),
		'open': Key('enter'),
		'run': Text('./') + Key('escape,enter,enter'),
		'view': Key('f9,f,v'),
		'edit | sublime': Key('f9,f,e'),
		'(show | hide) hidden': Key('a-dot'),
		'SSH jingyi': Key('f9,enter,h/2') + Text('joep@jingyi') + Key('enter/50') + Text('cd home/joep\n'),
	})


class ShellGitRule(GitRule):
	def value(self, node):
		return super(ShellGitRule, self).value(node)

class ShellGitRuleNew(GitRuleNew):
	def value(self, node):
		return super(ShellGitRuleNew, self).value(node)

class ShellTerminalQuickFinishersRule(TerminalQuickFinishersRule):
	def value(self, node):
		return super(ShellTerminalQuickFinishersRule, self).value(node)


class MidnightCommanderRule(RepeatRule):
	repeatables = [
		RuleRef(rule=MidnightCommanderRepeatablesRule()),
		RuleRef(rule=TerminalRepeatablesRule()),
		RuleRef(rule = ShellGitRule()),
		RuleRef(rule = ShellGitRuleNew()),
		RuleRef(rule = ChainFormatRule()),
		DictListRef('dynamic terminal', aenea.vocabulary.register_dynamic_vocabulary('terminal')),
	] + CommonRepeatables()
	finishers = [
		RuleRef(rule=MidnightCommanderFinishersRule()),
		RuleRef(rule = FormatRule()),
		RuleRef(rule = ScrollRule()),
		RuleRef(rule = SwapProgramRule()),
		RuleRef(rule=TerminalWindowsCommandsRule()),
		RuleRef(rule=TerminalFinishersRule()),
		RuleRef(rule = ShellTerminalQuickFinishersRule()),
	]


midnight_commander_grammar.add_rule(MidnightCommanderRule())
midnight_commander_grammar.load()

aenea.vocabulary.add_window_executable_tag('ConEmu64.exe', 'terminal')


def unload():
	global midnight_commander_grammar

	if midnight_commander_grammar:
		midnight_commander_grammar.unload()
	midnight_commander_grammar = None
