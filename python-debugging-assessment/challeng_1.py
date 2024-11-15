import random


def prompt_for_guess(srange: int, erange: int) -> int:
    """Prompt the player for a guess between two numbers: start and end.
    
    Args:
        srange: First guessable number.
        erange: Last guessable number.
    """
    try:
        return int(input(f'Guess a number between {srange} and {erange}: '))
    except ValueError:
        print('Your guess must be an integer. Example: 42')
        return prompt_for_guess(srange, erange)


def attempts(srange: int, erange: int, answer: int, prompt_callable: callable = prompt_for_guess) -> str:
    """A simple guessing game. Auto-generates a number between the start and end range.

    Args:
        srange: First guessable number.
        erange: Last guessable number.
        answer: Correct answer.
        prompt_callable: Callable used to prompt a user for their guess.
            - Must accept at least 2 positional arguments and return an int.
            - Default is prompt_for_guess.
    """
    # Until the player guesses correctly, they must keep guessing.
    while (guess := prompt_callable(srange, erange)) != answer:
        # Provide a hint.
        if guess > answer:
            yield '+'
        elif guess < answer:
            yield '-'
    else:
        yield '='


def start_game():
    """Play three games of 'guess the correct number'."""
    for _ in range(3):
        srange, erange = 1, 100
        answer = random.randint(srange, erange)

        for attempt in attempts(srange, erange, answer, prompt_for_guess):
            if attempt == '=':
                print(f'You win! {answer} is correct!')
                break  # Exit the current game loop.
            elif attempt == '+':
                print('Too high. Guess again.')
            elif attempt == '-':
                print('Too low. Guess again.')
            else:
                raise NotImplementedError(f'{attempt} is not an expected result of function: attempts')
    
    print('Thanks for playing!')


###############################################################################
#
# Application unit tests.
#
###############################################################################
import unittest
from unittest.mock import MagicMock, patch


class TestGuessingGame(unittest.TestCase):

    def test_prompt_for_guess(self):
        with patch('builtins.input') as input_patched:
            # Simulate valid inputs.
            input_patched.side_effect = '1 2 3'.split()
            self.assertEqual(prompt_for_guess(1, 3), 1)
            self.assertEqual(prompt_for_guess(1, 3), 2)
            self.assertEqual(prompt_for_guess(1, 3), 3)
            
            # Simulate invalid input followed by valid input.
            input_patched.side_effect = ['invalid', '4']
            with patch('builtins.print'):
                self.assertEqual(prompt_for_guess(1, 5), 4)

    def test_attempts(self):
        actual = list(attempts(1, 3, 2, MagicMock(side_effect=[1, 3, 2])))
        expect = '- + ='.split()
        self.assertEqual(actual, expect)


if __name__ == '__main__':
    unittest.main(verbosity=2)