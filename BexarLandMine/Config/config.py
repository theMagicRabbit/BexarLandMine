from tomllib import load
from os.path import exists, isfile

class Config():
    def __init__(self, file_path: str):
        self._file_path = file_path
        if not exists(self._file_path):
            raise FileNotFoundError(f"Config file not found: {self._file_path}")
        if not isfile(self._file_path):
            raise IsADirectoryError(f"Config file is not a regular file or link: {self._file_path}")
        with open(self._file_path, "rb") as f:
            data = load(f)
        self.data = data

    def __repr__(self):
        return f"Config({self._file_path})"
