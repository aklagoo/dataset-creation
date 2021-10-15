import tempfile
import gzip
import os
from lib import config, utils
from lib.utils import download_wget


def get_urls():
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
                    if any(segment_id in line for segment_id in config.SEGMENT_IDS):
                        url = config.SEGMENT_URL_DOMAIN + line
                        filtered_urls.append(url.strip())
                        file_warc.write(url + '\n')

    # If warc.paths already exists, open and load.
    else:
        with open(config.SEGMENT_FILE_WARC, 'r') as file_warc:
            for line in file_warc:
                filtered_urls.append(line.strip())

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
    for url in filtered_urls:
        download_wget(url, config.SEGMENT_DIR)


if __name__ == '__main__':
    download_batch(0)
