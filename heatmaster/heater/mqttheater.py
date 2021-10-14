from heatmaster.ConfigurationLoader.AutoGenerated import AutoGenerated
from heatmaster.temperature.mqttproxy import MqttProxy
from heatmaster.utils.trigger import Trigger
import datetime
import json

from heatmaster.utils import logging
logger = logging.getLogger(__name__)


class MqttHeater(Trigger, AutoGenerated):
    def __init__(self, config=None, topic=None):
        AutoGenerated.__init__(self)
        self.mqtt_ = MqttProxy()

        self.classFinder = {
            "heatingActive": self.setHeatingActiveTopic,
            "burnerPower": self.setBurnerPowerTopic,
            "tapWaterActive": self.setTapWaterTopic}

        if(topic):
            self.setTopic(topic)
        elif(config):
            self.loadConfig(config)

        self.__heatingActive = False

        self.topics = {""}

    def setTapWaterTopic(self, config):
        pass  # TODO: implement

    def setHeatingActiveTopic(self, config):
        self.__heatingActiveTopic = config
        self.mqtt_.subscribeToTopic(self.__heatingActiveTopic, self.updateHeatingActiveState)

    def setBurnerPowerTopic(self, config):
        self.__burnerPowerTopic = config

    def setBurnerPower(self, percent):
        if percent < 0:
            percent = 0
        if percent > 99:
            percent = 99
        command = {
            "cmd": "heatingcircuitpower",
            "data": percent}
        command_json = json.dumps(command)

        self.mqtt_.publish(self.__burnerPowerTopic, command_json)

    def setBurnerOnOff(self, onoff):
        power = 0
        if onoff:
            power = 99

        self.setBurnerPower(power)

    def stop(self):
        self.mqtt_.disconnect()

    def convertStringToTrueFalse(self, binaryvalue):
        onoffstring = binaryvalue.decode("utf-8")
        if (onoffstring is None):
            raise(Hell)
        elif (onoffstring == "0"):
            return False
        elif (onoffstring == "1"):
            return True
        elif (onoffstring.lower() == "on"):
            return True
        elif (onoffstring.lower() == "off"):
            return False
        else:
            raise(Hell)

    def updateHeatingActiveState(self, arg):
        print("here updateState ", self, " with: ", arg)
        state = self.convertStringToTrueFalse(arg)

        self.__heatingActive = state
        self.timestamp_ = datetime.datetime.now().timestamp()

        self.propagate(None, self.__heatingActive)

    def __str__(self):
        s = "MqttHeater {}".format(self.__heatingActive)
        return s

    def on(self):
        pass

    def off(self):
        pass

    def setHeating(self, heating):
        logger.warn("set heating to {}".format(heating))

        if self.__heatingActive != heating:
            self.setBurnerOnOff(heating)
