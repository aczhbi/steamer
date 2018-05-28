#! /usr/bin/env python
import sys
from itertools import islice
import collections

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
    # TODO convert to iters method used below
    file_iter = iter(enumerate(filecontents))
    for i, char in file_iter:
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
            _, char = get_next(file_iter)

            var_name = ''
            while char != ' ':
                var_name += char
                _, char = get_next(file_iter)

            while char != '=':
                _, char = get_next(file_iter)

            _, char = get_next(file_iter)
            if char != ' ':
                raise ValueError('Space required after equals')

            tokens.append('VARIABLE:{}'.format(var_name))

            tok = ''
        elif tok == 'you steam a good ham':
            tokens.append('END_EXECUTION')

        i += 1

    return tokens

def parse(tokens):

    local_vars = {}
    const_vars = {}

    token_iter = iter(enumerate(tokens))
    for i, token in token_iter:
        if token == 'PRINT':
            next_tkn = tokens[i + 1]

            if 'STRING' in next_tkn:
                string = next_tkn.split(':')[1]

                # Actually print out the text
                print(string)
            else:
                raise ValueError('Implement printing of non strings')

        elif token == 'ASSIGNMENT':
            _, token = get_next(token_iter)
            tok_type, var_name = token.split(':')
            # TODO check tok_type is VARIABLE
            _, tok = get_next(token_iter)
            tok_type, val = tok.split(':')
            # TODO check the tok_type
            local_vars[var_name] = val

        elif token == 'END_EXECUTION':
            print('\n----------------------------------------------\n   That was truly an unforgettable luncheon\n----------------------------------------------')
            sys.exit()

def run():
    """ Main entry point to the steamed hams interpreter """
    data = open_file(sys.argv[1])
    tokens = lexer(data)
    parse(tokens)

def consume(iterator, n):
    "Advance the iterator n-steps ahead. If n is none, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)

def get_next(iterator):
    return next(iterator)

run()

