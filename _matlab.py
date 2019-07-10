import aenea.config
import aenea.configuration
import aenea.misc
import aenea.vocabulary

from dragonfly import *

from SharedRules import *
from util import *
from CommonMappings import common_folders

matlab_context = AppContext(executable='matlab')
matlab_grammar = Grammar('matlab', context=matlab_context)
matlab_tags = ['matlab', 'keywords', 'functions']
matlab_keyword_vocabulary = DictListRef('keyword', aenea.vocabulary.register_dynamic_vocabulary('matlab_keywords'))
matlab_function_vocabulary = DictListRef('function', aenea.vocabulary.register_dynamic_vocabulary('matlab_functions'))




class MatlabRepeatablesRule(MappingCountRule):
	mapping = aenea.configuration.make_grammar_commands('terminal', {
		'stab':                              Key('tab/20,enter'),
		'break':                             Key('c-c'),
		'dear | dir':                        Text('cd '),
		'punk <nn>':                         Text('cd ..\n') * Repeat(extra = "nn"),
		'dodo <nn>':                         Text('../') * Repeat(extra = "nn"),
		'leap <quick_folder>': Text('cd d:%(quick_folder)s\n', pause = 0),
	})

	extras = [
		NoCompile(Optional(Integer(min = 0, max = 100), default = 1), name = 'nn'),
		Choice(name = 'quick_folder', choices = common_folders),
	]

keyword_value_function = lambda n, e: e['keyword'] + Key('space')
keyword_rule = Compound('key <keyword>', [matlab_keyword_vocabulary], value_func = keyword_value_function)

function_value_function = lambda n, e: e['function'] + Key('lparen,rparen,left')
function_rule = Compound('<function>', [matlab_function_vocabulary], value_func = function_value_function)

help_value_function = lambda n, e: Text('help ') + e['function']
help_rule = Compound('help <function>', [matlab_function_vocabulary], value_func = help_value_function)

class MatlabRepeatRule(RepeatRule):
	repeatables = [
		keyword_rule,
		help_rule,
		function_rule,
		RuleRef(rule=MatlabRepeatablesRule()),
		DictListRef('dynamic matlab', aenea.vocabulary.register_dynamic_vocabulary('matlab')),
	] + CommonRepeatables()
	finishers = CommonFinishers()


matlab_grammar.add_rule(MatlabRepeatRule())
matlab_grammar.load()

aenea.vocabulary.add_window_title_tag('MATLAB R20', 'matlab_file')



def unload():
	global matlab_grammar

	for tag in matlab_tags:
		aenea.vocabulary.unregister_dynamic_vocabulary(tag)

	if matlab_grammar:
		matlab_grammar.unload()

	matlab_grammar = None
