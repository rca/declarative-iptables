from .models import Rule
from .tables import IPTables


class IPTablesParser(object):
    def __init__(self):
        self.tables = IPTables()
        self._current_table = None
        self._current_table_name = None

    def commit(self):
        self._current_table = None
        self._current_table_name = None

    @classmethod
    def parse(cls, iptables_save_content: str) -> IPTables:
        parser = cls()

        for line in iptables_save_content.splitlines():
            if line.startswith('#'):
                continue
            elif line.startswith('*'):
                parser.parse_table(line)
            elif line.startswith(':'):
                parser.parse_chain(line)
            elif line.startswith('-A'):
                parser.parse_chain_rule(line)
            elif line == 'COMMIT':
                parser.commit()
            else:
                print('unknown line={}'.format(line))

        return parser.tables

    def parse_chain(self, line):
        line_split = line[1:].split()
        name = line_split[0]

        current_chain = {
            'rules': [],
        }

        self._current_table.setdefault(name, current_chain)

    def parse_chain_rule(self, line):
        action, chain_name, rule_s = line.split(' ', 2)

        chain = self._current_table[chain_name]

        chain['rules'].append(Rule(rule_s, priority=70))

    def parse_table(self, line):
        name = line[1:].strip()

        self._current_table_name = name
        self._current_table = {}

        self.tables.setdefault(name, self._current_table)
