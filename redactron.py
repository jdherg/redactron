import re
import argparse
import sys


def redact_word(word):
    if len(word) < 2:
        return word
    return word[0] + 'x' * (len(word) - 1)


def redact_phrase(phrase, redactions):
    result = phrase
    words = set(re.split('\W+', phrase))
    in_phrase = words & redactions
    for redaction in in_phrase:
        result = re.sub('(?<=\W)' + redaction + '(?=\W)',
                        redact_word(redaction), result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin)
    parser.add_argument('output_file', type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout)
    args = parser.parse_args()
    lines = args.input_file.readlines()
    words = set()
    for line in lines:
        words |= set(re.split('\W+', line))
    upcase = [word for word in words if len(word) and word[0].isupper()]
    only_up = [word for word in upcase if word.lower() not in words]
    for line in lines:
        print(redact_phrase(line, set(only_up)), file=args.output_file)

if __name__ == '__main__':
    main()
