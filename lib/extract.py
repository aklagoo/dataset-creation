from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
import uuid
from lib import config
from lib import utils
from typing import List


def _parse(content: str) -> List[dict]:
    """Extracts image lib-alt-par dictionaries.

    Args:
        content: String containing a page.
    Returns:
        images: A list of dictionary objects with keys:
            'src', 'alt', 'par'
    """
    samples = []
    soup = BeautifulSoup(content, 'html.parser')
    tags = soup.find_all('img', src=True, alt=True)
    for tag in tags:
        src = tag['src']
        alt = tag['alt']
        par = tag.parent.getText()
        samples.append({'src': src, 'alt': alt, 'par': par})
    return samples


def extract(warc_path: str, warc_segment_id: str, samples: list = None, limit: int = -1):
    """Extracts and image metadata and captions.

    Args:
        warc_path: Path to the .warc file.
        warc_segment_id: .warc file's segment ID.
        _samples: List of image data previously processed, if any.
        limit: Soft limits the number of image tags processed.
    Returns:
        images: List of image dictionaries with keys:
            'img_uuid', 'img_url', 'img_path', 'img_caption', 'warc_segment_id', 'warc_path', 'warc_url'
    """
    if not samples:
        _samples = []
    else:
        _samples = samples.copy()

    with open(warc_path, 'rb') as stream:
        for i, record in enumerate(ArchiveIterator(stream)):
            try:
                # Parse page
                warc_images = _parse(record.content_stream().read().decode("utf-8"))
                for image in warc_images:
                    # Generate UUID
                    image_uuid = uuid.uuid4()

                    # Append to warc_images
                    _samples.append({
                        'img_uuid': str(image_uuid),
                        'img_url': image['src'],
                        'img_caption': image['alt'],
                        'img_paragraph': image['par'],
                        'warc_segment_id': warc_segment_id,
                        'warc_path': warc_path,
                        'warc_url': record.rec_headers.get_header('WARC-Target-URI')
                    })
            except UnicodeDecodeError:
                pass
            if len(_samples) > limit != -1:
                break
    return _samples


def _test():
    wrc_path = "../data/segments/CC-MAIN-20210723143921-20210723173921-00258.warc.gz"
    segment_id = "1627046149929.88"
    samples = extract(wrc_path, segment_id, limit=10000)
    utils.export_csv(samples, config.CSV_FILE_SAMPLES)


if __name__ == "__main__":
    _test()
