import re
from dragonfly.grammar.elements import Repetition, Dictation

number_words = {
    'zero': 0,
    'one': 1,
    'do': 2,
    'to': 2,
    'two': 2,
    'free': 3,
    'three': 3,
    'for': 4,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'then': 10,
    'than': 10,
    'them': 10,
    'eleven': 11,
    'twelve': 12,
    'twelfth': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'sturdy': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90,
    'hundred': 100,
    'thousand': 1000,
    'million': 1000000,
    'billion': 1000000000
}


class DictateWords(Dictation):
    def __init__(self, name=None, min=1, max=10, default=None, format=True):
        Dictation.__init__(self, name=name, default=default)

# class DictateWords(Repetition):
#     def __init__(self, name=None, min=1, max=10, default=None, joinWith=' ', format=True):
#         Repetition.__init__(self, DictateWord(None, format), min, max, name, default, joinWith)


class DictateKnown(DictateWords):
    def __init__(self, words, min=1, max=10, name=None, default=None, format=True):
        DictateWords.__init__(self, name, min, max, default, format)
        self.words = words

    def decode(self, state):
        state.decode_attempt(self)

        # Check that at least one word has been dictated, otherwise feel.
        if state.rule() != "dgndictation" and state.rule() != "dgnwords":
            state.decode_failure(self)
            return

        # print "word: %s" % state.word()
        word = state.word()
        if word is not None:
            word = word.split('\\', 1)[0].replace('-', '')

        # Check that at least the first word is a known word
        if word not in self.words:
            state.decode_failure(self)
            return

        # Determine how many words have been dictated.
        count = 1
        word = state.word(count)
        if word is not None:
            word = word.split('\\', 1)[0].replace('-', '')

        while (state.rule(count) == "dgndictation" or state.rule(count) == "dgnwords") and word in self.words:
            count += 1
            word = state.word(count)
            if word is not None:
                word = word.split('\\', 1)[0].replace('-', '')

        state.next(count)
        state.decode_success(self)
        yield state

        # None of the possible states were accepted, failure.
        state.decode_failure(self)
        return


def spoken_word_to_number(n):
    """Assume n is a positive integer".
assert _positive_integer_number('nine hundred') == 900
assert spoken_word_to_number('one hundred') == 100
assert spoken_word_to_number('eleven') == 11
assert spoken_word_to_number('twenty two') == 22
assert spoken_word_to_number('thirty-two') == 32
assert spoken_word_to_number('forty two') == 42
assert spoken_word_to_number('two hundred thirty two') == 232
assert spoken_word_to_number('two thirty two') == 232
assert spoken_word_to_number('nineteen hundred eighty nine') == 1989
assert spoken_word_to_number('nineteen eighty nine') == 1989
assert spoken_word_to_number('one thousand nine hundred and eighty nine') == 1989
assert spoken_word_to_number('nine eighty') == 980
assert spoken_word_to_number('nine two') == 92 # wont be able to convert this one
assert spoken_word_to_number('nine thousand nine hundred') == 9900
assert spoken_word_to_number('one thousand nine hundred one') == 1901
"""

    n = n.lower().strip()
    if n in number_words:
        return number_words[n]
    else:
        inputWordArr = re.split('[ -]', n)

    # assert len(inputWordArr) > 1 #all single words are known

    # Check the pathological case where hundred is at the end or thousand is at end
    if inputWordArr[-1] == 'hundred':
        inputWordArr.append('zero')
        inputWordArr.append('zero')
    if inputWordArr[-1] == 'thousand':
        inputWordArr.append('zero')
        inputWordArr.append('zero')
        inputWordArr.append('zero')
    if inputWordArr[0] == 'hundred':
        inputWordArr.insert(0, 'one')
    if inputWordArr[0] == 'thousand':
        inputWordArr.insert(0, 'one')

    inputWordArr = [word for word in inputWordArr if word not in ['and', 'minus', 'negative']]
    currentPosition = 'unit'
    prevPosition = None
    output = 0

    for word in reversed(inputWordArr):
        if word not in number_words:
            pass
        elif currentPosition == 'unit':
            number = number_words[word]
            output += number
            if number > 9:
                currentPosition = 'hundred'
            else:
                currentPosition = 'ten'
        elif currentPosition == 'ten':
            if word != 'hundred':
                number = number_words[word]
                if number < 10:
                    output += number*10
                else:
                    output += number
            # else: nothing special
            currentPosition = 'hundred'
        elif currentPosition == 'hundred':
            if word not in ['hundred', 'thousand']:
                number = number_words[word]
                output += number*100
                currentPosition = 'thousand'
            elif word == 'thousand':
                currentPosition = 'thousand'
            else:
                currentPosition = 'hundred'
        elif currentPosition == 'thousand':
            # assert word != 'hundred'
            if word != 'thousand':
                number = number_words[word]
                output += number*1000
        # else:
        #   assert "Can't be here" == None

    return(output)


class DictateMapping(DictateKnown):
    def __init__(self, words, min=1, max=10, name=None, default=None, format=True):
        DictateKnown.__init__(self, words, min, max, name, default, format)

    def value(self, node):
        words = [word if word not in self.words else self.words[word] for word in node.words()]
        dc = node.engine.DictationContainer(words)
        return str(dc)


class DictateMappingWithIntegers(DictateMapping):
    def value(self, node):
        i = 0
        words = []
        node_words = node.words()
        while i < len(node_words):
            word = node_words[i]

            if word in number_words:
                nwords = []
                while word in number_words:
                    nwords.append(word)
                    i = i + 1
                    word = node_words[i]
                number = spoken_word_to_number(str(node.engine.DictationContainer(nwords)))
                words.append(number)

            elif word in self.words:
                words.append(self.words[word])

            else:
                words.append(word)

        dc = node.engine.DictationContainer(words)
        return str(dc)


class DictInteger(DictateKnown):

    def __init__(self, name=None, optional=False, default=None):
        min = 0 if optional else 1
        DictateKnown.__init__(self, number_words, min, 10, name, default, True)

    def value(self, node):
        dc = node.engine.DictationContainer(node.words())
        return spoken_word_to_number(str(dc))
        # return node.engine.DictationContainer(node.words())
