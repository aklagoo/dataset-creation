"""This module contains several methods to filter tags.

All methods return a boolean.
"""
from nltk.tokenize import word_tokenize
from lib import config
from numpy import ndarray
from typing import List


def filter_text_len(img_alt: str, img_par: str):
    """Checks if length of alt-text and par-text is greater than the minimum length."""
    alt_len = len(word_tokenize(img_alt))
    par_len = len(word_tokenize(img_par))
    return  alt_len > config.FILTER_TEXT_LEN,  par_len > config.FILTER_TEXT_LEN


def filter_img_shape(img: ndarray):
    """Checks if shape of image is large enough."""
    h, w, _ = img.shape
    return (h, w) >= config.FILTER_IMG_SIZE


def filter_match_classes(classes: List[str], text: str):
    """Checks if classes match the text."""
    # TODO Fill stub
    return True


def filter_text_english(text: str):
    """Checks if text contains at least some English words."""
    # TODO Fill stub
    return True
