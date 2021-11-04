"""This module contains several methods to filter tags.

All filters return one or more booleans.
"""
from nltk.tokenize import word_tokenize
from nltk.corpus import words
from nltk.corpus import wordnet as wn
from lib import config
from numpy import ndarray
from typing import List
from itertools import product
from nudenet import NudeClassifier
import os


def _generate_blacklist(blacklist_folder: str) -> set:
    """Generates a dictionary with all blacklisted domains"""
    print("Collecting list of blacklisted domains")
    blocked_list = []
    for blacklist_file in os.listdir(blacklist_folder):
        with open(os.path.join(blacklist_folder, blacklist_file)) as f:
            lines = f.readlines()
            for l in lines:
                blocked_list.append(l[:-1])

    return set(blocked_list)


sexual_classifier = NudeClassifier()
dictionary = set(words.words())
domain_blacklist = _generate_blacklist(config.FILTER_URL_BLACKLIST_DIR)


def filter_text_len(img_alt: str, img_par: str) -> (bool, bool):
    """Checks if length of alt-text and par-text is greater than the minimum length."""
    if config.TEXT_DROP_BIG:
        if len(img_alt) > config.TEXT_DROP_BIG_LEN or len(img_par) > config.TEXT_DROP_BIG_LEN:
            return False, False

    alt_len = len(word_tokenize(img_alt))
    par_len = len(word_tokenize(img_par))
    return alt_len > config.FILTER_TEXT_MIN_LEN, par_len > config.FILTER_TEXT_MIN_LEN


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
    for c, a in class_alt:
        x_syns = wn.synsets(c)
        y_syns = wn.synsets(a)

        # Get synset-synset product
        for x_syn, y_syn in product(x_syns, y_syns):
            if x_syn.path_similarity(y_syn) >= config.FILTER_MIN_SIMILARITY:
                alt_match = True
                break

    # Check if any pair of words is similar for par-text
    par_match = False
    for c, a in class_par:
        x_syns = wn.synsets(c)
        y_syns = wn.synsets(a)

        # Get synset-synset product
        for x_syn, y_syn in product(x_syns, y_syns):
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


def filter_sexual_content(img_path: str) -> bool:
    """Checks if an image does not contain sexual content."""
    score = sexual_classifier.classify(img_path)[img_path]['unsafe']
    if score >= config.FILTER_MIN_NSFW:
        return False
    return True


def filter_blacklisted_domains(domain: str) -> bool:
    """Checks if a domain does not belong to the list of blacklisted domains."""
    if domain not in domain_blacklist:
        return True
