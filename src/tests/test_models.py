import unittest

import iptables


class ChainTestCase(unittest.TestCase):
    def test_jump(self, *mocks):
        chain = iptables.Chain('foo')

        self.assertEqual('-j foo', chain.jump)
