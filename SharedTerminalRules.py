import aenea.config
import aenea.configuration
import aenea.misc
import aenea.vocabulary

from dragonfly import *

from SharedRules import *
from util import *
from CommonMappings import common_folders
from SwapProgram import switch_to_normal_mode

common_folders['home'] = '~'

common_terminal_words = {
	'sudo':       'sudo',
	'apt-get':    'sudo apt-get',
	'pip':        'pip',
	'apt remove': 'sudo apt autoremove',
	'conda':      'conda',
	'install':    'install',
	'uninstall':  'uninstall',
	'list': 'list',
	'help': 'help',
	'update':     'update',
	'upgrade':    'upgrade',
	'create': 'create',
	'show':       'show',
	'export':     'export',
	# 'python':     'python',

	'firebase':       'firebase',
	'login':          'login',
	'init':           'init',
	'deploy':         'deploy',
	'only':           '--only',
	'database':       'database',
	'hosting':        'hosting',
	'functions':      'functions',
	'storage':        'storage',

	'theano': 'theano',
	'lasagne': 'lasagne',
	'PS gan': 'psgan',
	'spatial GAN': 'spatial_gan',
	'samples': 'samples',
	'models': 'models',

	'upstream':       'upstream',
	'master':         'master',

	'example':        'example',
	'platform':       'platform',
	'port':           'port',
	'test':           'test',
	'tool':           'tool',
	'source':         'src',
	'doc':            'doc',
	'readme':         'readme',
	'lib USB':        'libusb',
	'Speech coding':  'SpeechCoding',
	'speech catcher': 'Spraakvanger',
	'BT stack':       'btstack',
}


def TerminalContext():
	# AppContext(executable='powershell.exe')
	return AppContext(executable='ConEmu64.exe')




class TerminalRepeatablesRule(MappingRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('terminal', {
		'leap <quick_folder>': Text('cd %(quick_folder)s\n', pause = 0),
		'path <quick_folder>': Text('%(quick_folder)s', pause = 0),

		# 'new tab':     Key('w-w/100'),
		# 'teepee <nn>': Key('w-%(nn)d'),
		# 'twink <nn>':  Key('w-q:%(nn)d'),
		# 'trip <nn>':   Key('w-x:%(nn)d'),
		# 'new CMD':     Key('ca-c'),



		# 'G D B': Text('gdb '),
		# 'run': Text('run '),
		# 'backtrace': Text('backtrace '),
		# 'continue': Text('continue '),
		# 'step': Text('step '),
		# 'link': Text('link '),


		
	})

	extras = [
		NoCompile(Optional(Integer(min = 0, max = 100), default = 1), name = 'nn'),
		Choice(name = 'quick_folder', choices = common_folders),
	]





class TerminalFinishersRule(MappingCountRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('terminal', {
		'rename window [<text>]': Key('cw-r') + Text('%(text)s'),
		'show settings': Key('wa-p'),
		'(edit | setup) tasks': Key('wa-t'),
		'commit': Text('git commit'),
		'commit amend': Text('git commit --amend'),
		'W get pake': Text('wget ') + Key('c-v,enter'),
		'exit': Text('exit\n'),
		# 'new SSH jingyi': Key('w-w/50,f10/1,apps:down/1,r/2,apps:up/5') + Text('Jingyi') + Key('enter/10') + Text('ssh joep@jingyi') + Key('enter/50') + Text('screen\n\nsource activate py27\ncd psgan\n'),
		# 'old SSH jingyi': Key('w-w/50,f10/1,apps:down/1,r/2,apps:up/5') + Text('Jingyi') + Key('enter/10') + Text('ssh joep@jingyi') + Key('enter/50') + Text('screen -r\n'),
	})


class TerminalQuickFinishersRule(MappingCountRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('terminal', {
		'status': Text('git status\n'),
		'list branches': Text('git branch --verbose\n'),
		'list remotes': Text('git remote -v\n'),
		'quick log': Text('git log -n5\n'),
		'diff': Text('git diff\n'),
		'diff cached': Text('git diff --cached\n'),
		'add interactive': Text('git add --interactive\n'),
		'make install': Text('sudo make install\n'),
		'make clean': Text('make clean\n'),
		'make': Text('make\n'),
		'configure': Text('./configure\n'),
		'use Python two seven': Text('source activate py27\n'),
	})


terminal_windows_commands = windows_commands.copy()
terminal_windows_commands['clove <nn>'] = Key('wa-del')
terminal_windows_commands['quit'] = Key('w-f4')
# terminal_windows_commands['flick'] = Key('c-o')
terminal_windows_commands['shell'] = Key('c-o')

class TerminalWindowsCommandsRule(MappingCountRule):
	exported = False
	mapping = terminal_windows_commands





