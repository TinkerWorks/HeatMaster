class Temperature:
    def __init__(self, callback):
        self.setCallback(callback)

    def get():
        raise NotImplementedError

    def setCallback(self, callback):
        self.callback_ = callback
