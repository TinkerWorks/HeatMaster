from ConfigurationLoader.Parser import Parser
from ConfigurationLoader.AutoGenerated import AutoGenerated

from thermostate.thermostate import Thermostate
from temperature.mqttproxy import MqttProxy

class HeatMaster(AutoGenerated):

    def __init__(self, config = None):
        super()
        self.classFinder = {"mqtt": MqttProxy, "thermostates" : Thermostate}

        if(config):
            self.loadConfig(config)


if __name__ == "__main__":
    import sys
    confFile = sys.argv[1]
    ps = Parser(confFile)

    hm = HeatMaster(config = ps.getConfiguration())
