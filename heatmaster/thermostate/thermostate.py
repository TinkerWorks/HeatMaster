from heatmaster.actuators.relay import Relay
from heatmaster.temperature.temperaturegroup import TemperatureGroup
from heatmaster.ConfigurationLoader.AutoGenerated import AutoGenerated
from heatmaster.utils.trigger import Trigger
from heatmaster.temperature.mqttproxy import MqttProxy

import logging
logger = logging.getLogger(__name__)

MIN_TEMPERATURE = 10
MAX_TEMPERATURE = 40
DEFAULT_TEMPERATURE = 25


class Thermostate(Trigger, AutoGenerated):

    def __init__(self, config=None):
        AutoGenerated.__init__(self)
        Trigger.__init__(self)
        self.__set_point = DEFAULT_TEMPERATURE

        self.classFinder = {"name": self.setName,
                            "relay": Relay,
                            "temperature": TemperatureGroup}

        self.mqtt_ = MqttProxy()

        self.children = self.loadConfig(config)

        self.registerCallback(self.children, self.propagate)

        self.mqtt_.subscribeToTopic(self.generateSetPointTopicSet(),
                                    self.setSetPoint)

    def __str__(self):
        return "Thermostate {} set to {} degrees".format(self.name_, self.__set_point)

    def setName(self, config):
        self.name_ = config

    def generateSetPointTopicSet(self):
        topic = self.generateSetPointTopicState()
        topic += "/" + "set"

        return topic

    def generateSetPointTopicState(self):
        topic = "heatmaster" # TODO: remove hard-coding
        topic += "/" + self.name_
        topic += "/" + "set_point"

        return topic

    def setSetPoint(self, setPoint):
        sp = float(setPoint)

        if (sp < MIN_TEMPERATURE):
            return False
        if (sp > MAX_TEMPERATURE):
            return False

        self.__set_point = sp
        self.mqtt_.publish(self.generateSetPointTopicState(), sp)
        return True
