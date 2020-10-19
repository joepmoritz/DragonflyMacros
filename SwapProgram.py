# -*- coding: utf-8 -*-
# Author: Joep Moritz <joep.moritz@gmail.com>
from dragonfly import Key as DragonKey, Text as DragonText, BringApp as DragonBringApp, FocusWindow as DragonFocusWindow
from dragonfly import *
# from aenea.strict import Key, Text, Mouse
# from aenea import ProxyBringApp as BringApp, NoAction
from util import DictateWords
from CommonMappings import *
from SharedChromeRules import SendCommandToClickByVoice
from SharedTerminalRules import WINDOW_TITLE_IDENTIFIER as TERMINAL_IDENTIFIER


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
# normal_mode = DragonFocusWindow(title='Notepad')
# command_mode = DragonFocusWindow(title='Messages from Python Macros', focus_only=True)
# normal_mode = NoAction()
# command_mode = NoAction()
bring_notepad = BringApp('Notepad.exe') + Pause('100')
bring_chrome =  BringApp('chrome.exe') + normal_mode
# bring_chrome = BringApp(process_name='WinAppHelper', process_title='Google Chrome', window_not='Slack')
bring_commit_message = BringApp(['notepad.exe', r'Z:\.GIT_COMMIT_MSG'], title='.GIT_COMMIT_MSG')
remember_window = Key('cw-f3/10')


def BringChrome(title, **kwargs):
	return BringApp('chrome.exe', title=title, **kwargs) + normal_mode

def BringWindow(w1, w2):
	return Key('win:down/10,{w1}:{w2}/20,win:up/50'.format(w1=w1, w2=w2))

def BringWebsite(title, w1, w2, url):
	jump_website_action = BringWindow(w1, w2) + Key('c-m/20,del/40') + Text(url) + Pause('50') + Key('enter')
	return BringChrome(title, start_action=jump_website_action)

# bring_chrome = BringWindow(1, 1) + normal_mode


swap_program_mapping = {
	'normal mode': normal_mode,
	'command mode': command_mode,
	'net link messages': FocusWindow(title = 'Messages from Python Macros'),

	'chrome':                    bring_chrome,
	# '[work] chrome <n>':           Key('win:down/10,1:%(n)d/10,win:up/10'Slack) + normal_mode,
	'[work] chrome <n>':         BringWindow(1, '%(n)d') + normal_mode,
	'work chrome':               BringWindow(1, 1) + normal_mode,
	# '[work] chrome <w2>':          Function(BringWindow, w1=3),
	'home chrome [<n>]':            BringWindow(3, '%(n)d') + normal_mode,
	# '<desktop_name> chrome':       Key('cw-%(desktop_name)d') + Pause('50') + bring_chrome + normal_mode,
	'google for [<text>]':         bring_chrome + Pause('50') + Key('c-t/50') + Text('%(text)s'),

	'dictate (this|that)':         remember_window + Key('c-c/10') + bring_notepad + DragonKey('c-a,del,c-v,c-end') + normal_mode,
	'dictate all':                 remember_window + Key('c-a,c-c/10') + bring_notepad + DragonKey('c-a,del,c-v,c-end') + normal_mode,
	'dictate new':                 remember_window + bring_notepad + DragonKey('c-a,del') + normal_mode,
	'dictate':                     normal_mode + bring_notepad,
	# 'dictate code':                Key('c-a/10,c-c/10,cw-f7') + Text('code') + Key('f12/100') + command_mode,
	# 'dictate python':           [u'shared', u'rules']   Key('c-a/10,c-c/10,cw-f7/5') + Text('python .py') + Key('f12/100,a-v,s,p,p,p,p,p,enter') + command_mode,

	'commit message':                bring_commit_message + normal_mode,
	'new commit message':            remember_window + bring_commit_message + Pause('100') + Key('c-a,del') + normal_mode,
	'website <common_websites>':     bring_chrome + Pause('50') + Key('c-t/10') + Text('%(common_websites)s\n', pause = 0) + normal_mode,
	'work e-mail':                   BringWebsite('Snap Inc. Mail', 1, 1, 'inbox.google.com'),
	'google that':                 Key('c-c') + bring_chrome + Pause('50') + DragonKey('c-t/10') + DragonKey('c-v,enter'),
	# 'map that':                    Key('w-c') + bring_chrome + Pause('50') + Key('w-t/10') + Text('https://www.google.co.uk/maps\n') + Pause('100') + Function(SendCommandToClickByVoice, command='lb') + Pause('100') + Key('w-v,enter') + command_mode,
	# 'scholar that':                Key('c-c') + bring_chrome + Pause('50') + DragonKey('c-t/10') + DragonText('scholar.google.com') + DragonKey('enter/300,g,i/10,c-v,enter'),
	# 'mat lab':                     Key('f8') + command_mode,
	# 'micro word':                  Key('a-f8') + command_mode,
	# 'term':                        Key('f4') + command_mode,
	# 'lime':                        Key('wcsa-f7/10,wcsa-f7')new_ + command_mode,
	'lime':                        BringApp('sublime_text.exe') + command_mode,
	# 'lime <n>':                    Key('win:down,2:%(n)d,win:up/10,enter') + command_mode,
	'lime <n>':                    BringWindow(2, '%(n)d'),
	# '<desktop_name> lime':         Key('cw-%(desktop_name)d') + Pause('50') + BringApp('sublime_text.exe') + command_mode,
	# 'finder | explorer':           BringApp('explorer.exe') + command_mode,
	'finder | explorer':           Key('f5') + command_mode,
	# 'slack':                       BringApp('chrome.exe', title='Slack') + normal_mode,
	'slack':                       BringWebsite('Slack', 1, 2, 'app.slack.com'),
	# 'PDF | Sumatra':               Key('c-f5'),
	# 'Skype':                       Key('s-f4'),
	# 'Jingyi':                      Key('c-f6/50, control:up') + command_mode,
	# 'Posture monitor':             Key('a-f12/50, alt:up'),
	# '<desktop_name> desktop':      Key('cw-%(desktop_name)d'),
	# 'move <desktop_name> desk':    Key('scw-%(desktop_name)d'),
	# 'wisp <n>':                    Key('w-%(n)d'),
	# 'imber': BringApp('notepad'),

	# 'snipping tool': BringApp('SnippingTool.exe', cwd='C:/Windows/System32', shell=True),
	# 'snipping tool': Key('w-r/20') + Text('C:/Windows/System32/SnippingTool.exe') + Key('enter'),
	# 'Reload AutoHotKey': StartApp('MyScripts.ahk', cwd='C:/Users/Joep/Google Drive/ScriptsAndSettings/AutoHotkeyScripts', shell=True),
}

