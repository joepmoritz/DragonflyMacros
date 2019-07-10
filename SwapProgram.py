# Author: Joep Moritz <joep.moritz@gmail.com>
from dragonfly import *
from util import DictateWords
from CommonMappings import *
from SharedChromeRules import SendCommandToClickByVoice


CurrentMode = 'unknown'

def switch_to_normal_mode():
	global CurrentMode
	if CurrentMode != 'normal':
		Mimic("normal", "mode", "on").execute()
		CurrentMode = 'normal'

def switch_to_command_mode():
	global CurrentMode
	if CurrentMode != 'command':
		Mimic("command", "mode", "on").execute()
		CurrentMode = 'command'

normal_mode = Function(switch_to_normal_mode)
command_mode = Function(switch_to_command_mode)



swap_program_mapping = {
	'normal mode': normal_mode,
	'command mode': command_mode,
	'net link messages': FocusWindow(title = 'Messages from Python Macros'),

	'chrome':                      Key('f6') + normal_mode,
	'<desktop_name> chrome':       Key('cw-%(desktop_name)d/50, control:up, alt:up, f6') + normal_mode,
	'google for [<text>]':         Key('f6/50,c-t/10') + Text('%(text)s') + normal_mode,

	'dictate':                     Key('c-a/10,c-c/10,cw-f3/100,c-a,c-v,c-home') + normal_mode,
	'dictate new':                 Key('cw-f3/100,c-a,del') + normal_mode,
	'dictate code':                Key('c-a/10,c-c/10,cw-f7') + Text('code') + Key('f12/100') + command_mode,
	'dictate python':              Key('c-a/10,c-c/10,cw-f7/5') + Text('python .py') + Key('f12/100,a-v,s,p,p,p,p,p,enter') + command_mode,
	'website <common_websites>':   Key('f6/50,c-t') + Text('%(common_websites)s\n', pause = 0) + normal_mode,
	# 'website <common_websites>':   Key('cw-%d/50,f6/50,c-t' % desktop_names['home']) + Text('%(common_websites)s\n', pause = 0) + normal_mode,
	'my (inbox | email)':          Key('f6/30,T/20') + Text('inbox.google.com') + Pause('10') + Key('enter') + normal_mode,
	'my calendar':                 Key('f6/30,T/20') + Text('Google Calendar') + Pause('10') + Key('enter') + normal_mode,
	'work email':                  Key('f6/30,T/20') + Text('outlook.office.com') + Pause('10') + Key('enter') + normal_mode,
	# 'google keep | my notes':    Key('f6/50,c-3') + normal_mode,
	'google that':                 Key('c-c,f6/50,c-t,c-v,enter') + normal_mode,
	'map that':                    Key('c-c,f6/50,c-t') + Text('https://www.google.co.uk/maps\n') + Pause('100') + Function(SendCommandToClickByVoice, command='lb') + Pause('100') + Key('c-v,enter') + normal_mode,
	'scholar that':                Key('c-c,f6/50,c-t/20') + Text('scholar.google.com') + Key('enter/300,g,i/10,c-v,enter') + normal_mode,
	'mat lab':                     Key('f8') + command_mode,
	'micro word':                  Key('a-f8') + normal_mode,
	# 'term':                        Key('f4') + command_mode,
	'lime':                        Key('f7') + command_mode,
	'<desktop_name> lime':         Key('cw-%(desktop_name)d/50,f7') + command_mode,
	# 'finder':                      Key('f5') + command_mode,
	'keepass':                     Key('c-f7/100, control:up'),
	'mandalay':                    Key('c-f8/100, control:up'),
	'PDF | Sumatra':               Key('c-f5'),
	# 'Skype':                       Key('s-f4'),
	'Jingyi':                      Key('c-f6/50, control:up') + normal_mode,
	'Posture monitor':             Key('a-f12/50, alt:up'),
	# '<desktop_name> desktop':      Key('cw-%(desktop_name)d'),
	'move <desktop_name> desk':    Key('scw-%(desktop_name)d'),
	# 'wisp <n>':                    Key('w-%(n)d'),
	# 'imber': BringApp('notepad'),

	# 'snipping tool': BringApp('SnippingTool.exe', cwd='C:/Windows/System32', shell=True),
	'snipping tool': Key('w-r/20') + Text('C:/Windows/System32/SnippingTool.exe') + Key('enter'),
	'Reload AutoHotKey': StartApp('MyScripts.ahk', cwd='C:/Users/Joep/Google Drive/ScriptsAndSettings/AutoHotkeyScripts', shell=True),
}

swap_program_mapping['websites scholar'] = Key('cw-%d/50,f6/50,c-t' % desktop_names['work']) + Text('%s\n' % common_websites['scholar'], pause = 0) + normal_mode


