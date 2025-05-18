#!/usr/bin/python3

# Mastermind
'''Something like Invicta Mastermind'''


from sys import stdin, stdout, stderr, argv
from getopt import getopt, GetoptError
from time import process_time


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
    dot_guess_used = [False]*len(guess)
    dot_code_used = [False]*len(code)
    for index in range(len(guess)):
        if guess[index] == code[index]:
            num_right += 1
            dot_guess_used[index] = True
            dot_code_used[index] = True
    for guess_index in range(len(guess)):
        for code_index in range(len(code)):
            if not dot_guess_used[guess_index] and not dot_code_used[code_index]:
                if guess[guess_index] == code[code_index]:
                    num_almost_right += 1
                    dot_guess_used[guess_index] = True
                    dot_code_used[code_index] = True
    return (num_right, num_almost_right)


class Board:
    def __init__(self, num_colors, num_dots):
        self.num_colors = num_colors
        self.num_dots = num_dots
        self.guesses = []
        self.scores = []
        self.code = []
        self.candidates = self.compute_valid_candidates()
        return
    
    def compute_valid_candidates(self):
        return set()
    

def main(arguments):
    program_name = app_name
    command_line_documentation = f'{program_name} --help --verbose --player [Person|Computer] --colors num_colors --dots num_dots'
    verbose = False
    player = 'P'
    num_colors = 6
    num_dots = 4
    input_file_name = ''
    sections = []

    try:
        opts, args = getopt(arguments, "hvp:c:d:", 
                            ("help", "verbose", "player=", "colors=", "dots="))
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

        if opt in ('-d', '--dots'):
            num_dots = int(arg)

    if input_file_name:
        with open(input_file_name, 'r') as input_file:
            print(f'Opened {input_file_name} for {app_name}')

    time_start = process_time()
    print(f'{player} will play with {num_dots} dots of {num_colors} colors.')
    if num_colors <= 6:
        colors = standard_colors[:num_colors]
    else:
        colors = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")[:num_colors]
    if verbose:
        print(f'The colors are {colors}')

    board = Board(num_colors, num_dots)
    if verbose:
        print(f'The board has {len(board.candidates)} candidates.')
        print(f"The test score is {score_guess(['W', 'B', 'W', 'B'], ['R', 'W', 'B', 'P'])}")
    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])