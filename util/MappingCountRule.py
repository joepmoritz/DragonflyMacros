from dragonfly import MappingRule, Optional, Integer
from DictationElements import DictateWords
from NoCompile import NoCompile



class MappingCountRule(MappingRule):
	exported = False
	extras = [
		NoCompile(Optional(Integer(min = 0, max = 99), default = 1), name = 'nn'),
		Integer(min = 1, max = 10, name = 'n'),
		Integer(min = 1, max = 100, name = 'bign'),
		DictateWords('text')
	]
	defaults = {'n': 1, 'nn': 1, 'text': '', 'bign': 1}
