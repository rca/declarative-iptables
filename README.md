# simple tables
A simple interface to managing iptables on linux

The hardest part of managing iptables is that they are a central piece of data that's constantly changing from many different directions.  Because its state isn't guaranteed, making a simple modification to it can have undesired consequences.  This project aims to solve this problem by making yet another interface to iptables.

This interface aims to be declarative.  Rather than looking at issuing changes directly to iptables, this package defines the desired state.  The significance is that it matters less what the tables look like at any given time and instead the goal is to end up with what it should look like.

Additionally, because it's unknown what changes other systems have made, any tables and rules that have not been declared are left untouched.


## Example

```
import iptables

plan = iptables.Plan()

# this will delete an existing table and create it from scratch
berto_chain = plan.add_chain('OPENVPN_BERTO')

# rules are added with a default priority of 50
berto_chain.add_rule(iptables.Rule('-o tun0 -s 192.168.2.2 -d 192.168.1.1 -j ACCEPT'))

# this will get an existing table and create it if it does not exist
openvpn_chain = plan.get_chain('OPENVPN')

# rules with higher number priority get added to the chain first
# when updating an existing chain, rules already in the chain get a priority of 70.
# being added is compared to existing rules and will be added if missing or left alone.
openvpn_chain.add_rule(iptables.Rule('-o ! tun0 -j RETURN', priority=100))
openvpn_chain.add_rule(berto_chain.jump)

# make necessary changes to achieve the desired outcome
plan_execute()
```
