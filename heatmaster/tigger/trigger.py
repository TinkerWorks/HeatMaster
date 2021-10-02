import logging

class Trigger:
    def __init__(self):
        pass

    def setCallback(self, callback):
        self.callback_ = callback

    def registerCallback(self, children, callback):
        for child in children:
            try:
                child.setCallback(callback)
            except AttributeError as e:
                self.logger.info ("Child {} has no callback".format(child))

    def propagate(self, chain, arg):
        if(chain is None):
            chain = []

        self.logger.info("Propagate from chain {}".format(chain))

        if (self.callback_ is not None):
            chain.append(self)
            self.callback_(chain, arg)
