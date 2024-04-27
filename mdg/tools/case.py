#!/usr/bin/python
"""
String convert functions
"""

from __future__ import annotations
import re


def camelcase(string:str) -> str:
    if string is None or string == "":
        return string
    words: list = re.split(' |_', string.strip(' _'))
    
    # Can't use Title function in str library as this lowers all but the first char: does not handle existing camelCased input
    words_camel: list = [(words[0][0].lower() + words[0][1:])] + list(word[0].upper() + word[1:] for word in words[1:])
    return "".join(words_camel)


def capitalcase(string: str) -> str:
    """Convert string into capital case.
    First letters will be uppercase.

    Args:
        string: String to convert.

    Returns:
        string: Capital case string.

    """

    string = str(string)
    if not string:
        return string
    return uppercase(string[0]) + string[1:]


def constcase(string: str) -> str:
    """Convert string into upper snake case.
    Join punctuation with underscore and convert letters into uppercase.

    Args:
        string: String to convert.

    Returns:
        string: Const cased string.

    """

    return uppercase(snakecase(string))


def lowercase(string: str) -> str:
    """Convert string into lower case.

    Args:
        string: String to convert.

    Returns:
        string: Lowercase case string.

    """

    return str(string).lower()


def pascalcase(string: str) -> str:
    """Convert string into pascal case.

    Args:
        string: String to convert.

    Returns:
        string: Pascal case string.

    """
    return capitalcase(camelcase(string))


def pathcase(string: str) -> str:
    """Convert string into path case.
    Join punctuation with slash.

    Args:
        string: String to convert.

    Returns:
        string: Path cased string.

    """
    string = snakecase(string)
    if not string:
        return string
    return re.sub(r"_", "/", string)


def backslashcase(string: str) -> str:
    """Convert string into spinal case.
    Join punctuation with backslash.

    Args:
        string: String to convert.

    Returns:
        string: Spinal cased string.

    """
    str1 = re.sub(r"_", r"\\", snakecase(string))

    return str1
    # return re.sub(r"\\n", "", str1))  # TODO: make regex fot \t ...


def sentencecase(string: str) -> str:
    """Convert string into sentence case.
    First letter capped and each punctuations are joined with space.

    Args:
        string: String to convert.

    Returns:
        string: Sentence cased string.

    """
    joiner = ' '
    string = re.sub(r"[\-_\.\s]", joiner, str(string))
    if not string:
        return string
    return capitalcase(trimcase(
        re.sub(r"[A-Z]", lambda matched: joiner + lowercase(matched.group(0)), string)))


def snakecase(string):
    if string is None or f"{string}" == "":
        return string

    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', string)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace(" ", "_")
    return word.lower()


def spinalcase(string: str) -> str:
    """Convert string into spinal case.
    Join punctuation with hyphen.

    Args:
        string: String to convert.

    Returns:
        string: Spinal cased string.

    """

    return re.sub(r"_", "-", snakecase(string))


def dotcase(string: str) -> str:
    """Convert string into dot case.
    Join punctuation with dot.

    Args:
        string: String to convert.

    Returns:
        string: Dot cased string.

    """

    return re.sub(r"_", ".", snakecase(string))


def titlecase(string: str) -> str:
    """Convert string into sentence case.
    First letter capped while each punctuations is capitalsed
    and joined with space.

    Args:
        string: String to convert.

    Returns:
        string: Title cased string.

    """

    return ' '.join(
        [capitalcase(word) for word in snakecase(string).split("_")]
    )


def trimcase(string: str) -> str:
    """Convert string into trimmed string.

    Args:
        string: String to convert.

    Returns:
        string: Trimmed case string
    """

    return str(string).strip()


def uppercase(string: str) -> str:
    """Convert string into upper case.

    Args:
        string: String to convert.

    Returns:
        string: Uppercase case string.

    """

    return str(string).upper()


def alphanumcase(string: str) -> str:
    """Cuts all non-alphanumeric symbols,
    i.e. cuts all expect except 0-9, a-z and A-Z.

    Args:
        string: String to convert.

    Returns:
        string: String with cutted non-alphanumeric symbols.

    """
    return ''.join(filter(str.isalnum, str(string)))
