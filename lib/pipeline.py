from typing import List, Dict
import cv2
import torch
import torchvision
from torchvision import transforms
from lib.detect import _predict
from lib import filters
from lib.utils import download_urllib
import os
from lib import config
import json
from urllib.parse import urlparse, urljoin
from tqdm import tqdm


_device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
_model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
_model.eval().to(_device)
_transform = transforms.Compose([
    transforms.ToTensor(),
])


def filter_text(samples: List[dict]) -> List[dict]:
    """Checks if par and alt are valid. Discards otherwise."""
    _samples = []
    for sample in tqdm(samples):
        _sample = sample.copy()

        alt = _sample['img_alt']
        par = _sample['img_par']

        # Length check
        alt_len, par_len = filters.filter_text_len(alt, par)
        if not alt_len and not par_len:
            continue
        else:
            _sample['FLAG_ALT_LEN'] = alt_len
            _sample['FLAG_PAR_LEN'] = par_len

        # Language check
        alt_en, par_en = filters.filter_text_english(alt, par)
        if not alt_en and not par_en:
            continue
        else:
            _sample['FLAG_ALT_EN'] = alt_en
            _sample['FLAG_PAR_EN'] = par_en

        # Append sample to _samples
        _samples.append(_sample)

    return _samples


def download(samples: List[dict]) -> List[dict]:
    """Downloads images for all tags. Discards tags with invalid URLs."""
    _samples = []
    for sample in tqdm(samples):
        _sample = sample.copy()

        # Generate file path
        url = _sample['img_url']
        ext = '.' + url.split('.')[-1]
        if ext.lower() not in config.IMG_ALLOWED_EXT:
            continue
        path = os.path.join(config.IMG_DIR_BASE, _sample['img_uuid'] + ext)

        # Check if image has been downloaded
        try:
            exists, path = download_urllib(url, path)
            if path:
                _sample['img_path'] = path
                _samples.append(_sample)

        except ValueError:
            domain = urlparse(url).netloc
            url = urljoin(domain, url)
            try:
                exists, path = download_urllib(url, path)
                if path:
                    _sample['img_path'] = path
                    _samples.append(_sample)
            except ValueError:
                pass

    return _samples


def detect_and_filter_img(samples: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Detects and filters images."""
    _samples = []
    for sample in tqdm(samples):
        _sample = sample.copy()

        # Load and check image size
        img = cv2.imread(_sample['img_path'])
        if not filters.filter_img_shape(img):
            continue

        # Check NSFW content
        if not filters.filter_sexual_content(_sample['img_path']):
            continue

        # Predict classes and boxes
        classes, labels, boxes = _predict(img, _model, _device, 0.8, _transform)
        if len(labels) == 0:
            continue

        # Check if the alt-text and par-text match the classes
        alt = _sample['img_alt']
        par = _sample['img_par']
        alt_match, par_match = filters.filter_match_classes(labels, alt, par)
        if not alt_match and not par_match:
            continue

        # Append sample
        _sample['FLAG_ALT_MATCH'] = alt_match
        _sample['FLAG_PAR_MATCH'] = par_match
        _sample['classes'] = json.dumps(labels)
        _sample['boxes'] = json.dumps(boxes.tolist())
        _samples.append(_sample)

    return _samples


pipeline = [filter_text, download, detect_and_filter_img]
