from .models import Chain

class Plan(object):
    def __init__(self):
        self.steps = []

    def create_chain(self, name):
        return self.get_chain(name, delete_existing=True)

    def execute(self):
        print(self.steps)

    def get_chain(self, name, delete_existing=False):
        step = Chain(name, delete_existing=delete_existing)

        self.steps.append(step)

        return step
