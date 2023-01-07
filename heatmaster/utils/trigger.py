from heatmaster.utils import logging
logger = logging.getLogger(__name__)


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
                logger.info("Child {} has no callback".format(child))

    def propagate(self, chain, arg):
        if (chain is None):
            chain = []

        logger.spam("In object \"{}\" -> propagate from top chain {}".
                    format(self, chain))

        if (self.callback_ is not None):
            chain.append(self)
            self.callback_(chain, arg)
