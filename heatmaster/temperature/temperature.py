from tigger.trigger import Trigger

class Temperature(Trigger):
    def __init__(self):
        pass

    def get(self):
        return self.temperature_
