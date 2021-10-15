import torchvision.transforms as transforms
import torchvision
import cv2
import numpy as np
import torch
import csv
from lib import config
from utils import export_csv
from typing import List, Dict


def _predict(image: np.ndarray, model: torch.nn.Module, device: torch.device, detection_threshold: float,
             transform: torchvision.transforms.Compose):
    """Detects objects in a single image.

    Args:
        image: An image passed as (H, W, C).
        model: A PyTorch detection model.
        device: The inference device picked.
        detection_threshold: Minimum confidence threshold for classifying objects. Must be between 0 and 1.
        transform: A set of image and vector transforms.

    Returns:
        boxes: Detected bounding boxes.
        pred_classes: List of detected objects as strings.

    """
    # Convert image to data format
    image = transform(image).to(device)
    image = image.unsqueeze(0)
    outputs = model(image)

    # Extract labels
    classes = outputs[0]['labels'].cpu().numpy()
    labels = [config.DETECT_COCO_NAMES[label] for label in classes]

    # Extract bounding boxes
    boundaries = outputs[0]['boxes'].detach().cpu().numpy()
    scores = outputs[0]['scores'].detach().cpu().numpy()
    boxes = boundaries[scores >= detection_threshold].astype(np.int32)

    return classes, labels, boxes


def draw_boxes(boxes, classes, labels, image):
    colors = np.random.uniform(70, 100, size=(len(config.DETECT_COCO_NAMES), 3))
    for i, box in enumerate(boxes):
        color = colors[labels[i]]
        cv2.rectangle(
            image,
            (int(box[0]), int(box[1])),
            (int(box[2]), int(box[3])),
            color, 2
        )
        cv2.putText(image, classes[i], (int(box[0]), int(box[1]-5)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, 
                    lineType=cv2.LINE_AA)
    return image


def detect() -> List[Dict[str, str]]:
    """Loads and tags images.

    Returns:
        tagged_samples: List of samples containing source metadata and tagged classes.
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    model.eval().to(device)

    transform = transforms.Compose([
        transforms.ToTensor(),
    ])

    tagged_samples = []
    with open(config.CSV_FILE_SAMPLES, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            # Predict classes and bounding boxes for image
            classes, labels, boxes = _predict(cv2.imread(row['img_path']), model, device, 0.8, transform)
            tagged_samples.append({
                'img_uuid': row['img_uuid'],
                'img_url': row['img_url'],
                'img_path': row['img_path'],
                'img_caption': row['img_caption'],
                'img_par': row['img_par'],
                'warc_path': row['warc_path'],
                'warc_url': row['warc_url'],
                'classes': ' '.join(list(set(classes))),
            })

    return tagged_samples


if __name__ == '__main__':
    tagged = detect()
    export_csv(tagged, config.CSV_FILE_CLASSES)
