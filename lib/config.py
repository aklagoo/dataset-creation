"""This module contains system-wide configuration constants."""
import os

BASE_DIR = os.getcwd()

SEGMENT_DIR = "data/segments"
SEGMENT_IDS = [
    "1627046149929.88",
    "1627046151531.67",
    "1627046152085.13",
    "1627046153392.43"
]
SEGMENT_URL_WARC = "https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2021-31/warc.paths.gz"
SEGMENT_URL_DOMAIN = "https://commoncrawl.s3.amazonaws.com/"
SEGMENT_FILE_WARC = os.path.join(BASE_DIR, "data/segments/warc.paths")

CSV_FILE_SAMPLES = os.path.join(BASE_DIR, "data/csv/samples.csv")
CSV_FILE_CLASSES = os.path.join(BASE_DIR, "data/csv/classes.csv")

IMG_DIR_BASE = os.path.join(BASE_DIR, "data/img/base")
IMG_DIR_TAGGED = os.path.join(BASE_DIR, "data/img/tagged")
IMG_ALLOWED_EXT = ['.png', '.jpg', '.jpeg']

DETECT_COCO_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'street sign', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'hat', 'backpack', 'umbrella', 'shoe', 'eye glasses',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'plate', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'mirror', 'dining table',
    'window', 'desk', 'toilet', 'door', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'blender', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush', 'hair brush'
]

FILTER_TEXT_LEN = 10
FILTER_IMG_SIZE = (50, 50)
FILTER_MIN_SIMILARITY = 0.7
FILTER_TEXT_EN_LEN = 8
FILTER_URL_BLACKLIST_DIR = os.path.join(BASE_DIR, 'data/blacklists')
FILTER_MIN_NSFW = 0.5
