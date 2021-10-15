import pandas as pd
from typing import List
import os.path
from urllib.request import urlopen
from urllib.error import URLError
import wget


def download_urllib(url: str, file_path: str = None, dir_path: str = None, verbose: bool = False):
    """Downloads file. Returns None on URLError.

    Args:
        url: A correctly formatted URL to the target file.
        file_path: Output file path. The filename is generated from the URL if not supplied.
        dir_path: Output directory path. Ignored if file_path is provided. The filename is generated from the URL.
        verbose: Prints verbose status messages.

    Returns:
        If file is downloaded successfully,
            file_path: Path to the downloaded file.
        Else,
            None.
    """
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
        return file_path

    # Open connection and write to file
    try:
        with urlopen(url) as response, open(file_path, 'wb') as file:
            file.write(response.read())
        if verbose:
            print(f"[SUCCESS] '{filename}' downloaded.")
        return file_path
    except URLError:
        if verbose:
            print(f"[ERROR] Unable to download'{filename}'.")
        return None


def download_wget(url: str, dir_path: str = None, verbose: bool = False):
    filename = url.split('/')[-1]
    if not os.path.exists(filename):
        try:
            wget.download(url.strip(), dir_path)
            if verbose:
                print(f"[SUCCESS] '{filename}' downloaded.")
        except URLError or ValueError:
            if verbose:
                print(f"[ERROR] Unable to download '{filename}'.")
    else:
        if verbose:
            print(f"[SKIP] {filename} already exists.")


def export_csv(rows: List[dict], output_path: str):
    """Writes a list of dictionaries to a CSV file."""
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
