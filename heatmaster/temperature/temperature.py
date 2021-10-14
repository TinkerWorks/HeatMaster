from heatmaster.utils.trigger import Trigger


class Temperature(Trigger):
    def __init__(self):
        Trigger.__init__(self)
        pass

    def value(self):
        return self.temperature_

    def timeUpdate(self):
        return self.timestamp_
