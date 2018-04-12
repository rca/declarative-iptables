class IPTables(dict):
    def __init__(self, *args, executor=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.executor = executor

    def create_chain(self, table_name, chain_name):
        self.executor('-t {} -N {}'.format(table_name, chain_name))

    def delete_chain(self, table_name, chain_name):
        self.flush_chain(table_name, chain_name)

        self.executor('-t {} -X {}'.format(table_name, chain_name))

    def find_chain(self, table_name, chain_name):
        return self.get(table_name, {}).get(chain_name)

    def flush_chain(self, table_name, chain_name):
        self.executor('-t {} -F {}'.format(table_name, chain_name))

    def find_rule(self, table_name, chain_name, rule):
        chain = self.find_chain(table_name, chain_name)
        if not chain:
            return

        for idx, _rule in enumerate(chain['rules']):
            if _rule == rule:
                return idx, _rule
