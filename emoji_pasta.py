"""Provides functions to emojii-fy text"""

import re

num_to_word = {
'1': 'one',
'2': 'two',
'3': 'three',
'4': 'four',
'5': 'five',
'6': 'six',
'7': 'seven',
'8': 'eight',
'9': 'nine',
'0': 'zero',
}


def emojify_character(char):
    res = re.match('\d', char)
    if res:
        return ':' + num_to_word[res.group(0)] + ':'
    return ':' + char + ':'

def emojify_word(word):
    return ''.join(map(emojify_character, list(word)))

def emojifier(line):
    return ' '.join(map(emojify_word, line.split(' ')))

if __name__ == "__main__":
    print(emojifier("t3st ish"))
