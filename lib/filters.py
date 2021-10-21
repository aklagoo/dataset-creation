"""This module contains several methods to filter tags.

All methods return a boolean.
"""
from nltk.tokenize import word_tokenize
from lib import config
from numpy import ndarray
from typing import List


def _filter_text_len(img_alt: str, img_par: str) -> (bool, bool):
    """Checks if length of alt-text and par-text is greater than the minimum length."""
    alt_len = len(word_tokenize(img_alt))
    par_len = len(word_tokenize(img_par))
    return alt_len > config.FILTER_TEXT_LEN,  par_len > config.FILTER_TEXT_LEN


def _filter_img_shape(img: ndarray) -> bool:
    """Checks if shape of image is large enough."""
    h, w, _ = img.shape
    return (h, w) >= config.FILTER_IMG_SIZE


def _filter_match_classes(classes: List[str], text: str) -> bool:
    """Checks if classes match the text."""
    # TODO Fill stub
    return True


def _filter_text_english(img_alt: str, img_par: str) -> (bool, bool):
    """Checks if alt-text and par-text contain at least some English words."""
    # TODO Fill stub
    return True, True


def filter_text(tags: List[dict]) -> List[dict]:
    """Checks if par and alt are valid. Discards otherwise."""
    # TODO Fill stub
    return tags


def filter_download(tags: List[dict]) -> List[dict]:
    """Downloads images for all tags. Discards tags with invalid URLs."""
    # TODO Fill stub
    return tags


def filter_img(tags: List[dict]) -> List[dict]:
    """Checks if text matches classes. Discards tags otherwise."""
    # TODO Fill stub
    return tags


filters = [filter_text, filter_download, filter_img]
