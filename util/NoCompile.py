from dragonfly.grammar.elements import Empty


class NoCompile(Empty):

	def __init__(self, child, name=None, default=None):
		Empty.__init__(self, name, value = True, default=default)

		self._child = child


	def dependencies(self, memo):
		if self in memo:
			return []
		memo.append(self)
		return self._child.dependencies(memo)

	def gstring(self):
		return "[[" + self._child.gstring() + "]]"

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