# swap_program_mapping['websites scholar'] = Key('cw-%d/50,f6/50,c-t' % desktop_names['work']) + Text('%s\n' % common_websites['scholar'], pause = 0) + normal_mode


for sublime_project in sublime_projects:
	project_name = sublime_project['project_name']
	start_action = BringApp('sublime_text.exe') + Pause('50') + Key('ca-p') + Pause('50') + Text(project_name) + Key('enter')
	# bring_action = BringApp('sublime_text.exe', title=u'— '+project_name, start_action=start_action)
	bring_action = BringApp('sublime_text.exe', title=u'('+project_name+')', start_action=start_action)
	action = bring_action + command_mode
	if 'desktop_name' in sublime_project:
		desktop = desktop_names[sublime_project['desktop_name']]
		action = Key('cw-%d' % desktop) + Pause('50') + action
	swap_program_mapping[sublime_project['speech']] = action


for folder in common_folders:
	if 'jump_point' in folder:
		start_action = BringApp('sublime_text.exe') + Key('c-m,c-j') + Text(folder['jump_point']) + Key('enter')
		bring_action = BringApp('sublime_text.exe', title=u'— ' + folder['jump_point'], start_action=start_action)
		action = bring_action + command_mode
		if 'desktop_name' in folder:
			desktop = desktop_names[folder['desktop_name']]
			action = Key('cw-%d' % desktop) + Pause('50') + action
		swap_program_mapping['browse ' + folder['speech']] = action


# terminal_actions = {
# 	'<desktop_name> mid com': {
# 		'desktop_number': '%(desktop_name)d',
# 		'name': 'mc - ',
# 		'start_command': 'mc',
# 		'late_start_command': False
# 	},
# 	'<desktop_name> term': {
# 		'desktop_number': '%(desktop_name)d',
# 		'name': 'term - ',
# 		'start_command': False,
# 		'late_start_command': False
# 	},
# 	'mid com jingyi': {
# 		'desktop_number': desktop_names['work'],
# 		'name': 'mc - jingyi',
# 		'start_command': 'mc',
# 		'late_start_command': '{F9}fqsh://joep@jingyi/home/joep/' # + Pause('200') + Key('f9,enter,h/2') + Text('joep@jingyi\n')
# 		# 'late_start_command': '{F9}{enter}hjoep@jingyi' # + Pause('200') + Key('f9,enter,h/2') + Text('joep@jingyi\n')
# 	},
# 	'mid com jet': {
# 		'desktop_number': desktop_names['work'],
# 		'name': 'mc - UCL jet',
# 		'start_command': 'mc',
# 		'late_start_command': '{F9}fqsh://jmoritz@jet.cs.ucl.ac.uk/cs/academic/phd1/marine/jmoritz' # + Pause('200') + Key('f9,enter,h/2') + Text('joep@jingyi\n')
# 	},
# 	'ssh jingyi': {
# 		'desktop_number': desktop_names['work'],
# 		'name': 'ssh - jingyi',
# 		'start_command': 'ssh joep@jingyi',
# 		'late_start_command': 'screen -d -RR\n\nsource activate py27\ncd ~/psgan'
# 	},
# 	'ssh jet': {
# 		'desktop_number': desktop_names['work'],
# 		'name': 'ssh - UCL jet',
# 		'start_command': 'ssh jmoritz@jet.cs.ucl.ac.uk',
# 		'late_start_command': ''
# 	},
# 	'mid com': {
# 		'desktop_number': False,
# 		'name': 'mc - ',
# 		'start_command': 'mc',
# 		'late_start_command': False
# 	},
# 	'term': {
# 		'desktop_number': False,
# 		'name': 'term - ',
# 		'start_command': False,
# 		'late_start_command': False
# 	},
# 	'ssh': {
# 		'desktop_number': False,
# 		'name': 'ssh - ',
# 		'start_command': False,
# 		'late_start_command': False
# 	},
# 	'python': {
# 		'desktop_number': False,
# 		'name': 'python',
# 		'start_command': 'python',
# 		'late_start_command': 'import numpy as np\nimport pandas as pd\nfrom pprint import pprint as pp'
# 	}
# }

