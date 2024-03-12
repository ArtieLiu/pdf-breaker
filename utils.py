from pathlib import Path


def filename_of(filepath):
    return Path(filepath).stem

