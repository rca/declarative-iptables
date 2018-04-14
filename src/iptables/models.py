class Chain(object):
    built_in_chains = (
        'FORWARD',
        'INPUT',
        'OUTPUT',
        'POSTROUTING',
        'PREROUTING',
    )

    def __init__(self, table, name, default_policy='drop', delete_existing=False):
        self.table = table
        self.name = name
        self.delete_existing = delete_existing

        self.table.add_chain(self)

        self.rules = []

        self.default_policy = default_policy

    def __str__(self):
        return str(self.name)

    def add_rule(self, rule):
        if isinstance(rule, str):
            rule_obj = Rule(rule)
        else:
            rule_obj = rule

        self.rules.append(rule_obj)

    def get_full_rule(self, rule_s: str):
        return self.table.get_full_rule('-A {} {}'.format(self.name, rule_s))

    @property
    def jump(self):
        return '-j {}'.format(self.name)

    def modify_tables(self, tables):
        existing_rules = []
        new_rules = []

        create_chain = True
        chain = tables.find_chain(self.table.name, self.name)
        if chain:
            create_chain = False

            if self.delete_existing:
                tables.flush_chain(self.table.name, self.name)

                existing_rules = []
            else:
                existing_rules = chain['rules']

        # only create a chain if it's not a built-in one
        if create_chain and self.name not in self.built_in_chains:
            tables.executor(self.table.get_full_rule('-N {}'.format(self)))

        # set the default policy
        tables.executor(self.table.get_full_rule('-P {} {}'.format(self, self.default_policy.upper())))

        # go through the existing rules and prune out any of the ones
        # being declared
        for rule in self.rules:
            while rule in existing_rules:
                idx = existing_rules.index(rule)
                existing_rules.pop(idx)

                tables.executor('-t {} -D {} {}'.format(self.table, self, idx+1))

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

    def get_full_rule(self, rule_s: str):
        return '-t {} {}'.format(self, rule_s)
