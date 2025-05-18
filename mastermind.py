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
    time_end = process_time()
    print(f'Time taken: {time_end - time_start} seconds.')

    return


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        command_line = input(f'enter command line for {app_name}: ')
        argv.extend(command_line.split())
    main(argv[1:])