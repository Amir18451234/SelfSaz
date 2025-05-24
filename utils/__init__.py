from config import PERSIAN_NUMERALS, ENGLISH_NUMERALS

def convert_persian_numbers(text):
    return text.translate(str.maketrans(PERSIAN_NUMERALS, ENGLISH_NUMERALS))

__all__ = ['convert_persian_numbers']