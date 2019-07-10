from dragonfly import Key, Text, Function, Optional, Choice, Integer
from dragonfly.windows.clipboard import Clipboard

import aenea.config
import aenea.configuration
import string

from util import MappingCountRule, NoCompile

hint_first_letters = ['L', 'P', 'M', 'R', 'T', 'S', 'G', 'Y', 'F', 'J', 'SL', 'FL', 'BL', 'GL', 'ST', 'TR', 'KR']
jump_letters_direct = {fl + 'o': i for i, fl in enumerate(hint_first_letters)}
jump_letters_new_tab = {fl + 'ee': i for i, fl in enumerate(hint_first_letters)}
jump_letters_hover = {fl + 'ay': i for i, fl in enumerate(hint_first_letters)}
jump_letters_copy_url = {fl + 'op': i for i, fl in enumerate(hint_first_letters)}
jump_letters_copy_text = {fl + 'oppy': i for i, fl in enumerate(hint_first_letters)}

jump_letters_direct['Toe'] = jump_letters_direct['To']
jump_letters_new_tab['Me'] = jump_letters_new_tab['Mee']
jump_letters_new_tab['Re'] = jump_letters_new_tab['Ree']


def SendCommandToClickByVoice(command):
	def go():
		temporary = Clipboard({Clipboard.format_text: command})
		temporary.copy_to_system()
		Key('cs-dot/100').execute()

	try:
		original = Clipboard(from_system=True)
		go()
		original.copy_to_system()
	except Exception as e:
		go()

def ActivateLink(jl_direct, letter):
	SendCommandToClickByVoice(hint_first_letters[jl_direct] + letter)

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
		'new tab':                  Key('c-t'),
		'new window':               Key('c-n'),
		'new incognito':            Key('cs-n'),
		'teepee <nn>':              Key('c-%(nn)d'),
		'teepee back':              Key('caret'),
		'twink <nn>':               Key('cs-tab:%(nn)d'),
		'trip <nn>':                Key('c-tab:%(nn)d'),
		'steak' :                   Key('c-s'),
		'stop' :                    Key('c-dot'),
		'print' :                   Key('c-p'),
		'zoom in <nn>':             Key('c-plus:%(nn)d'),
		'zoom out <nn>':            Key('c-minus:%(nn)d'),
		'links':                    Key('c-m'),
		'tinks':                    Key('c-k'),
		'multi links':              Key('a-f'),
		'copy link URL':            Key('y,f'),
		'reload | refresh':         Key('c-r'),
		'duplicate tab | dope tab': Key('y,t'),
		'(pin | unpin) tab':        Key('a-p'),
		'move tab left':            Key('langle, langle'),
		'move tab right':           Key('rangle, rangle'),
		'save to mandalay': Key('cs-m'),
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
		'reopen <nn>':        Key('cs-t:%(nn)d'),
		'history':            Key('c-h'),
		'settings': Key('a-e,s'),
		'extensions': Key('a-e,l,e'),
		'downloads':          Key('c-j'),
		'[manage] bookmarks': Key('cs-o'),
		'developer tools':    Key('cs-i'),
		'exit':               Key('cs-q'),
		'select element': Key('cs-c'),
	})
