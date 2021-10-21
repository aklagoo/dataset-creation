from typing import List, Tuple
import tempfile
import gzip
import os
from lib import config, utils
from lib.utils import download_wget
import glob
from numpy.random import choice


def get_urls() -> List[Tuple[str, str]]:
    """Generates a list of URLs filtered by segments."""
    filtered_urls = []

    # Check if warc.paths already exists. If not, download the file.
    if not os.path.exists(config.SEGMENT_FILE_WARC):
        with tempfile.TemporaryDirectory() as tempdir:

            # Download to a temporary directory and extract.
            path_gz = os.path.join(tempdir, 'warc.paths.gz')
            path_gz = utils.download_urllib(config.SEGMENT_URL_WARC, path_gz)

            # Filter URLs by segment IDs and write to file
            with gzip.open(path_gz, 'r') as file_gz, open(config.SEGMENT_FILE_WARC, 'w') as file_warc:
                for line in file_gz:
                    line = line.decode(encoding='utf-8').strip()

                    # Check if any segmentID is in the URL
                    for segment_id in config.SEGMENT_IDS:
                        if segment_id in line:
                            url = config.SEGMENT_URL_DOMAIN + line.strip()
                            filtered_urls.append((segment_id, url))
                            file_warc.write(segment_id + ',' + url + '\n')

    # If warc.paths already exists, open and load.
    else:
        with open(config.SEGMENT_FILE_WARC, 'r') as file_warc:
            for line in file_warc:
                filtered_urls.append(tuple(line.strip().split(',')))

    return filtered_urls


def download_batch(first_n=-1):
    """Downloads a filtered set of WARC files.

    Args:
        first_n: A limit on the number of files downloaded.
    """
    filtered_urls = get_urls()

    # Download segments.
    if first_n != -1:
        filtered_urls = filtered_urls[:first_n]
    for _, url in filtered_urls:
        download_wget(url, config.SEGMENT_DIR)


def download_rand_new() -> (str, str):
    """Downloads a single new WARC file.

    This function randomly picks a WARC file until the file does not exist
    locally. The missing file is downloaded.

    Returns:
        segment_id: Segment ID of the file.
        file: Path to downloaded file.
    """
    filtered_urls = get_urls()
    files_exist = [x.split('/')[-1] for x in glob.glob(config.SEGMENT_DIR)]

    while True:
        url = choice(filtered_urls)
        segment_id = url[0]
        file_name = url[1].split('/')[-1]
        if file_name not in files_exist:
            _, file = utils.download_wget(url, config.SEGMENT_DIR)
            return segment_id, file


if __name__ == '__main__':
    download_batch(0)
