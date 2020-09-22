from dragonfly import Key, Text, Function, Optional, Choice, Integer, Pause
from dragonfly.windows.clipboard import Clipboard
# from aenea.strict import *
from dragonfly import Key as DragonKey, Text as DragonText

import aenea.config
import aenea.configuration

from util import MappingCountRule, NoCompile

hint_first_letters = ['l', 'm', 'r', 't', 's', 'g', 'y', 'f', 'j', 'sl', 'fl', 'gl', 'br', 'st', 'tr', 'cr']
jump_letters_direct = {fl + 'o': i for i, fl in enumerate(hint_first_letters)}
jump_letters_new_tab = {fl + 'ee': i for i, fl in enumerate(hint_first_letters)}
jump_letters_hover = {fl + 'ay': i for i, fl in enumerate(hint_first_letters)}
jump_letters_copy_url = {fl + 'op': i for i, fl in enumerate(hint_first_letters)}
jump_letters_copy_text = {fl + 'oppy': i for i, fl in enumerate(hint_first_letters)}

def change(d, old, new):
	d[new] = d[old]
	del d[old]

# jump_letters_direct['poe'] = jump_letters_direct['po']
# jump_letters_direct['poh'] = jump_letters_direct['po']
# jump_letters_direct['pow'] = jump_letters_direct['po']
change(jump_letters_direct, 'to', 'toe')
change(jump_letters_new_tab, 'mee', 'me')
change(jump_letters_new_tab, 'ree', 're')



def SendCommandToClickByVoice(command):
	action = Key('ws-space') + Pause('20') + Text(command) + Key('enter')
	action.execute()

def SendCommandToClickByVoiceDragon(command):
	def go():
		temporary = Clipboard({Clipboard.format_text: command})
		temporary.copy_to_system()
		DragonKey('cs-dot/100').execute()

	try:
		original = Clipboard(from_system=True)
		go()
		original.copy_to_system()
	except Exception as e:
		go()

def ActivateLink(jl_direct, letter):
	SendCommandToClickByVoiceDragon(hint_first_letters[jl_direct] + letter)

def ActivateLinkNewTab(jl_new_tab, letter):
	ActivateLink(jl_new_tab, letter + ':b')

def ActivateLinkHover(jl_hover, letter):
	ActivateLink(jl_hover, letter + ':h')

def ActivateLinkCopyUrl(jl_copy_url, letter):
	ActivateLink(jl_copy_url, letter + ':k')

def ActivateLinkCopyText(jl_copy_text, letter):
	ActivateLink(jl_copy_text, letter + ':s')

class SharedChromeRepeatablesRule(MappingCountRule):
	mapping = aenea.configuration.make_grammar_commands('chrome', {
		'<jl_direct> <letter>':     Function(ActivateLink),
		'<jl_new_tab> <letter>':    Function(ActivateLinkNewTab),
		'<jl_hover> <letter>':      Function(ActivateLinkHover),
		'<jl_copy_url> <letter>':   Function(ActivateLinkCopyUrl),
		'<jl_copy_text> <letter>':  Function(ActivateLinkCopyText),
		
		'"new tab"':                DragonKey('c-t'),
		'new window':               DragonKey('c-n'),
		'new incognito':            DragonKey('cs-n'),
		'teepee <nn>':              DragonKey('c-%(nn)d'),
		'teepee back':              DragonKey('caret'),
		'twink <nn>':               DragonKey('cs-tab:%(nn)d'),
		'trip <nn>':                DragonKey('c-tab:%(nn)d'),
		'steak' :                   DragonKey('c-s'),
		'stop' :                    DragonKey('w-dot'),
		'print' :                   DragonKey('c-p'),
		'zoom in <nn>':             DragonKey('c-plus:%(nn)d'),
		'zoom out <nn>':            DragonKey('c-minus:%(nn)d'),
		'zoom reset':               DragonKey('c-0'),
		# 'links':                    DragonKey('c-m'),
		# 'tinks':                    DragonKey('c-k'),
		# 'multi links':              DragonKey('a-f'),
		# 'copy link URL':            DragonKey('y,f'),
		'reload | refresh':         DragonKey('c-r'),
		# 'duplicate tab | dope tab': DragonKey('y,t'),
		# '(pin | unpin) tab':        DragonKey('a-p'),
		# 'move tab left':            DragonKey('langle, langle'),
		# 'move tab right':           DragonKey('rangle, rangle'),
		# '"new tab"':                Key('w-t'),
		# 'new window':               Key('w-n'),
		# 'new incognito':            Key('ws-n'),
		# 'teepee <nn>':              Key('w-%(nn)d'),
		# 'teepee back':              Key('caret'),
		# 'twink <nn>':               Key('cs-tab:%(nn)d'),
		# 'trip <nn>':                Key('c-tab:%(nn)d'),
		# 'steak' :                   Key('w-s'),
		# 'stop' :                    Key('w-dot'),
		# 'print' :                   Key('w-p'),
		# 'zoom in <nn>':             Key('w-plus:%(nn)d'),
		# 'zoom out <nn>':            Key('w-minus:%(nn)d'),
		# 'links':                    Key('c-m'),
		# 'tinks':                    Key('c-k'),
		# 'multi links':              Key('a-f'),
		# 'copy link URL':            Key('y,f'),
		# 'reload | refresh':         Key('w-r'),
		# 'duplicate tab | dope tab': Key('y,t'),
		# '(pin | unpin) tab':        Key('a-p'),
		# 'move tab left':            Key('langle, langle'),
		# 'move tab right':           Key('rangle, rangle'),
	})

	extras = [
		NoCompile(Optional(Integer(min = 0, max = 100), default = 1), name = 'nn'),
		Choice(name = 'jl_direct', choices = jump_letters_direct),
		Choice(name = 'jl_new_tab', choices = jump_letters_new_tab),
		Choice(name = 'jl_hover', choices = jump_letters_hover),
		Choice(name = 'jl_copy_url', choices = jump_letters_copy_url),
		Choice(name = 'jl_copy_text', choices = jump_letters_copy_text),
		Choice(choices = aenea.misc.LETTERS, name = 'letter'),
	]


class SharedChromeFinishersRule(MappingCountRule):
	mapping = aenea.configuration.make_grammar_commands('chrome', {
		'reopen <nn>':        DragonKey('cs-t:%(nn)d'),
		'history':            DragonKey('c-h'),
		# 'settings':           DragonKey('c-comma'),
		'downloads':          DragonKey('c-j'),
		'[manage] bookmarks': DragonKey('cs-o'),
		'developer tools':    DragonKey('cs-i'),
		'select element':     DragonKey('cs-c'),
		'extensions':         DragonKey('c-t/50') + DragonText('chrome://extensions/\n'),
		# 'reopen <nn>':        Key('ws-t:%(nn)d'),
		# 'history':            Key('w-y'),
		# 'settings':           Key('w-comma'),
		# 'downloads':          Key('aw-l'),
		# '[manage] bookmarks': Key('aw-b'),
		# 'developer tools':    Key('aw-i'),
		# 'exit':               Key('w-q'),
		# 'select element':     Key('cs-c'),
	})
