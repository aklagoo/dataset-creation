from typing import List, Dict
import cv2
import torch
import torchvision
from torchvision import transforms as transforms
from lib.detect import _predict


def filter_text(tags: List[dict]) -> List[dict]:
    """Checks if par and alt are valid. Discards otherwise."""
    # TODO Fill stub
    return tags


def detect(tags: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Loads and tags images."""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    model.eval().to(device)

    transform = transforms.Compose([
        transforms.ToTensor(),
    ])

    _tags = []
    for sample in tags:
        # Predict classes and bounding boxes for image
        classes, labels, boxes = _predict(cv2.imread(sample['img_path']), model, device, 0.8, transform)
        _tags.append({
            'img_uuid': sample['img_uuid'],
            'img_url': sample['img_url'],
            'img_path': sample['img_path'],
            'img_caption': sample['img_caption'],
            'img_par': sample['img_par'],
            'warc_path': sample['warc_path'],
            'warc_url': sample['warc_url'],
            'classes': ' '.join(list(set(classes))),
        })

    return _tags


def download(tags: List[dict]) -> List[dict]:
    """Downloads images for all tags. Discards tags with invalid URLs."""
    # TODO Fill stub
    return tags


def filter_img(tags: List[dict]) -> List[dict]:
    """Checks if text matches classes. Discards tags otherwise."""
    # TODO Fill stub
    return tags


pipeline = [filter_text, download, detect, filter_img]