terminal_actions = {
	'<desktop_name> mid com': {
		'desktop_number': '%(desktop_name)d',
		'name': 'mc - ',
		'start_command': 'mc',
		'late_start_command': False
	},
	'<desktop_name> term': {
		'desktop_number': '%(desktop_name)d',
		'name': 'term - ',
		'start_command': False,
		'late_start_command': False
	},
	'mid com jingyi': {
		'desktop_number': desktop_names['work'],
		'name': 'mc - jingyi',
		'start_command': 'mc',
		'late_start_command': '{F9}fqsh://joep@jingyi/home/joep/' # + Pause('200') + Key('f9,enter,h/2') + Text('joep@jingyi\n')
		# 'late_start_command': '{F9}{enter}hjoep@jingyi' # + Pause('200') + Key('f9,enter,h/2') + Text('joep@jingyi\n')
	},
	'mid com jet': {
		'desktop_number': desktop_names['work'],
		'name': 'mc - UCL jet',
		'start_command': 'mc',
		'late_start_command': '{F9}fqsh://jmoritz@jet.cs.ucl.ac.uk/cs/academic/phd1/marine/jmoritz' # + Pause('200') + Key('f9,enter,h/2') + Text('joep@jingyi\n')
	},
	'ssh jingyi': {
		'desktop_number': desktop_names['work'],
		'name': 'ssh - jingyi',
		'start_command': 'ssh joep@jingyi',
		'late_start_command': 'screen -d -RR\n\nsource activate py27\ncd ~/psgan'
	},
	'ssh jet': {
		'desktop_number': desktop_names['work'],
		'name': 'ssh - UCL jet',
		'start_command': 'ssh jmoritz@jet.cs.ucl.ac.uk',
		'late_start_command': ''
	},
	'mid com': {
		'desktop_number': False,
		'name': 'mc - ',
		'start_command': 'mc',
		'late_start_command': False
	},
	'term': {
		'desktop_number': False,
		'name': 'term - ',
		'start_command': False,
		'late_start_command': False
	},
	'ssh': {
		'desktop_number': False,
		'name': 'ssh - ',
		'start_command': False,
		'late_start_command': False
	},
	'python': {
		'desktop_number': False,
		'name': 'python',
		'start_command': 'python',
		'late_start_command': 'import numpy as np\nimport pandas as pd\nfrom pprint import pprint as pp'
	}
}

for (name, folder) in common_folders.iteritems():
	terminal_actions['mid com ' + name] = {
		'desktop_number': folder_desktops.get(name, False),
		'name': 'mc - %s' % name,
		'start_command': 'cd %s && mc' % folder
	}

	terminal_actions['term ' + name] = {
		'desktop_number': folder_desktops.get(name, False),
		'name': 'term - %s' % name,
		'start_command': 'cd %s' % folder
	}


terminal_actions['sync PS gan'] = terminal_actions['term PS gan'].copy()
terminal_actions['sync PS gan'].update({
	'always_command': 'rsync -vL --timeout=5 %s/* joep@jingyi:~/psgan/' % common_folders['PS gan']
})

terminal_actions['run PS gan'] = terminal_actions['ssh jingyi'].copy()
terminal_actions['run PS gan'].update({
	'always_command': 'cd ~/psgan\npython psgan.py'
})

terminal_actions['run visualize'] = terminal_actions['ssh jingyi'].copy()
terminal_actions['run visualize'].update({
	'always_command': 'cd ~/psgan\npython visualize.py model.psgan'
})

terminal_actions['run show differences'] = terminal_actions['ssh jingyi'].copy()
terminal_actions['run show differences'].update({
	'always_command': 'cd ~/psgan\npython show_differences.py model.psgan'
})

terminal_actions['run make embedding'] = terminal_actions['ssh jingyi'].copy()
terminal_actions['run make embedding'].update({
	'always_command': 'cd ~/psgan\npython make_embedding.py model.psgan'
})

terminal_actions['run plot result'] = terminal_actions['ssh jingyi'].copy()
terminal_actions['run plot result'].update({
	'always_command': 'cd ~/psgan\npython plot_result.py'
})




def MakeTerminalAction(desktop_number, name, start_command = False, late_start_command = False, always_command = False):
	start_key = 's-f4/5'
	if desktop_number:
		start_key = 'cw-%s/50,%s' % (str(desktop_number), start_key)

	action = Key(start_key) + Text(name, pause = 0.001) + Key('f11/2')
	action += Text(start_command, pause = 0.001) + Key('f11/2') if start_command else Text('') + Key('f12/2')
	action += Text(late_start_command, pause = 0.001) + Key('f11/2') if late_start_command else Text('') + Key('f12/2')
	action += Text(always_command, pause = 0.001) + Key('f11/2') if always_command else Text('') + Key('f12/2')

	return action


for (command, terminal_action) in terminal_actions.iteritems():
	swap_program_mapping[command] = MakeTerminalAction(**terminal_action)










class SwapProgramRule(MappingRule):
	mapping = swap_program_mapping
	exported = False
	extras = [
		Integer(min = 1, max = 5, name = 'n'),
		DictateWords('text'),
		Choice(name = 'quick_folder', choices = common_folders),
		Choice(name = 'common_websites', choices = common_websites),
		Choice(name = 'desktop_name', choices = desktop_names),
	]
	defaults = {'n': 1}

