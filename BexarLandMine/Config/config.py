from tomllib import load
from os.path import exists, isfile


class Config():
    def __init__(self, file_path: str):
        self._file_path = file_path
        if not exists(self._file_path):
            raise FileNotFoundError(("Config file not found: "
                                     f"{self._file_path}"))
        if not isfile(self._file_path):
            raise IsADirectoryError(("Config file is not a regular file "
                                     f"or link: {self._file_path}"))
        with open(self._file_path, "rb") as f:
            data = load(f)
        self.data = data

    def __repr__(self):
        return f"Config({self._file_path})"
