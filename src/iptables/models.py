class Chain(object):
    def __init__(self, table, name, delete_existing=False):
        self.table = table
        self.name = name
        self.delete_existing = delete_existing

        self.table.add_chain(self)

        self.rules = []

    def __str__(self):
        return str(self.name)

    def add_rule(self, rule):
        if isinstance(rule, str):
            rule_obj = Rule(rule)
        else:
            rule_obj = rule

        self.rules.append(rule_obj)

    def get_full_rule(self, rule_s: str):
        return '-t {} -A {} {}'.format(self.table, self.name, rule_s)

    @property
    def jump(self):
        return '-j {}'.format(self.name)

    def modify_tables(self, tables):
        existing_rules = []
        new_rules = []

        chain = tables.find_chain(self.table.name, self.name)
        if chain and self.delete_existing:
            tables.flush_chain(self.table.name, self.name)

            existing_rules = []
        elif chain:
            existing_rules = chain['rules']

        # go through the existing rules and prune out any of the ones
        # being declared
        for rule in self.rules:
            if rule in existing_rules:
                idx = existing_rules.index(rule)
                existing_rules.pop(idx)

            new_rules.append(rule)

        new_rules.extend(existing_rules)

        for rule in sorted(new_rules, key=lambda x: -x.priority):
            tables.executor(self.get_full_rule(rule))


class Rule(object):
    def __init__(self, rule: str, priority: int=50, **kwargs):
        self.rule = rule
        self.priority = priority

    def __eq__(self, other):
        return self.rule == other.rule

    def __repr__(self):
        return '<Rule: {}>'.format(self)

    def __str__(self):
        return str(self.rule)


class Table(object):
    valid_tables = (
        'raw',
        'filter',
        'nat',
        'mangle',
        'security',
    )

    def __init__(self, name):
        if name not in self.valid_tables:
            raise TableError('table name={} is not valid'.format(name))

        self.name = name
        self.chains = []

    def __str__(self):
        return str(self.name)

    def add_chain(self, chain):
        self.chains.append(chain)
