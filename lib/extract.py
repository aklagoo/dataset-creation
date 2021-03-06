from urllib.parse import urlparse
from tqdm import tqdm
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
import uuid
from lib import config
from lib import utils
from lib.filters import filter_blacklisted_domains
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
        try:
            par = tag.parent.getText()
            samples.append({'src': src, 'alt': alt, 'par': par})
        except:
            pass
    return samples


def extract(warc_path: str, warc_segment_id: str, samples: list = None, limit: int = -1):
    """Extracts and image metadata and captions.

    Args:
        warc_path: Path to the .warc file.
        warc_segment_id: .warc file's segment ID.
        samples: List of image data previously processed, if any.
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
        for i, record in enumerate(tqdm(ArchiveIterator(stream))):
            try:
                # Get URL
                url = record.rec_headers.get_header('WARC-Target-URI')
                domain = urlparse(url).netloc
                if not filter_blacklisted_domains(domain):
                    continue

                # Parse page
                warc_images = _parse(record.content_stream().read().decode("utf-8"))
                for image in warc_images:
                    # Generate UUID
                    image_uuid = uuid.uuid4()

                    # Append to warc_images
                    _samples.append({
                        'img_uuid': str(image_uuid),
                        'img_url': image['src'],
                        'img_alt': image['alt'],
                        'img_par': image['par'],
                        'warc_segment_id': warc_segment_id,
                        'warc_path': warc_path,
                        'warc_url': url
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
    utils.export_csv(samples, config.CSV_DIR_SAMPLES)


if __name__ == "__main__":
    _test()
