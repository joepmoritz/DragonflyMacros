# This file is part of Aenea
#
# Aenea is free software: you can redistribute it and/or modify it under
# the terms of version 3 of the GNU Lesser General Public License as
# published by the Free Software Foundation.
#
# Aenea is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with Aenea.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (2014) Alex Roper
# Alex Roper <alex@aroper.net>

'''The vocabulary module provides control of dynamic and static
vocabulary.  These are user-configurable mappings of phrases to
actions that can be dynamically updated and en/dis-abled on demand,
and shared across modules.


_vocabulary holds whatever is loaded from JSON,
but with shortcuts/text changed to dragonfly functions

_lists holds result of merging and tag checking of _vocabulary items.
This means it depends on active window title/exe.
Dynamic updates every time you speak, static only when you change JSON.
This means the word list is cleared and every word re-added every time,
all the way down to Dragon.

Optimization: clear dynamic _lists when JSON changes, but not when you speak.
Instead, rebuild the list in a temp var, then compare the keys (values not needed)
If any removed, clear list and update all. If any added, only add those keys.

Alternative opt: only update _lists when win title/exe changes


'''

import re

# from aenea.lax import (
#     Text,
#     Key
#     )

from dragonfly import Text, Key

from wrappers import NoAction

from aenea.proxy_actions import ProxyMousePhantomClick as MousePhantomClick


try:
    import dragonfly
    from dragonfly import (
        Pause,
        Mimic
        )
except ImportError:
    import dragonfly_mock as dragonfly
    # TODO: mock this better

    class ActionMock(object):
        def __init__(self, *a, **kw):
            pass

        def __add__(self, other):
            return self

    class Text(ActionMock):
        pass

    class Pause(ActionMock):
        pass

    class Mimic(ActionMock):
        pass

    class MousePhantomClick(ActionMock):
        pass

    class NoAction(ActionMock):
        pass

    class Key(ActionMock):
        pass

import aenea.config
import aenea.configuration

_vocabulary = {'static': {}, 'dynamic': {}}

# dynamic only
_disabled_vocabularies = set()

# Hack because Dragonfly is weird about when you can clear a DictList.
# We have native dicts store the data, and sync to whichever DictList
# most recently was registered. This is necessary so grammars can be
# reloaded with mic off/on. We store static the same way for simplicity.
_lists = {'static': {}, 'dynamic': {}}

# mapping from inhibited_vocab_name to list of (inhibit_context, inhibiting_grammar)
_vocabulary_inhibitions = {}

# global DictList that takes inhibitions into account. Reserved for _vocabulary.
_global_list = None

# global List that lists all dynamic vocabularies. Reserved for _vocabulary.
_list_of_dynamic_vocabularies = None

_watchers = {
    'dynamic': aenea.configuration.ConfigDirWatcher(('vocabulary_config', 'dynamic')),
    'static': aenea.configuration.ConfigDirWatcher(('vocabulary_config', 'static'))
    }

_enabled_watcher = aenea.configuration.ConfigWatcher(('vocabulary_config', 'enabled'))

_window_title_tags = {}
_window_executable_tags = {}
_last_window_title_tags = set()
_last_window_executable_tags = set()


def get_context():
    # return aenea.proxy_contexts._get_context()
    win = aenea.config.get_window_foreground()
    return {'title': win.title, 'executable': win.executable}

def get_window_title_tags(context):
    if 'title' not in context:
        return

    for tag, texts in _window_title_tags.iteritems():
        if any(text.lower() in context['title'].lower() for text in texts):
            yield tag
    
def get_window_executable_tags(context):
    if 'executable' not in context:
        return

    for tag, texts in _window_executable_tags.iteritems():
        if any(text.lower() in context['executable'].lower() for text in texts):
            yield tag

def window_tags_have_changed():
    # context = aenea.proxy_contexts._get_context()
    context = get_context()
    return (_last_window_title_tags != set(get_window_title_tags(context))
        or _last_window_executable_tags != set(get_window_executable_tags(context)))


def refresh_vocabulary(force_reload=False):
    '''Reloads all static and dynamic vocabulary files, if any have changed
       since they were last read. Note that changes to a static file will not
       be active until the grammar is reloaded (in practice, Dragon restarted
       unless you change the grammar file and turn mic off then on).

       Also updates the active lists, so you'll need to call this whenever the
       context changes if you want the global inhibitions to update.

       The module _vocabulary.py includes a rule to call this whenever the user
       starts to say anything.'''
    global _vocabulary

    vocabularies_have_changed = any(w.refresh() for w in _watchers.itervalues())

    if force_reload or vocabularies_have_changed:
        for vocabulary in 'static', 'dynamic':
            for kind in _vocabulary[vocabulary].itervalues():
                del kind[:]

            for (fn, watcher) in _watchers[vocabulary].files.iteritems():
                watcher.refresh()
                vox = watcher.conf
                if isinstance(vox, dict):
                    vox = [vox]
                for v in vox:
                    print('reloading vocabulary %s' % v['name'])
                    for window_title in v.get('window_titles', []):
                        v['tags'].append(window_title)
                        add_window_title_tag(window_title, window_title)
                        # print('added window title tag: %s' % window_title)

                    _update_one_vocabulary(
                        vocabulary,
                        v['name'],
                        v['tags'],
                        v.get('vocabulary', {}),
                        v.get('shortcuts', {})
                        )
            _rebuild_lists('static')

    _load_enabled_from_disk()

    if window_tags_have_changed() or force_reload or vocabularies_have_changed:
        _rebuild_lists('dynamic')


