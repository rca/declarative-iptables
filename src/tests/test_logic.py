import unittest
from unittest import mock

import iptables

from tests.utils import get_tables


class PlanTestCase(unittest.TestCase):
    def _get_plan(self):
        plan = iptables.Plan()

        # this will delete an existing table and create it from scratch
        berto_chain = plan.create_chain('mangle', 'OPENVPN_BERTO')

        # rules are added with a default priority of 50
        berto_chain.add_rule('-o tun0 -s 192.168.2.2 -d 192.168.1.1 -j ACCEPT')

        # this will get an existing table and create it if it does not exist
        openvpn_chain = plan.get_chain('mangle', 'OPENVPN')

        # rules with higher number priority get added to the chain first
        # when updating an existing chain, rules already in the chain get a priority of 70.
        # being added is compared to existing rules and will be added if missing or left alone.
        openvpn_chain.add_rule(iptables.Rule('-o ! tun0 -j RETURN', priority=100))
        openvpn_chain.add_rule(berto_chain.jump)
        openvpn_chain.add_rule(iptables.Rule('-j DROP', priority=10))

        return plan

    @mock.patch('iptables.logic.run_command')
    @mock.patch('iptables.logic.subprocess')
    def test_execute(self, *mocks):
        tables = get_tables('iptables-save_with-mangle.txt')

        run_command_mock = mocks[1]
        run_command_mock.return_value = None, None, None

        plan = self._get_plan()
        plan.get_current_tables = mock.Mock()
        plan.get_current_tables.return_value = tables

        plan.execute()

        self.assertEqual(5, len(run_command_mock.mock_calls))
