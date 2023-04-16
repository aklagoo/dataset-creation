from urllib.parse import urlparse
from tqdm import tqdm
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
import uuid
from lib import config
from lib import utils
from lib.filters import filter_blacklisted_domains
from typing import List


class SampleFormatException(Exception):
    def __init__(self, text, samples):
        super().__init__(text)

        self._samples = samples
        self._errors = {
            'src': {'missing': [], 'incorrect_type': []},
            'alt': {'missing': [], 'incorrect_type': []},
            'par': {'missing': [], 'incorrect_type': []},
        }

        for i, sample in samples:
            if 'src' not in sample:
                self._errors['src']['missing'].append(i)
            elif not isinstance(sample['src'], str):
                self._errors['src']['incorrect_type'].append(i)

            if 'alt' not in sample:
                self._errors['alt']['missing'].append(i)
            elif not isinstance(sample['alt'], str):
                self._errors['alt']['incorrect_type'].append(i)

            if 'par' not in sample:
                self._errors['par']['missing'].append(i)
            elif not isinstance(sample['par'], str):
                self._errors['par']['incorrect_type'].append(i)

        self._stats = {
            'src_missing': len(self._errors['src']['missing']),
            'src_incorrect_type': len(self._errors['src']['incorrect_type']),
            'src_err': len(self._errors['src']['missing']) + len(self._errors['src']['incorrect_type']),
            'alt_missing': len(self._errors['alt']['missing']),
            'alt_incorrect_type': len(self._errors['alt']['incorrect_type']),
            'alt_err': len(self._errors['alt']['missing']) + len(self._errors['alt']['incorrect_type']),
            'par_missing': len(self._errors['par']['missing']),
            'par_incorrect_type': len(self._errors['par']['incorrect_type']),
            'par_err': len(self._errors['par']['missing']) + len(self._errors['par']['incorrect_type']),
        }
        self._stats['total_err'] = self._stats['src_err'] + self._stats['alt_err'] + self._stats['par_err']
        self._stats['ratio_err'] = self._stats['total_err'] / len(self._samples) / 3

    @property
    def errors(self):
        return self._errors

    @property
    def samples(self):
        return self._samples

    @property
    def stats(self):
        return self._stats

    def __repr__(self):
        if self.args[0]:
            return f"SampleFormatError ('{self.args[0]}', {self._stats['total_err']} errors)"
        return f"SampleFormatError ('{self._stats['total_err']} errors)"

    def __str__(self):
        if self.args[0]:
            return f"""{self.args[0]}
            Total Errors: {self._stats['total_err']} [{self._stats['ratio_err']}]
                src: {self._stats['src_err']}
                    Missing values: {self._stats['src_missing']}
                    Incorrect types: {self._stats['src_incorrect_type']}
                alt: {self._stats['alt_err']}
                    Missing values: {self._stats['alt_missing']}
                    Incorrect types: {self._stats['alt_incorrect_type']}
                par: {self._stats['par_err']}
                    Missing values: {self._stats['par_missing']}
                    Incorrect types: {self._stats['par_incorrect_type']}
            """

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

    # Check if sample format is correct
    for sample in _samples:
        if 'src' not in sample or 'alt' not in sample or 'par' not in sample:
            raise SampleFormatException("Missing value", samples)
        if not isinstance(sample['src'], str) or not isinstance(sample['alt'], str) or \
                not isinstance(sample['par'], str):
            raise SampleFormatException("Wrong type", samples)

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
