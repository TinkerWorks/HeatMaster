from ConfigurationLoader.Parser import Parser
from temperature.mqtttemperature import MqttProxy
from thermostate.thermostate import Thermostate

class HeatMaster:

    def __init__(self):
        self.classFinder = {"mqtt": MqttProxy, "thermostates" : Thermostate}

    def loadConfig(self, config):
        print(config)

        for k, v in config.items():
            print (" Key: ", k, " : ", v)
            keyClass = self.classFinder[k]
            print (keyClass)

            o = keyClass()
            o.loadConfig(v)


if __name__ == "__main__":
    import sys
    confFile = sys.argv[1]
    ps = Parser(confFile)

    hm = HeatMaster()
    hm.loadConfig(ps.getConfiguration())
