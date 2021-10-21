from typing import List, Dict
import cv2
import torch
import torchvision
from torchvision import transforms as transforms
from lib.detect import _predict
from lib.filters import filter_text_len, filter_text_english


def filter_text(samples: List[dict]) -> List[dict]:
    """Checks if par and alt are valid. Discards otherwise."""
    _samples = []
    for sample in samples:
        _sample = sample.copy()

        alt = _sample['img_alt']
        par = _sample['img_par']

        # Length check
        alt_len, par_len = filter_text_len(alt, par)
        if not alt_len and not par_len:
            continue
        else:
            _sample['FLAG_ALT_LEN'] = alt_len
            _sample['FLAG_PAR_LEN'] = par_len

        # Language check
        alt_en, par_en = filter_text_english(alt, par)
        if not alt_en and not par_en:
            continue
        else:
            _sample['FLAG_ALT_EN'] = alt_en
            _sample['FLAG_PAR_EN'] = par_en

        # Append sample to _samples
        _samples.append(_sample)

    return _samples


def detect(samples: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Loads and tags images."""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    model.eval().to(device)

    transform = transforms.Compose([
        transforms.ToTensor(),
    ])

    _samples = []
    for sample in samples:
        _sample = sample.copy()

        # Predict classes and bounding boxes for image
        classes, labels, boxes = _predict(cv2.imread(_sample['img_path']), model, device, 0.8, transform)
        _sample['classes'] = ' '.join(list(set(classes)))
        _samples.append(_sample)

    return _samples


def download(tags: List[dict]) -> List[dict]:
    """Downloads images for all tags. Discards tags with invalid URLs."""
    # TODO Fill stub
    return tags


def filter_img(tags: List[dict]) -> List[dict]:
    """Checks if text matches classes. Discards tags otherwise."""
    # TODO Fill stub
    return tags


pipeline = [filter_text, download, detect, filter_img]
