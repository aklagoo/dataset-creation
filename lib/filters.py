"""This module contains several methods to filter tags.

All methods return a boolean.
"""
from nltk.tokenize import word_tokenize
from nltk.corpus import words
from nltk.corpus import wordnet as wn
from lib import config
from numpy import ndarray
from typing import List
from itertools import product


dictionary = set(words.words())


def filter_text_len(img_alt: str, img_par: str) -> (bool, bool):
    """Checks if length of alt-text and par-text is greater than the minimum length."""
    alt_len = len(word_tokenize(img_alt))
    par_len = len(word_tokenize(img_par))
    return alt_len > config.FILTER_TEXT_LEN,  par_len > config.FILTER_TEXT_LEN


def filter_img_shape(img: ndarray) -> bool:
    """Checks if shape of image is large enough."""
    h, w, _ = img.shape
    return (h, w) >= config.FILTER_IMG_SIZE


def filter_match_classes(classes: List[str], img_alt: str, img_par: str) -> (bool, bool):
    """Checks if classes match the text."""
    # Get unique words
    classes = set(classes)
    alt = set(word_tokenize(img_alt))
    par = set(word_tokenize(img_par))

    # Get class-word cross product
    class_alt = product(classes, alt)
    class_par = product(classes, par)

    # Check if any pair of words is similar for alt-text
    alt_match = False
    for x, y in class_alt:
        x_syn = wn.synset(x)
        y_syn = wn.synset(y)
        if x_syn.path_similarity(y_syn) >= config.FILTER_MIN_SIMILARITY:
            alt_match = True
            break

    # Check if any pair of words is similar for alt-text
    par_match = False
    for x, y in class_par:
        x_syn = wn.synset(x)
        y_syn = wn.synset(y)
        if x_syn.path_similarity(y_syn) >= config.FILTER_MIN_SIMILARITY:
            par_match = True
            break

    return alt_match, par_match


def filter_text_english(img_alt: str, img_par: str) -> (bool, bool):
    """Checks if alt-text and par-text contain at least some English words.

    This method tokenizes both sentences and checks if there are at least some
    English words.
    """
    # Count English words
    alt_words = word_tokenize(img_alt)
    alt_count = sum([x in dictionary for x in alt_words])
    par_words = word_tokenize(img_par)
    par_count = sum([x in dictionary for x in par_words])

    return alt_count >= config.FILTER_TEXT_EN_LEN, par_count >= config.FILTER_TEXT_EN_LEN
