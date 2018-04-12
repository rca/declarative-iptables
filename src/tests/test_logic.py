import unittest

import iptables


class PlanTestCase(unittest.TestCase):
    def _get_plan(self):
        plan = iptables.Plan()

        # this will delete an existing table and create it from scratch
        berto_chain = plan.create_chain('OPENVPN_BERTO')

        # rules are added with a default priority of 50
        berto_chain.add_rule('-o tun0 -s 192.168.2.2 -d 192.168.1.1 -j ACCEPT')


        # this will get an existing table and create it if it does not exist
        openvpn_chain = plan.get_chain('OPENVPN')

        # rules with higher number priority get added to the chain first
        # when updating an existing chain, rules already in the chain get a priority of 70.
        # being added is compared to existing rules and will be added if missing or left alone.
        openvpn_chain.add_rule(iptables.Rule('-o ! tun0 -j RETURN', priority=100))
        openvpn_chain.add_rule(berto_chain.jump)

        return plan

    def test_execute(self, *mocks):
        plan = self._get_plan()

        # self.assertEqual(True, plan)
