from random import randint
import re


digit_strings = {
    0: 'zero',
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine'
}


def emojify(string):
    emojis = ''
    for item in string:
        if item.isalpha():
            emojis += ':regional_indicator_%s:' % item.lower()
        elif item.isdigit():
            emojis += ':%s:' % digit_strings[int(item)]
        elif item == ' ':
            emojis += '   '
        else:
            raise ValueError()
    return emojis


def get_random_text(length):
    chars = ''
    for _ in range(length):
        cc = randint(33, 126)
        chars += chr(cc)
    return chars


def pastify(string):
    emojis = [":joy:", ":ok_hand:", ":gun:", ":clap:", ":wave:", ":100:", ":eyes:", ":poop:", ":pray:"]
    str_array = string.split(' ')
    for _ in range(0, randint(0, len(str_array) * 4)):
        str_array.insert(randint(0, len(str_array) - 1), emojis[randint(0, len(emojis) - 1)])
    return re.sub(r'[bB]', ':b:', ' '.join(str_array))
