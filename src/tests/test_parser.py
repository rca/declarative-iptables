import json
import unittest

from unittest import mock

from iptables.parser import IPTablesParser

from tests.utils import get_content


class IPTablesParserTestCase(unittest.TestCase):
    def test_parse(self, *mocks):
        content = get_content('iptables-save_with-mangle.txt')

        tables = IPTablesParser.parse(content)

        self.assertEqual(len(tables), 3)
        self.assertEqual(sorted(tables.keys()), ['filter', 'mangle', 'nat'])

        self.assertEqual(
            sorted(tables['mangle'].keys()),
            [
                'FORWARD',
                'INPUT',
                'OPENVPN_BERTO',
                'OUTPUT',
                'POSTROUTING',
                'PREROUTING',
            ],
        )
