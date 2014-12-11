import re
import argparse
import sys


def redact_word(word):
    if len(word) < 2:
        return word
    return word[0] + 'x' * (len(word) - 1)


def reverse_word(word):
    return word[::-1]


def redact_positionally(text, positions, redaction_method=redact_word):
    for position in positions:
        (start, stop) = position
        text = text[:start] + redaction_method(text[start:stop]) + \
            text[stop:]
    return text


def redact_set(text, redaction_set, redaction_method=redact_word):
    words = set(re.split('\W+', text))
    in_phrase = words & redaction_set
    for redaction in in_phrase:
        text = re.sub('\\b' + redaction + '\\b',
                      redaction_method(redaction), text)
    return text


def redact_properish(text, redaction_method=redact_word):
    words = set(re.split('\W+', text))
    upcase = {word for word in words if len(word) and word[0].isupper()}
    only_up = {word for word in upcase if word.lower() not in words}
    return redact_set(text, only_up)


def redact(text, target_method=redact_properish, redaction_method=redact_word):
    return target_method(text, redaction_method=redaction_method)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin)
    parser.add_argument('output_file', type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout)
    args = parser.parse_args()
    input_text = args.input_file.read()
    print(redact(input_text), file=args.output_file)
if __name__ == '__main__':
    main()