# for (name, folder) in common_folders.iteritems():
# 	terminal_actions['mid com ' + name] = {
# 		'desktop_number': folder_desktops.get(name, False),
# 		'name': 'mc - %s' % name,
# 		'start_command': 'cd %s && mc' % folder
# 	}

# 	terminal_actions['term ' + name] = {
# 		'desktop_number': folder_desktops.get(name, False),
# 		'name': 'term - %s' % name,
# 		'start_command': 'cd %s' % folder
# 	}


# terminal_actions['sync PS gan'] = terminal_actions['term PS gan'].copy()
# terminal_actions['sync PS gan'].update({
# 	'always_command': 'rsync -vL --timeout=5 %s/* joep@jingyi:~/psgan/' % common_folders['PS gan']
# })

# terminal_actions['run PS gan'] = terminal_actions['ssh jingyi'].copy()
# terminal_actions['run PS gan'].update({
# 	'always_command': 'cd ~/psgan\npython psgan.py'
# })

# terminal_actions['run visualize'] = terminal_actions['ssh jingyi'].copy()
# terminal_actions['run visualize'].update({
# 	'always_command': 'cd ~/psgan\npython visualize.py model.psgan'
# })

# terminal_actions['run show differences'] = terminal_actions['ssh jingyi'].copy()
# terminal_actions['run show differences'].update({
# 	'always_command': 'cd ~/psgan\npython show_differences.py model.psgan'
# })

# terminal_actions['run make embedding'] = terminal_actions['ssh jingyi'].copy()
# terminal_actions['run make embedding'].update({
# 	'always_command': 'cd ~/psgan\npython make_embedding.py model.psgan'
# })

# terminal_actions['run plot result'] = terminal_actions['ssh jingyi'].copy()
# terminal_actions['run plot result'].update({
# 	'always_command': 'cd ~/psgan\npython plot_result.py'
# })




# def MakeTerminalAction(desktop_number, name, start_command = False, late_start_command = False, always_command = False):
# 	start_key = 'f4/5'
# 	if desktop_number:
# 		start_key = 'cw-%s/50,%s' % (str(desktop_number), start_key)

# 	action = Key(start_key)
# 	# action = Key(start_key) + Text(name, pause = 0.001) + Key('f11/2')
# 	# action += Text(start_command, pause = 0.001) + Key('f11/2') if start_command else Text('') + Key('f12/2')
# 	# action += Text(late_start_command, pause = 0.001) + Key('f11/2') if late_start_command else Text('') + Key('f12/2')
# 	# action += Text(always_command, pause = 0.001) + Key('f11/2') if always_command else Text('') + Key('f12/2')

# 	return action


# for (command, terminal_action) in terminal_actions.iteritems():
# 	swap_program_mapping[command] = MakeTerminalAction(**terminal_action)








small_integer = ShortIntegerRef(min=1, max=9, name='n')
common_websites_choice = { w['speech']: w['url'] for w in common_websites }

class SwapProgramRule(MappingRule):
	mapping = swap_program_mapping
	exported = False
	extras = [
		RuleRef(small_integer.rule, "n"),
		RuleRef(small_integer.rule, "w1"),
		RuleRef(small_integer.rule, "w2"),
		DictateWords('text'),
		# Choice(name = 'quick_folder', choices = common_folders),
		Choice(name = 'common_websites', choices = common_websites_choice),
		Choice(name = 'desktop_name', choices = desktop_names),
	]
	defaults = {'n': 1}

