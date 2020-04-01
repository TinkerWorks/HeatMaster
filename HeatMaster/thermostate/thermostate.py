from relay.relay import Relay
from temperature.temperaturefactory import TemperatureFactory

from relay.relay import Relay

class Thermostate:

    def __init__(self):
        self.classFinder = {"name": self.setName, "relay" : Relay, "temperature" : TemperatureFactory.loadConfig}

        print (" This is a thermostate !!! ")
        print (" I AM ALIVE !! ")

    def setName(self, name):
        self.name_ = name

    def loadConfig(self, config):
        print(config)

        for th in config:
            for k, v in th.items():
                print (" Key: ", k, " : ", v)

                keyClass = self.classFinder[k]
                print (keyClass)

                o = keyClass(v)
                #o.loadConfig(v)
