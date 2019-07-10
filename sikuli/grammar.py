from dragonfly import Grammar, Key, Function, MappingRule

from sikuli.dragonfly_proxy import launch_IDE, launch_server, reload_scripts, unload_proxy



sikuli_grammar = Grammar('Sikuli')


class SikuliRule(MappingRule):
	mapping = {
			"launch sick IDE":           Function(launch_IDE),
			"launch sick server":        Function(launch_server),
			"reload sick you Lee":       Function(reload_scripts),
			"sick you Lee shot":         Key("cs-2"),
		}


sikuli_grammar.add_rule(SikuliRule())

sikuli_grammar.load()


def unload():
	global sikuli_grammar

	if sikuli_grammar:
		sikuli_grammar.unload()
	sikuli_grammar = None

	unload_proxy()
