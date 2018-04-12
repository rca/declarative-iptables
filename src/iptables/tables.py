class IPTables(dict):
    def find_chain(self, table_name, chain_name):
        return self.get(table_name, {}).get(chain_name)

    def find_rule(self, table_name, chain_name, rule):
        chain = self.find_chain(table_name, chain_name)
        if not chain:
            return

        for idx, _rule in enumerate(chain['rules']):
            if _rule == rule:
                return idx, _rule
