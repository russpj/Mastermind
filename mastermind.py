#!/usr/bin/python3

# Mastermind
'''Something like Invicta Mastermind'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time
from random import randint, choice


app_name = 'mastermind.py'

standard_colors = [
    "R",
    "B",
    "Y",
    "G",
    "P",
    "W"
]

class Score:
    def __init__(self, num_right, num_almost_right):
        self.num_right = num_right
        self.num_almost_right = num_almost_right
        return

    
class Guess:
    def __init__(self, colors):
        self.colors = colors
        return
    
def score_guess(guess, code):
    if len(guess) != len(code):
        return
    num_right = 0
    num_almost_right = 0
    spot_guess_used = [False]*len(guess)
    spot_code_used = [False]*len(code)
    for index in range(len(guess)):
        if guess[index] == code[index]:
            num_right += 1
            spot_guess_used[index] = True
            spot_code_used[index] = True
    for guess_index in range(len(guess)):
        for code_index in range(len(code)):
            if not spot_guess_used[guess_index] and not spot_code_used[code_index]:
                if guess[guess_index] == code[code_index]:
                    num_almost_right += 1
                    spot_guess_used[guess_index] = True
                    spot_code_used[code_index] = True
    return (num_right, num_almost_right)


class Board:
    def __init__(self, num_colors, num_spots):
        self.num_colors = num_colors
        self.num_spots = num_spots
        self.guesses = []
        self.scores = []
        self.code = []
        if num_colors <= 6:
            self.colors = standard_colors[:num_colors]
        else:
            self.colors = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")[:num_colors]
        return

    def codes(self):
        num_spots = self.num_spots
        num_colors = self.num_colors
        indices = [0]*num_spots
        while True:
            yield tuple([self.colors[indices[i]] for i in range(num_spots)])
            for index_position in [num_spots-i-1 for i in range(num_spots)]:
                indices[index_position] += 1
                if indices[index_position] < num_colors:
                    break
                indices[index_position] = 0
            if indices == [0]*num_spots:
                return

    

class Solver:
    def __init__(self, board):
        self.board = board
        self.compute_valid_candidates()
        return
    
    def compute_valid_candidates(self):
        self.candidates = set()
        self.candidates = {code for code in self.board.codes()}
        return

    def guess(self):
        if self.candidates:
            return choice(list(self.candidates))
        return None
    
    def remove_candidates(self, guess, score):
        for candidate in self.candidates:
            if  score_guess(guess, candidate) != score:
                self.candidates.remove(candidate)
    

def play_as_player(board, debug):
    print('How about a nice game of Mastermind?')
    print(f"I'm thinking of {board.num_spots} spots made up of {board.num_colors} colors.")
    print("You can use the letters ", end='')
    for color in board.colors:
        print(color, end='')
    print(" for your guesses.")

    code = []
    for _ in range(board.num_spots):
        code.append(board.colors[randint(0,board.num_colors-1)])
    if debug:
        print(f'The secret code is {code}')
    board.code = code

    num_right = 0
    count_guess = 0
    while num_right != board.num_spots:
        guess_is_valid = False
        while not guess_is_valid:
            guess_string = input("What is your guess? ")
            guess = list(guess_string.upper())
            count_guess += 1
            guess_is_valid = True
            for color in guess:
                if color not in board.colors:
                    print(f"{color} is not a valid color")
                    guess_is_valid = False
        num_right, num_almost_right = score_guess(guess, board.code)
        print(f"Guess: {''.join(guess)}, Score: {num_right}, {num_almost_right}")
    print(f"Congratulations. You solved it in {count_guess} guesses.")

    return


def play_as_computer(board, debug):
    solver = Solver(board)
    num_guesses = 0
    while solver.candidates:
        if debug:
            print(f'Out of {len(solver.candidates)} candidates ', end='')
        num_guesses += 1
        guess = solver.guess()
        score = input(f"I guess {''.join(guess)}. What is my score? ")
        score_right, score_almost_right = (int(num) for num in score.split(','))
        if score_right == board.num_spots:
            print(f'I got it in {num_guesses} tries!')
            return
        solver.remove_candidates(guess, (score_right, score_almost_right))
    print (f"I couldn't get it after {num_guesses} tries. It was too hard.")
    return


def main(arguments):
    program_name = app_name
    command_line_documentation = f'{program_name} --help --verbose --player [Person|Computer] --colors num_colors --spots num_spots'
    verbose = False
    player = 'P'
    num_colors = 6
    num_spots = 4
    input_file_name = ''
    sections = []

    try:
        opts, args = getopt(arguments, "hvp:c:d:", 
                            ("help", "verbose", "player=", "colors=", "spots="))
    except GetoptError:
        print(f'Invalid Arguments: {command_line_documentation}')
        exit(2)

    for opt, arg in opts:	
        if opt in ('-h', '--help'):
            print(f'usage: {command_line_documentation}')
            exit(0)

        if opt in ('-v', '--verbose'):
            verbose = True

        if opt in ('-p', '--player'):
            if arg[0] == 'c' or arg[0] == 'C':
                player = 'C'

        if opt in ('-c', '--colors'):
            num_colors = int(arg)
            if num_colors > 26:
                num_colors = 26

        if opt in ('-d', '--spots'):
            num_spots = int(arg)

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')

    time_start = process_time()
    print(f'{player} will play with {num_spots} spots of {num_colors} colors.')

    board = Board(num_colors, num_spots)
    if verbose:
        print(f"The test score is {score_guess(['W', 'B', 'W', 'B'], ['R', 'W', 'B', 'P'])}")
        print(f'The colors are {board.colors}')
    if player == 'P':
        play_as_player(board, verbose)
    else:
        play_as_computer(board, verbose)
    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])