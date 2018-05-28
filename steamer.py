#! /usr/bin/env python
import sys

def open_file(filename):
    with open(filename, 'r') as f:
        contents = f.read()
    return contents

def lexer(data):
    tok = ''
    string = ''
    tokens = []
    lines = data.split('\n')

    filecontents = []
    for line in lines:
        filecontents.extend(list(line))

    initial_token = ''.join(filecontents[0:12])
    if initial_token != 'well seymour':
        raise ValueError('The house is on fire!')

    filecontents = filecontents[12:]

    print('-------------------------\n  steaming your ham...\n-------------------------\n')

    state = 0

    # for char in filecontents:
    i = 0
    while i < len(filecontents):
        char = filecontents[i]
        tok += char
        # print(tok)
        if tok == 'auroraBorealis ':
            tokens.append('PRINT')
            tok = ''
        elif tok == '"':
            if state == 0:
                state = 1
            elif state == 1:
                tokens.append('STRING:{}'.format(string))
                string = ''
                state = 0
            tok = ''
        elif state == 1:
            string += char
            tok = ''
        elif tok == 'albanyexp ':
            tokens.append('ASSIGNMENT')
            i += 1
            char = filecontents[i]

            var_name = ''
            while char != ' ':
                var_name += filecontents[i]
                i += 1
                char = filecontents[i]

            while char == ' ' or char == '=':
                i += 1
                char = filecontents[i+1]

            tokens.append('VARIABLE:{}'.format(var_name))

            tok = ''
        elif tok == 'you steam a good ham':
            tokens.append('END_EXECUTION')

        i += 1
    print(tokens)
    return tokens

def parse(tokens):

    local_vars = {}

    for i, token in enumerate(tokens):
        if token == 'PRINT':
            next_tkn = tokens[i + 1]

            if 'STRING' in next_tkn:
                string = next_tkn.split(':')[1]

                # Actually print out the text
                print(string)
            else:
                raise ValueError('Implement printing of non strings')

        elif token == 'ASSIGNMENT':
            pass
        elif token == 'END_EXECUTION':
            print('\n----------------------------------------------\n   That was truly an unforgettable luncheon\n----------------------------------------------')
            sys.exit()

def run():
    """ Main entry point to the steamed hams interpreter """
    data = open_file(sys.argv[1])
    tokens = lexer(data)
    parse(tokens)

run()