def _load_enabled_from_disk():
    '''Sets the set of enabled grammars from the disk file.'''
    if _enabled_watcher.refresh():
        disabled = set()
        for (name, status) in _enabled_watcher.conf.iteritems():
            if not status:
                disabled.add(name)
        _disabled_vocabularies.clear()
        _disabled_vocabularies.update(disabled)
        _enabled_watcher.write()


def _save_enabled_to_disk():
    _enabled_watcher.conf.clear()
    for name in _vocabulary['dynamic']:
        _enabled_watcher.conf[name] = name not in _disabled_vocabularies
    _enabled_watcher.write()


def _rebuild_lists(vocabulary):
    global _disabled_vocabularies
    global _global_list
    global _lists
    global _vocabulary_inhibitions
    global _list_of_dynamic_vocabularies
    global _last_window_title_tags, _last_window_executable_tags

    context = get_context()
    context_title = context['title']
    context_executable = context['executable']

    if vocabulary == 'dynamic':
        # print "rebuilding lists dynamic %s" % context['title']
        if _global_list is not None:
            _global_list.clear()

    for t, dlist in _lists[vocabulary].iteritems():
        if dlist:
            dlist.clear()

    _last_window_title_tags = set(get_window_title_tags(context))
    _last_window_executable_tags = set(get_window_executable_tags(context))

    # print(_last_window_title_tags)
    # print(_last_window_executable_tags)

    for name, vocabs in _vocabulary[vocabulary].iteritems():
        for (tags, vocab) in vocabs:
            if name not in _disabled_vocabularies:
                if ('global' in tags and vocabulary == 'dynamic' and _global_list is not None):
                    global_inhibited = False
                    for tag in tags:
                        if any(c is None or c.matches(context_executable, context_title, None)
                                for (c, _) in _vocabulary_inhibitions.get(tag, [])):
                            global_inhibited = True
                            break
                    if not global_inhibited:
                        _global_list.update(vocab)

                has_any_window_title_tag = any([tag in _window_title_tags for tag in tags])
                has_any_executable_tag = any([tag in _window_executable_tags for tag in tags])

                has_correct_window_title_tag = all(
                    any(window_title_tag in context_title for window_title_tag in _window_title_tags[tag])
                    for tag in tags if tag in _window_title_tags
                )

                has_correct_executable_tag = any(
                    executable_tag.lower() in context_executable.lower()
                    for tag in tags if tag in _window_executable_tags
                    for executable_tag in _window_executable_tags[tag]
                )

                if (has_any_window_title_tag or has_any_executable_tag) and not (has_correct_window_title_tag or has_correct_executable_tag):
                    # print('Vocab %s does not have correct window_title given %s' % (name, context['title']))
                    break

                for tag in tags:
                    if vocabulary == 'static':
                        _lists[vocabulary].setdefault(tag, {})
                    # If it's dynamic, we'll build the list on
                    # demand when someone registers it, so do
                    # nothing here.
                    # print('Loading vocab %s for tag %s' % (name, tag))
                    if tag in _lists[vocabulary]:
                        _lists[vocabulary][tag].update(vocab)


    if _list_of_dynamic_vocabularies is not None:
        _list_of_dynamic_vocabularies.set(_vocabulary['dynamic'])


def get_static_vocabulary(tag):
    '''Returns a dict of string to dragonfly.ActionBase-derived.'''
    if tag not in _lists['static']:
        # Dragonfly chokes on unicode.
        _lists['static'][str(tag)] = {}
    return _lists['static'][str(tag)]


def unregister_dynamic_vocabulary(tag):
    '''Call this to unregister a dynamic vocabulary in the unload.'''
    global _lists
    _lists['dynamic'].pop(str(tag), None)
    _save_enabled_to_disk()


def register_dynamic_vocabulary(tag):
    '''Call this to register a dynamic vocabulary hook in your grammar that
       users can configure. It returns a DictList, which will always be
       kept up to date with user updates. You need to call unregister when
       the grammar is unloaded or your module won't successfully reload without
       restarting Dragon.'''
    global _lists
    _lists['dynamic'][str(tag)] = dragonfly.DictList('dynamic %s' % str(tag))
    refresh_vocabulary()
    _load_enabled_from_disk()
    _save_enabled_to_disk()
    return _lists['dynamic'][str(tag)]


