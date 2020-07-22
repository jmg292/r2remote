class BaseCommandHandler(object):

    def __init__(self, config):
        self.config = config

    def handle(self, *args):
        raise NotImplementedError(f"{self.__class__.__name__} does not implement the handle method.")