from dragonfly.grammar.elements import Empty


class NoCompile(Empty):

	def __init__(self, child, name=None):
		self._child = child
		Empty.__init__(self, name=name)


	def dependencies(self, memo):
		if self._id in memo:
			return []
		memo.add(self._id)
		return self._child.dependencies(memo)


	def compile(self, compiler):
		pass


	def gstring(self):
		return "<NoCompile(" + self._child.gstring() + ")>"


	def decode(self, state):
		# print "NoCompile.decode"
		state.decode_attempt(self)

		# Allow the rule to attempt decoding.
		for result in self._child.decode(state):
			state.decode_success(self)
			yield state
			state.decode_retry(self)

		# The rule failed to deliver a valid decoding, failure.
		state.decode_failure(self)
		return


	def value(self, node):
		# print "NoCompile.value %s" % node.children[0].value()
		return node.children[0].value()

