import os

SCRIPT_DIR = os.path.dirname(__file__)


def get_content(path):
    full_path = os.path.join(SCRIPT_DIR, 'files', path)

    with open(full_path) as fh:
        return fh.read()