def disable_dynamic_vocabulary(name):
    '''Disables all dynamic vocabularies with the specified name immediately.
       No reload or mic off/on is necessary.'''
    _load_enabled_from_disk()
    _disabled_vocabularies.add(name)
    _rebuild_lists('dynamic')
    _save_enabled_to_disk()


def enable_dynamic_vocabulary(name):
    '''Enables all dynamic vocabularies with the specified name immediately.
       No reload or mic off/on is necessary.'''
    _load_enabled_from_disk()
    if name in _disabled_vocabularies:
        _disabled_vocabularies.remove(name)
    _rebuild_lists('dynamic')
    _save_enabled_to_disk()


def register_global_dynamic_vocabulary():
    '''Returns a DictList of the global vocabulary. This is like all vocabs
       tagged 'global', EXCEPT grammars may inhibit a name from being here by
       calling inhibit_name_globally when a given context is active. This is
       intended to allow more complex editing grammars (eg, multiedit), which
       have their own custom hooks for vocabs which enable advanced features
       to avoid conflicting with the global grammar.

       Note that this is NOT the same as calling
       register_dynamic_vocabulary('global'); which will ignore inhibited
       vocabularies.'''
    global _global_list
    _global_list = dragonfly.DictList(name='global inhibited')
    refresh_vocabulary()
    return _global_list


def unregister_global_dynamic_vocabulary():
    '''Unregisters the global dynamic vocabulary. You need to call this in
       any grammar that registers it at unload if you want it to be reloadable
       without restarting Dragon.'''
    global _global_list
    _global_list = None


def inhibit_global_dynamic_vocabulary(grammar_name, tag, context=None):
    '''Ensures that whenever the specified context is active, all vocabularies
       with the specified tag(s) will not be active in the global dynamic
       vocabulary.'''
    global _vocabulary_inhibitions
    if isinstance(tag, basestring):
        _vocabulary_inhibitions.setdefault(tag, [])
        if (context, grammar_name) not in _vocabulary_inhibitions[tag]:
            _vocabulary_inhibitions[tag].append((context, grammar_name))
            _rebuild_lists('dynamic')
    else:
        for t in tag:
            inhibit_global_dynamic_vocabulary(grammar_name, t, context)


def uninhibit_global_dynamic_vocabulary(grammar_name, tag):
    '''Remove all inhibitions by grammar_name on specified tags.'''
    global _vocabulary_inhibitions
    if isinstance(tag, basestring):
        _vocabulary_inhibitions.setdefault(tag, [])
        _vocabulary_inhibitions[tag] = [
            (c, g) for (c, g) in _vocabulary_inhibitions[tag]
            if g != grammar_name
            ]
        _rebuild_lists('dynamic')
    else:
        for t in tag:
            uninhibit_global_dynamic_vocabulary(grammar_name, t)


def register_list_of_dynamic_vocabularies():
    global _list_of_dynamic_vocabularies
    _list_of_dynamic_vocabularies = dragonfly.List('list of vocabularies')
    # Don't rebuild here because the grammar may not yet have loaded.
    return _list_of_dynamic_vocabularies


def unregister_list_of_dynamic_vocabularies():
    global _list_of_dynamic_vocabularies
    _list_of_dynamic_vocabularies = None

def add_window_title_tag(window_title, tag):
    _window_title_tags.setdefault(tag, set())
    _window_title_tags[tag].add(window_title)

def add_window_executable_tag(window_executable, tag):
    _window_executable_tags.setdefault(tag, set())
    _window_executable_tags[tag].add(window_executable)

def _build_action(action):
    '''Processes a single custom dynamic grammar action.'''
    actions = {'Text': Text, 'Key': Key, 'Pause': Pause, 'Mimic': Mimic,
               'MousePhantomClick': MousePhantomClick, 'NoAction': NoAction}
    return actions[str(action['type'])](*map(str, action['args']))


def _build_action_list(command):
    '''Processes a list of custom dynamic grammar actions into a single
       dragonfly.ActionBase subclass.'''
    if len(command) == 0:
        return NoAction()
    else:
        agg = _build_action(command[0])
        for action in command[1:]:
            agg = agg + _build_action(action)
        return agg


def _parse_text(text):
    def action():
        while True:
            yield 'Text'
            yield 'Key'

    pieces = re.split(r'(?<!\\){{(.+?)(?<!\\)}}', text)
    return _build_action_list([{'type': t, 'args': [s.replace('\\{', '{')]} for t, s in zip(action(), pieces)])


def _update_one_vocabulary(vocabulary, name, tags, vocab, shortcuts):
    global _vocabulary

    this_chunk = {}
    for (dataset, default) in ((vocab, _parse_text), (shortcuts, Key)):
        for phrase, command in dataset.iteritems():
            if isinstance(command, basestring):
                this_chunk[str(phrase)] = default(str(command))
            else:
                this_chunk[str(phrase)] = _build_action_list(command)
    _vocabulary[vocabulary].setdefault(str(name), [])
    _vocabulary[vocabulary][str(name)].append((tags, this_chunk))

