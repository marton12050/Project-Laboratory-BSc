import re


def valid_regex(regex):
    try:
        re.compile(regex)
        return True
    except re.error:
        print("Invalid regex")
        raise SyntaxError