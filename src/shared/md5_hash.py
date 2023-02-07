__author__ = "Sylivie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

import hashlib
from werkzeug.datastructures import FileStorage


class MD5Hash:
    @staticmethod
    def compute_hash(file: FileStorage = None):
        """
        Computes MD5 hash of a given file.
        """
        md5_hash: hashlib.md5 = hashlib.md5()
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
        hashString: str = md5_hash.hexdigest()
        file.stream.seek(0)
        return hashString
