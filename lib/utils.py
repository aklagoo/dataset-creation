from socket import timeout
import pandas as pd
from typing import List
import os.path
from urllib.request import urlopen
from urllib.error import URLError
import wget
from lib import config


def download_urllib(url: str, file_path: str = None, dir_path: str = None, verbose: bool = False, skip_big: bool = False) -> (bool, str):
    """Downloads file. Returns None on URLError.

    Args:
        url: A correctly formatted URL to the target file.
        file_path: Output file path. The filename is generated from the URL if not supplied.
        dir_path: Output directory path. Ignored if file_path is provided. The filename is generated from the URL.
        verbose: Prints verbose status messages.
        skip_big: Boolean. If set, skips large files (Sizes over config.).

    Returns:
        exists: True, if file exists.
        file_path: Path to the downloaded file, if successful. Else, None.
    """
    exists = False
    # Generate file name if path hasn't been provided
    filename = url.split('/')[-1]
    if not file_path:
        if dir_path:
            file_path = os.path.join(dir_path, filename)
        else:
            file_path = filename

    # Check if file already exists
    if os.path.exists(file_path):
        if verbose:
            print(f"[SKIP] '{filename}' already exists.")
            exists = True
        return exists, file_path

    # Open connection and write to file
    try:
        with urlopen(url, timeout=config.UTILS_DL_TIMEOUT) as response, open(file_path, 'wb') as file:
            # Check for file size
            if int(response.info()["Content-Length"]) >= config.UTILS_DL_FILE_MAX:
                if verbose:
                    print(f"[ERROR] File '{filename}' too large. Skipped.")
                return exists, None
            file.write(response.read())
        if verbose:
            print(f"[SUCCESS] '{filename}' downloaded.")
        return exists, file_path
    # except URLError:
    except:
        if verbose:
            print(f"[ERROR] Unable to download '{filename}'.")
        return exists, None
    #except timeout:
    #    if verbose:
    #        print(f"[ERROR] Timeout while downloading '{filename}'.")
    #    return exists, None
    #except KeyError:
    #    if verbose:
    #        print(f"[ERROR] Skipping '{filename}'. Could not find header \"Content-Length\".")
    #    return exists, None


def download_wget(url: str, dir_path: str = None, verbose: bool = False) -> (bool, str):
    """Downloads a file via wget.

    Args:
        url: URL to the file.
        dir_path: Path to output directory.
        verbose: If set, prints a status output.

    Returns:
        exists: True, if file already exists.
        filename: Path to the downloaded file.
    """
    filename = url.split('/')[-1]
    exists = False
    if not os.path.exists(filename):
        try:
            filename = wget.download(url.strip(), dir_path)
            if verbose:
                print(f"[SUCCESS] '{filename}' downloaded.")
        except URLError or ValueError:
            if verbose:
                print(f"[ERROR] Unable to download '{filename}'.")
    else:
        if verbose:
            print(f"[SKIP] {filename} already exists.")
            exists = True

    return exists, filename


def export_csv(rows: List[dict], output_path: str):
    """Writes a list of dictionaries to a CSV file."""
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
