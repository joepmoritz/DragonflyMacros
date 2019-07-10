import aenea.configuration

# from dragonfly.grammar.elements_basic import Repetition, Alternative, RuleRef, ElementBase, Literal
# from dragonfly.grammar.elements_compound import Choice, Compound
# from dragonfly import MappingRule, CompoundRule

from dragonfly import *

from util import DictInteger, DictateWords, MappingCountRule



def recurse_values(node, types):
	value = ''
	for child in node.children:
		if child.actor.__class__ in types:
			value += child.value()
		value += recurse_values(child, types)
	return value


class GitAddOptionRule(MappingRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('git_add_options', {
		'dry run': '--dry-run ',
		'verbose': '--verbose ',
		'force': '--force ',
		'interactive': '--interactive ',
		'patch': '--patch ',
		'edit': '--edit ',
		'update': '--update ',
		'all': '--all ',
		'no ignore removal': '--no-ignore-removal ',
		'no all': '--no-all ',
		'ignore removal': '--ignore-removal ',
		'intent to add': '--intent-to-add ',
		'refresh': '--refresh ',
		'ignore errors': '--ignore-errors ',
		'ignore missing': '--ignore-missing '
	})
add_option = RuleRef(name='add_option', rule=GitAddOptionRule())
add_options = Repetition(add_option, min=1, max=10, name='add_options')


class GitAddRule(CompoundRule):
	exported = False
	spec = "add [<add_options>]"
	extras = [add_options]

	def value(self, node):
		return 'add ' + recurse_values(node, [GitAddOptionRule])
add_rule = RuleRef(name='add_rule', rule=GitAddRule())

class GitDiffOptionRule(MappingRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('git_diff_options', {
		'cached': '--cached ',
	})
diff_option = RuleRef(name='diff_option', rule=GitDiffOptionRule())
diff_options = Repetition(diff_option, min=1, max=3, name='diff_options')


class GitDiffRule(CompoundRule):
	exported = False
	spec = "diff [<diff_options>]"
	extras = [diff_options]

	def value(self, node):
		return 'diff ' + recurse_values(node, [GitDiffOptionRule])
diff_rule = RuleRef(name='diff_rule', rule=GitDiffRule())


class GitCommitOptionRule(MappingRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('git_commit_options', {
		'all': '--all ',
		'patch': '--patch ',
		'reuse message': '--reuse-message="',
		'reedit message': '--reedit-message="',
		'fix up': '--fixup="',
		'squash': '--squash="',
		'reset author': '--reset-author ',
		'short': '--short ',
		'branch': '--branch ',
		'porcelain': '--porcelain ',
		'long': '--long ',
		'null': '--null ',
		'file': '-F ',
		'author': '--author="',
		'date': '--date="',
		'message': '--message="',
		'template': '-t ',
		'signoff': '--signoff ',
		'no verify': '--no-verify ',
		'allow empty message': '--allow-empty-message ',
		'allow empty': '--allow-empty ',
		'edit': '--edit ',
		'no edit': '--no-edit ',
		'amend': '--amend ',
		'no post rewrite': '--no-post-rewrite ',
		'include': '--include ',
		'only': '--only ',
		'verbose': '--verbose ',
		'quiet': '--quiet ',
		'dry run': '--dry-run ',
		'status': '--status ',
		'no status': '--no-status ',
		# TODO: add cleanup and options
		# TODO: add mode and options
	})
commit_option = RuleRef(
	name='commit_option', rule=GitCommitOptionRule()
)
commit_options = Repetition(
	commit_option, min=1, max=10, name='commit_options'
)


class GitCommitRule(CompoundRule):
	exported = False
	spec = 'commit [<commit_options>]'
	extras = [commit_options]

	def value(self, node):
		return 'commit ' + recurse_values(node, [GitCommitOptionRule])
commit_rule = RuleRef(name='commit_rule', rule=GitCommitRule())


class GitCheckoutOptionRule(MappingRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands(
		'git_checkout_options', {
			'quiet': '--quiet ',
			'force': '--force ',
			'ours': '--ours ',
			'theirs': '--theirs ',
			'branch': '-b ',
			'track': '--track ',
			'no track': '--no-track ',
			'detatch': '--detach ',
			'orphan': '--orphan ',
			'ignore skip worktree bits': '--ignore-skip-worktree-bits ',
			'merge': '--merge ',
			'patch': '--patch ',
		})
checkout_option = RuleRef(
	name='checkout_option', rule=GitCheckoutOptionRule()
)
checkout_options = Repetition(
	checkout_option, min=1, max=10, name="checkout_options"
)


class GitCheckoutRule(CompoundRule):
	exported = False
	spec = 'checkout [<checkout_options>]'
	extras = [checkout_options]

	def value(self, node):
		return 'checkout ' + recurse_values(node, [GitCheckoutOptionRule])
checkout_rule = RuleRef(name='checkout_rule', rule=GitCheckoutRule())


class GitPushOptionRule(MappingRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('git_push_options', {
		"all": "--all ",
		"prune": "--prune ",
		"mirror": "--mirror ",
		"dry run": "--dry-run ",
		"delete": "--delete ",
		"tags": "--tags ",
		"force": "--force ",
		"set upstream": "--set-upstream ",
	})
push_option = RuleRef(name="push_option", rule=GitPushOptionRule())
push_options = Repetition(push_option, min=1, max=10, name="push_options")


class GitPushRule(CompoundRule):
	exported = False
	spec = "push [<push_options>]"
	extras = [push_options]

	def value(self, node):
		return "push " + recurse_values(node, [GitPushOptionRule])
push_rule = RuleRef(name="push_rule", rule=GitPushRule())


class GitStatusRuleOption(MappingRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands('git_status_options', {
		"short": "--short ",
		"branch": "--branch ",
		"long": "--long ",
		"ignored": "--ignored ",
	})
status_option = RuleRef(
	name="status_option", rule=GitStatusRuleOption()
)
status_options = Repetition(
	status_option, min=1, max=10, name="status_options"
)


class GitStatusRule(CompoundRule):
	exported = False
	spec = "status [<status_options>]"
	extras = [status_options]

	def value(self, node):
		return "status " + recurse_values(node, [GitStatusRuleOption])
status_rule = RuleRef(name="status_rule", rule=GitStatusRule())


class GitPrettyFormatRule(MappingRule):
	exported = False
	mapping = {
		"one line": "oneline ",
		"short": "short ",
		"medium": "medium ",
		"full": "full ",
		"fuller": "fuller ",
		"email": "email ",
		"raw": "raw ",
	}
pretty_format_rule = RuleRef(
	name="pretty_format_rule", rule=GitPrettyFormatRule()
)


class GitPrettyRule(CompoundRule):
	exported = False
	spec = "pretty <pretty_format_rule>"
	extras = [pretty_format_rule]

	def value(self, node):
		return "--pretty=" + recurse_values(node, [GitPrettyFormatRule])
pretty_rule = RuleRef(name="pretty_rule", rule=GitPrettyRule())
pretty_rules = Alternative(name="pretty_rules", children=[
	pretty_rule
])


class GitLogOptionRule(CompoundRule):
	exported = False
	# TODO: expand this class to use more than a single "pretty" rule
	spec = "<pretty_rules>"
	extras = [pretty_rules]

	def value(self, node):
		return '' + recurse_values(node, [GitPrettyRule])
log_option = RuleRef(name="log_option", rule=GitLogOptionRule())


class GitLogRule(CompoundRule):
	exported = False
	spec = "log [<log_option>]"
	extras = [log_option]

	def value(self, node):
		return "log "
log_rule = RuleRef(name="log_option", rule=GitLogRule())


class GitBranchOptionRule(MappingRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands(
		'git_branch_options', {
			'delete': '--delete ',
			'force': '--force ',
			'move': '--move ',
			'remotes': '--remotes ',
			'verbose': '--verbose ',
			'quiet': '--quite ',
		}
	)
branch_option = RuleRef(
	name="branch_option", rule=GitBranchOptionRule()
)
branch_options = Repetition(
	branch_option, min=1, max=10, name="branch_options"
)


class GitBranchRule(CompoundRule):
	exported = False
	spec = "branch [<branch_options>]"
	extras = [branch_options]

	def value(self, node):
		return "branch " + recurse_values(node, [GitBranchOptionRule])
branch_rule = RuleRef(name="branch_rule", rule=GitBranchRule())


class GitPullOption(MappingRule):
	exported = False
	mapping = aenea.configuration.make_grammar_commands(
		"git_pull_options", {
			"quiet": "--quiet ",
			"verbose": "--verbose ",
			"rebase": "--rebase ",
			"force": "--force ",
		}
	)
pull_option = RuleRef(name="pull_option", rule=GitPullOption())
pull_options = Repetition(pull_option, min=1, max=10, name="pull_options")


class GitPullRule(CompoundRule):
	exported = False
	spec = "pull [<pull_options>]"
	extras = [pull_options]

	def value(self, node):
		return "pull " + recurse_values(node, [GitPullOption])
pull_rule = RuleRef(name="pull_rule", rule=GitPullRule())





git_command = Alternative(name='command', children=[
	add_rule,
	commit_rule,
	checkout_rule,
	push_rule,
	status_rule,
	log_rule,
	branch_rule,
	pull_rule,
	diff_rule,
])

class GitRule(CompoundRule):
	spec = 'git <command>'
	extras = [git_command]

	def process_recognition(self, node):
		self.value(node).execute()

	def value(self, node):
		cmd = node.children[0].children[0].children[1].children[0].children[0]
		value = Text('git ' + cmd.value())
		print('git ' + cmd.value())
		return value







merge_options = {
	'verbose': '-v',
}
merge_option_rep = Repetition(Choice(choices = merge_options), name='merge_options', joinWith=' ', min=0, max=2)

merge_rule = Compound(
	spec = "merge [<merge_options>]",
	extras = [merge_option_rep],
	value_func=lambda n, e: 'merge ' + e["merge_options"]
	)

rebase_options = {
	'continue': '--continue',
	'skip': '--skip',
	'abort': '--abort',
	'edit to do': '--edit-todo',
	'interactive': '-i',
}
rebase_option_rep = Repetition(Choice(choices = rebase_options), name='rebase_options', joinWith=' ', min=0, max=2)

rebase_rule = Compound(
	spec = "rebase [<rebase_options>]",
	extras = [rebase_option_rep],
	value_func=lambda n, e: 'rebase ' + e["rebase_options"]
	)


clone_rule = Compound(
	spec = 'clone ',
	extras = [],
	value_func = lambda n, e: 'clone ')


git_commands = [
	merge_rule,
	rebase_rule,
	clone_rule,
]

class GitRuleNew(MappingCountRule):
	mapping = aenea.configuration.make_grammar_commands('shared', {
		'git <command>': Text('git %(command)s'),
	})

	extras = [
		Alternative(children = git_commands, name = 'command')
	]
