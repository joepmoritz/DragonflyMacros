# Author: Joep Moritz <joep.moritz@gmail.com>

import aenea.config
import aenea.configuration
import aenea.misc
from aenea.vocabulary import add_window_executable_tag, add_window_title_tag, register_dynamic_vocabulary
import sound

from dragonfly import *
import dragonfly.log as log

from natlink import setMicState
from util import *
from SharedRules import *

from sikuli import dragonfly_proxy as sikuli

log.setup_log()


chrome_context = AppContext(executable='Chrome')
finder_context = AppContext(executable='explorer') | AppContext(title ='Save As') | AppContext(title ='Select Folder')
matlab_context = AppContext(executable='matlab')
sublime_context = AppContext(executable='sublime')
terminal_context = AppContext(executable='ConEmu64.exe')

all_context = None
other_context = ~chrome_context & ~finder_context & ~matlab_context & ~sublime_context & ~terminal_context

global_tags = ['global_stuff']

add_window_executable_tag('mspaint.exe', 'window_executable_paint')
add_window_executable_tag('keepass.exe', 'window_executable_keepass')
add_window_executable_tag('SumatraPDF.exe', 'window_executable_sumatra')
add_window_executable_tag('MendeleyDesktop.exe', 'window_executable_mendeley')
add_window_executable_tag('WINWORD.exe', 'window_executable_word')
add_window_executable_tag('SnippingTool.exe', 'window_executable_snipping_tool')
add_window_title_tag('COMMIT_EDITMSG - WordPad', 'window_title_commit_message_wordpad')
add_window_title_tag('COMMIT_EDITMSG - Notepad', 'window_title_commit_message_wordpad')
add_window_title_tag('Untitled - Notepad', 'window_title_untitled_notepad')
add_window_title_tag('Dictation', 'window_title_dictation')
add_window_title_tag('Dictate code', 'window_title_dictate_code')
add_window_title_tag('Dictate python', 'window_title_dictate_code')



def cancel_and_sleep(text=None, text2=None):
    """Used to cancel an ongoing dictation and puts microphone to sleep.

    This method notifies the user that the dictation was in fact canceled,
    with a sound and a message in the Natlink feedback window.
    Then the the microphone is put to sleep.
    Example:
    "'random mumbling go to sleep'" => Microphone sleep.

    """
    print("* Dictation canceled. Going to sleep. *")
    sound.play(sound.SND_SLEEP)
    setMicState("sleeping")


def wakeup():
  print("* Dictation on. *")
  sound.play(sound.SND_WAKE)
  setMicState("on")

class DragonRule(MappingRule):
    mapping = aenea.configuration.make_grammar_commands('dragon', {
      "[<text>] ([go to] sleep | cancel and sleep | snooze) [<text2>]": Function(cancel_and_sleep),
      'wake [up]': Function(wakeup),
    })
    extras = [DictateWords(name='text'), DictateWords(name='text2')]


class GlobalRepeatRule(RepeatRule):
    repeatables = CommonRepeatables() + [
        DictListRef('dynamic global', register_dynamic_vocabulary('global_stuff')),
    ]
    finishers = CommonFinishers()


grammar_all = Grammar('Global', context = all_context)
grammar_all.add_rule(ExecuteActionRule(element = DictListRef(sikuli.get_mapping('global'))))
# grammar_all.add_rule(DragonRule())
grammar_all.load()

grammar_other = Grammar('Global', context = other_context)
grammar_other.add_rule(GlobalRepeatRule())
# grammar_other.add_rule(DragonRule())
grammar_other.load()


def unload():
    global grammar_all
    global grammar_other

    for tag in global_tags:
        aenea.vocabulary.unregister_dynamic_vocabulary(tag)

    if grammar_all:
        grammar_all.unload()
    grammar_all = None

    if grammar_other:
        grammar_other.unload()
    grammar_other = None


