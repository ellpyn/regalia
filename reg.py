import sys

pattern = 'he.*$'
match = 'helloooooor'
debug = False

def tokenize(pattern):
    tokens = []
    alphabet = range(ord('a'), ord('z'))

    for i in range(0, len(pattern)):
        cc = pattern[i]

        if ord(cc) in alphabet:
            tokens.append(['LETTER', cc])
        elif cc == '*':
            prev = pattern[i - 1]
            tokens.pop()
            tokens.append(['PZERO', prev])
        elif cc == '+':
            prev = pattern[i - 1]
            tokens.pop()
            tokens.append(['PONE', prev])
        elif cc == '.':
            tokens.append(['WILDCARD'])
        elif cc == '$':
            tokens.append(['END'])
        elif cc == '^':
            tokens.append(['START'])
    return tokens

tokens = tokenize(pattern)
if debug:
    print 'pattern:', pattern, 'matchstring:', match
    print str(len(pattern)) + ' length pattern'
    for token in tokens:
        print token

index = 0
if debug:
    print 'matching'
for tsplit in tokens:
    if tsplit[0] == 'LETTER':
        letter = tsplit[1]
        if letter == match[index]:
            if debug:
                print 'matched', letter
            index += 1
        else:
            print 'FAILED to match', letter
            sys.exit(0)
    elif tsplit[0] == 'WILDCARD':
        index += 1
    elif tsplit[0] == 'PONE':
        target = tsplit[1]
        if match[index] == target:
            while match[index] == target:
                index += 1
                print 'pone matched', target
        else:
            print 'FAILED pone target not matched!'
            sys.exit(0)
    elif tsplit[0] == 'PZERO':
        target = tsplit[1]
        while match[index] == target:
            index += 1
            if debug:
                print 'pzero matched', target
    elif tsplit[0] == 'START':
        if not index == 0:
            print 'FAILED not at start'
            sys.exit(0)
    elif tsplit[0] == 'END':
        if not index == len(match):
            print 'FAILED not at end'
            sys.exit(0)
print 'SUCCESS'
