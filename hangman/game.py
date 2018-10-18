from .exceptions import *
from random import choice


class GuessAttempt(object):

    # Setting up hit/miss logic for guesses.

    def __init__(self, attempt, hit=None, miss=None):

        self.attempt = attempt
        self.hit = hit
        self.miss = miss

        if self.hit == True and self.miss == True:
            raise InvalidGuessAttempt()

    def is_hit(self):

        if self.hit:
            return True

        if self.miss:
            return False

    def is_miss(self):

        if self.miss:
            return True

        if self.hit:
            return False


class GuessWord(object):

    # Checks for valid words, raising exceptions if not. Then checks for letters guessed as well as
    # controlling the case of the letter.

    def __init__(self, a_word):
        a_word = a_word.lower()

        if not a_word:
            raise InvalidWordException()

        self.answer = a_word
        self.masked = '*' * len(a_word)

    def perform_attempt(self, letter):

        letter = letter.lower()

        if len(letter) > 1:
            raise InvalidGuessedLetterException

        if letter in self.answer:
            attempt = GuessAttempt(letter, hit=True, miss=False)

        if letter not in self.answer:
            attempt = GuessAttempt(letter, hit=False, miss=True)

        index = 0
        new_masked = ''
        for char in self.answer:

            if char == letter:
                new_masked += letter
            else:
                new_masked += self.masked[index]
            index += 1

        self.masked = new_masked
        return attempt


class HangmanGame(object):

    # Setting the default word list using the same default list as last time.

    WORD_LIST = ['rmotr', 'python', 'awesome']

    # Initializing with selection of a word from the list of words as well as setting number of guesses.

    def __init__(self, list_of_words=WORD_LIST, number_of_guesses=5):

        self.list_of_words = list_of_words
        self.number_of_guesses = number_of_guesses
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(self.select_random_word(list_of_words))

    # Class method selecting a random word and a check that the word is valid using an exception.

    @classmethod
    def select_random_word(cls, list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException
        return choice(list_of_words)

    # Function checking if the game is finished then checking the word for the guessed letter as well as
    # decrementing guess count for incorrect misses and checking that, raising an exception for losing
    # the game if it hits 0.

    def guess(self, letter):

        if self.is_won() or self.is_lost():
            raise GameFinishedException()

        letter = letter.lower()
        self.word.perform_attempt(letter)
        self.previous_guesses.append(letter)

        if self.word.perform_attempt(letter).is_miss():
            self.remaining_misses -= 1

        if self.word.answer == self.word.masked:
            raise GameWonException()

        if self.remaining_misses == 0:
            raise GameLostException()

        return self.word.perform_attempt(letter)

    # Checks for win/loss/finish

    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False

    def is_lost(self):
        if self.remaining_misses == 0:
            return True
        return False

    def is_finished(self):
        if self.word.answer == self.word.masked or self.remaining_misses == 0:
            return True
        return False
