desktop_names = {
	'home': 1,
	'script': 1,
	'work': 1,
	'bart': 1,
}

sublime_projects = [
	{
		'speech': 'lime speech',
		'project_name': 'SpeechCoding',
		# 'project_file_path': '/Users/joepmoritz/Projects/Personal/SpeechCoding.sublime-project',
		# 'desktop_name': 'script',
	},
	{
		'speech': 'lime auto hotkey',
		'project_name': 'AutoHotkey',
		# 'project_file_path': '/Users/joepmoritz/Projects/Personal/SpeechCoding.sublime-project',
		# 'desktop_name': 'script',
	},
	{
		'speech': 'lime clever',
		'project_name': 'CleverCoder',
		# 'project_file_path': '/Users/joepmoritz/Projects/Personal/CleverCoder.sublime-project',
		# 'desktop_name': 'script',
	},
	{
		'speech': 'lime settings',
		'project_name': 'my-sublime-settings',
		# 'desktop_name': 'script',
	},
	{
		'speech': '[lime] click by voice',
		'project_name': 'click-by-voice',
		'project_file_path': '/Users/joepmoritz/Projects/Personal/click-by-voice.sublime-project',
		# 'desktop_name': 'script',
	},
	{
		'speech': 'lime dot files',
		'project_name': 'dotfiles',
		# 'desktop_name': 'script',
	},
	{
		'speech': 'lime pro man',
		'project_name': 'ProjectManager',
		# 'desktop_name': 'script',
	},
	{
		'speech': 'lime ace jump',
		'project_name': 'ace-jump-sublime',
		# 'desktop_name': 'script',
	},
	{
		'speech': 'lime file browser',
		'project_name': 'SublimeFileBrowser',
		# 'desktop_name': 'script',
	},
	{
		'speech': 'lime terminus',
		'project_name': 'Terminus',
		# 'desktop_name': 'script',
	},
	{
		'speech': 'lime Dragon words',
		'project_name': 'DragonWords',
		# 'desktop_name': 'script',
	},
	{
		'speech': 'lime local',
		'project_name': 'localisation',
		# 'desktop_name': 'work',
	},
	{
		'speech': 'lime recon',
		'project_name': 'reconstruction',
		# 'desktop_name': 'work',
	},
	{
		'speech': 'lime SnapCV',
		'project_name': 'SnapCV',
		# 'desktop_name': 'work',
	},
	{
		'speech': 'lime new pruning',
		'project_name': 'new_pruning',
		# 'desktop_name': 'work',
	},
	{
		'speech': 'lime chunk merging',
		'project_name': 'chunk_merging',
		# 'desktop_name': 'work',
	},
	{
		'speech': 'lime lut hack',
		'project_name': 'lut_hack',
		# 'desktop_name': 'work',
	},
	{
		'speech': 'lime multi seed',
		'project_name': 'multi_seed',
		# 'desktop_name': 'work',
	},
	{
		'speech': 'lime lineariser',
		'project_name': 'lineariser',
		# 'desktop_name': 'work',
	},
	# {
	# 	'speech': '[lime] terminals',
	# 	'project_name': 'Terminals',
	# 	# 'desktop_name': 'work',
	# },
]

common_folders = [
	{
		'speech': 'personal',
		'path': '~/Personal',
	},
	{
		'speech': '(win | windows) downloads',
		'path': 'C:/Users/Joep Moritz/Downloads',
	},
	{
		'speech': '[Linux] downloads',
		'path': '~/Downloads',
	},
	{
		'speech': 'world AR',
		'path': '~/Projects/WorldAR',
		'desktop_name': 'work',
	},
	{
		'speech': 'videos',
		'path': '~/Projects/WorldAR/videos/carnaby-street',
		'desktop_name': 'work',
	},
	{
		'speech': 'SnapCV',
		'path': '~/Projects/WorldAR/SnapCV',
		'desktop_name': 'work',
	},
	{
		'speech': 'LensCore',
		'path': '~/Projects/WorldAR/LensCore',
		'desktop_name': 'work',
	},
	{
		'speech': '(recon | reconstruction) native',
		'path': '~/Projects/WorldAR/reconstruction_native',
		'desktop_name': 'work',
	},
	{
		'speech': 'cloud [recon]',
		'path': '~/Projects/WorldAR/cloud_reconstruction',
		'desktop_name': 'work',
	},
	{
		'speech': '(recon | reconstruction)',
		'path': '~/Projects/WorldAR/reconstruction',
		'desktop_name': 'work',
	},
	{
		'speech': 'det eval',
		'path': '~/Projects/WorldAR/detector_evaluation',
		'desktop_name': 'work',
	},
	{
		'speech': 'new pruning',
		'path': '~/Projects/WorldAR/new_pruning',
		'desktop_name': 'work',
	},
	{
		'speech': 'chunk merging',
		'path': '~/Projects/WorldAR/chunk_merging',
		'desktop_name': 'work',
	},
	{
		'speech': 'lut hack',
		'path': '~/Projects/WorldAR/lut_hack',
		'desktop_name': 'work',
	},
	{
		'speech': 'multi seed',
		'path': '~/Projects/WorldAR/multi_seed',
		'desktop_name': 'work',
	},
	{
		'speech': 'lineariser',
		'path': '~/Projects/WorldAR/lineariser',
		'desktop_name': 'work',
	},
	{
		'speech': 'Google Drive',
		'jump_point': 'Google Drive',
		'path': '/Users/joepmoritz/Google Drive',
		'desktop_name': 'work',
	}
]

for cf in common_folders:
	cf['path_win'] = cf['path'].replace('~', 'Z:')



common_websites = [
	{
		'speech': 'maps',
		'url': 'https://www.google.co.uk/maps',
	},
	{
		'speech': 'nationwide',
		'url': 'https://onlinebanking.nationwide.co.uk/AccessManagement/Login',
	},
	{
		'speech': 'lloyds',
		'url': 'https://online.lloydsbank.co.uk/personal/logon/login.jsp',
	},
	{
		'speech': 'ING',
		'url': 'https://www.ing.nl/particulier/index.html',
	},
	{
		'speech': 'scholar',
		'url': 'https://scholar.google.co.uk/',
	},
	{
		'speech': 'TFL',
		'url': 'tfl.gov.uk',
	},
	{
		'speech': 'Guardian',
		'url': 'https://www.theguardian.com/international',
	},
	{
		'speech': 'VK',
		'url': 'www.vk.nl',
	},
	{
		'speech': 'LinkedIn',
		'url': 'www.linkedin.com',
	},
	{
		'speech': 'photos',
		'url': 'photos.google.com',
	},
	{
		'speech': 'sheets',
		'url': 'https://docs.google.com/spreadsheets/u/0/',
	},
	{
		'speech': 'dropbox',
		'url': 'www.dropbox.com',
	},
	{
		'speech': 'amazon',
		'url': 'https://www.amazon.co.uk/',
	},
	{
		'speech': 'booking.com',
		'url': 'www.booking.com',
	},
	{
		'speech': 'indeed',
		'url': 'www.indeed.co.uk',
	},
	{
		'speech': 'glass door',
		'url': 'www.glassdoor.com',
	},
	{
		'speech': 'sky scanner',
		'url': 'www.skyscanner.net',
	},
	{
		'speech': 'Google drive',
		'url': 'drive.google.com',
	},
	{
		'speech': 'national rail',
		'url': 'www.nationalrail.co.uk',
	},
	{
		'speech': 'Google keep',
		'url': 'https://keep.google.com/',
	},
]
