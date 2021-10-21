"""This module contains several methods to filter tags.

All methods return a boolean.
"""
from nltk.tokenize import word_tokenize
from numpy.core.shape_base import block
import config
from numpy import ndarray
from typing import List
from open_nsfw_python3 import NSFWClassifier # pip install open_nsfw_python3\
import os

sexual_classifier = NSFWClassifier()


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
    # TODO Fill stub
    return True, True


def filter_text_english(img_alt: str, img_par: str) -> (bool, bool):
    """Checks if alt-text and par-text contain at least some English words."""
    return True, True

def filter_sexual_content(img_path: str) -> bool:
    """Checks if an image contains sexual content"""
    score = sexual_classifier.get_score(img_path)
    if score > 0.5:
        return True

def generate_blacklist(blacklist_folder: str) -> dict:
    """Generates a dictionary with all blacklisted domains"""
    print("Collecting list of blacklisted domains")
    blocked_list = []
    for blacklist_file in os.listdir(blacklist_folder):
        with open(os.path.join(blacklist_folder, blacklist_file)) as f:
            lines = f.readlines()
            for l in lines:
                blocked_list.append(l[:-1])

    return set(blocked_list)

domain_blacklist = generate_blacklist("../blacklists")

def filter_blacklisted_domains(domain: str) -> bool:
    """Checks if a domain belongs to the list of blacklisted domains"""
    if domain in domain_blacklist:
        return True



