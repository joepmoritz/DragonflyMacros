from dragonfly import MappingRule, Repetition, Alternative, Function


class RepeatRule(MappingRule):
	def __init__(self, name = None, repeatables = None, finishers = None, max = 10, exported = True):
		if repeatables is None: repeatables = self.repeatables
		if finishers is None: finishers = self.finishers

		repeatablesRule = Repetition(Alternative(repeatables), min=1, max=max, name='repeatables')
		finishersRule = Alternative(finishers, name='finishers')

		extras = [repeatablesRule, finishersRule]

		MappingRule.__init__(self, name = name, extras = extras, exported = exported)


	def Execute(repeatables = None, finishers = None):
		if repeatables:
			for action in repeatables:
				action.execute()

		if finishers:
			finishers.execute()

	mapping = {
		'[<repeatables>] [<finishers>]': Function(Execute),
	}

