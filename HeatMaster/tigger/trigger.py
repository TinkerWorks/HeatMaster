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
                print ("Child ", child, " has no callback")

    def propagate(self, chain, arg):
        if(chain is None):
            chain = []

        print("Propagate from chain ", chain)

        if (self.callback_):
            chain.append(self)
            self.callback_(chain, arg)
