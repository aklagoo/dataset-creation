import tempfile
import unittest
from lib.utils import download_urllib
import os


def _remove(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


class UtilsDownloadFile(unittest.TestCase):
    URL_VALID = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_light_color_272x92dp.png'
    URL_INVALID = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_light_color_272x92dp.pn'
    FILENAME_DEFAULT = 'googlelogo_light_color_272x92dp.png'
    FILENAME_CUSTOM = 'temp.svg'
    TEXT_CUSTOM = b'Hello world!'

    def test_404(self):
        res = download_urllib(self.URL_INVALID)
        self.assertIsNone(res, "should return None when 404.")

    def test_200(self):
        res = download_urllib(self.URL_VALID)
        self.assertIsInstance(res, str, "should return type 'str' when 200.")
        _remove(res)

    def test_file_create(self):
        res = download_urllib(self.URL_VALID)
        self.assertTrue(os.path.exists(res), "should create a file.")
        _remove(res)

    def test_file_path_default(self):
        res = download_urllib(self.URL_VALID)
        self.assertEqual(res, self.FILENAME_DEFAULT, "should extract the correct filename from the URL.")
        _remove(res)

    def test_file_path_specified(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = os.path.join(tempdir, self.FILENAME_CUSTOM)
            res = download_urllib(self.URL_VALID, path)
            self.assertTrue(os.path.exists(res), "should create a file at the specified path.")

    def test_dir_path(self):
        with tempfile.TemporaryDirectory() as tempdir:
            _ = download_urllib(self.URL_VALID, dir_path=tempdir)
            target_path = os.path.join(tempdir, self.FILENAME_DEFAULT)
            self.assertTrue(os.path.exists(target_path), "should create a file file in the specified directory.")

    def test_duplicate(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = os.path.join(tempdir, self.FILENAME_CUSTOM)
            with open(path, 'wb') as file:
                file.write(self.TEXT_CUSTOM)
            _ = download_urllib(self.URL_VALID, path)
            with open(path, 'rb') as file:
                self.assertEqual(file.read(), self.TEXT_CUSTOM, "should not download if file already exists.")
