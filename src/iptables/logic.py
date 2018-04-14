import shlex
import subprocess

from .models import Chain, Table
from .parser import IPTablesParser


class CommandError(Exception):
    pass


def run_command(command: str):
    command_split = shlex.split(command)

    proc = subprocess.Popen(command_split, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    return proc, stdout, stderr


class Executor(object):
    def __call__(self, command):
        full_command = 'iptables {}'.format(command)

        return run_command(full_command)


class Plan(object):
    def __init__(self):
        self.steps = []

    def create_chain(self, table_name, chain_name):
        return self.get_chain(table_name, chain_name, delete_existing=True)

    def execute(self):
        tables = self.get_current_tables()
        tables.executor = Executor()

        for step in self.steps:
            step.modify_tables(tables)

    def get_chain(self, table_name, chain_name, delete_existing=False):
        table = Table(table_name)
        step = Chain(table, chain_name, delete_existing=delete_existing)

        self.steps.append(step)

        return step

    def get_current_tables(self):
        command = 'iptables-save'
        _, stdout, _ = run_command(command)

        return IPTablesParser.parse(stdout.decode('utf8'))
