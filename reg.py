import sys

pattern = '^[baka]*oli$'
match = 'oli'
debug = True

def tokenize(pattern):
    tokens = []
    alphabet = range(ord('a'), ord('z'))

    i = 0
    while i < len(pattern):
        cc = pattern[i]
        print i

        if ord(cc) in alphabet:
            tokens.append(['LETTER', cc])
        elif cc == '[':
            global i
            i += 1
            patt = ''
            while not pattern[i] == ']':
                patt += pattern[i]
                i += 1
                print i
            tokens.append(['BRACKET', patt])
        elif cc == '(':
            i += 1
            patt = ''
            while not pattern[i] == ']':
                patt += pattern[i]
                i += 1
            tokens.append(['PAREN', [tokenize(patt)]])
        elif cc == '*':
            tokens.append(['PZERO', [tokens.pop()]])
        elif cc == '+':
            tokens.append(['PONE', [tokens.pop()]])
        elif cc == '.':
            tokens.append(['WILDCARD'])
        elif cc == '$':
            tokens.append(['END'])
        elif cc == '^':
            tokens.append(['START'])
        i+=1
    return tokens

tokens = tokenize(pattern)
if debug:
    print 'pattern:', pattern, 'matchstring:', match
    print str(len(pattern)) + ' length pattern'
    for token in tokens:
        print token

if debug:
    print 'matching'


def matches(match, tokens):
    print 'comparing',tokens,'to',match
    index = 0
    for tsplit in tokens:
        if tsplit[0] == 'LETTER':
            letter = tsplit[1]
            if letter == match[index]:
                if debug:
                    print 'matched', letter
                index += 1
            else:
                print 'FAILED to match', letter, 'to', match[index]
                return False
        elif tsplit[0] == 'WILDCARD':
            index += 1
        elif tsplit[0] == 'BRACKET':
            print 'considering BRACKET'
            target = tsplit[1]
            print 'bracket',target,'matching',match[index]

            if match[index] in target:
                print 'bracket matched', target, 'to', match[index]
                index += 1
            else:
                print 'FAILED to be in bracket'
                return False
        elif tsplit[0] == 'PONE':
            target = tsplit[1]
            if matches(match[index], target):
                while index < len(match) and matches(match[index], target):
                    index += 1
                    if debug:
                        print 'pone matched', target
            else:
                print 'FAILED pone target not matched!'
                return False
        elif tsplit[0] == 'PZERO': # Kleene star
            target = tsplit[1]
            print 'tokenpattern',target
            print 'entering pzero'
            while index < len(match) - 1 and matches(match[index], target) == True:
                index += 1
                if debug:
                    print 'pzero matched', target
        elif tsplit[0] == 'START':
            if not index == 0:
                print 'FAILED not at start'
                return False
        elif tsplit[0] == 'END':
            if not index >= len(match):
                print 'FAILED not at end'
                return False

    print 'SUCCESS'
    return True

matches(match, tokens)

