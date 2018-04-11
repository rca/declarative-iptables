import unittest

from iptables.tables import IPTables

from tests.utils import get_tables


class IPTablesTestCase(unittest.TestCase):
    @property
    def tables(self):
        return get_tables('iptables-save_with-mangle.txt')

    def test_find_chain(self, *mocks):
        tables = self.tables

        chain = tables.find_chain('mangle', 'OPENVPN_BERTO')

        self.assertEqual({'rules': [['-o', 'tun0', '-j', 'DROP']]}, chain)

    def test_find_missing_chain(self, *mocks):
        tables = self.tables

        chain = tables.find_chain('mangle', 'OPENVPN_NOTHING')

        self.assertEqual(None, chain)

    def test_find_rule(self, *mocks):
        tables = self.tables

        rule = ['-o', 'tun0', '-j', 'DROP']

        idx = tables.find_rule('mangle', 'OPENVPN_BERTO', rule)

        self.assertEqual(0, idx)

    def test_find_missing_rule(self, *mocks):
        tables = self.tables

        rule = ['-o', 'tun0', '-d', '192.168.1.1/32', '-j', 'ACCEPT']

        idx = tables.find_rule('mangle', 'OPENVPN_BERTO', rule)

        self.assertEqual(None, idx)
