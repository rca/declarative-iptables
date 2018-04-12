class Chain(object):
    def __init__(self, name, delete_existing=False):
        self.name = name
        self.delete_existing = delete_existing

        self.rules = []

    def add_rule(self, rule):
        if isinstance(rule, str):
            rule_obj = Rule(str)
        else:
            rule_obj = rule

        self.rules.append(rule_obj)

    @property
    def jump(self):
        return f'-j {self.name}'


class Rule(object):
    def __init__(self, rule: str, priority: int=50, **kwargs):
        self.rule = rule
        self.priority = priority

    def __eq__(self, other):
        return self.rule == other.rule

    def __repr__(self):
        return f'<Rule: {self}>'

    def __str__(self):
        return str(self.rule)
