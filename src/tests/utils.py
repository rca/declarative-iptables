import os

from iptables.parser import IPTablesParser

SCRIPT_DIR = os.path.dirname(__file__)


def get_content(path):
    full_path = os.path.join(SCRIPT_DIR, 'files', path)

    with open(full_path) as fh:
        return fh.read()


def get_tables(path):
    return IPTablesParser.parse(get_content(path))
