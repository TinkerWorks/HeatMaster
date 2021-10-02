

class Trigger:
    def __init__(self):
        self.callback_ = None

    def setCallback(self, callback):
        self.callback_ = callback

    def registerCallback(self, children, callback):
        for child in children:
            try:
                child.setCallback(callback)
            except AttributeError:
                self.logger.info("Child {} has no callback".format(child))

    def propagate(self, chain, arg):
        if(chain is None):
            chain = []

        self.logger.info("Propagate from chain {}".format(chain))

        if (self.callback_ is not None):
            chain.append(self)
            self.callback_(chain, arg)
