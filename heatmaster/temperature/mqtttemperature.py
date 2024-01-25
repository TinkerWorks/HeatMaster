import logging
import datetime
import json
from threading import Timer

from heatmaster.temperature.temperature import Temperature
from heatmaster.ConfigurationLoader.AutoGenerated import AutoGenerated
from heatmaster.temperature.mqttproxy import MqttProxy


class MqttTemperature(Temperature, AutoGenerated):
    def __init__(self, config=None, topic=None, callback=None):
        AutoGenerated.__init__(self)
        Temperature.__init__(self)
        self.mqtt_ = MqttProxy()
        self.temperature_ = float('nan')
        self.classFinder = {"topic": self.setTopic,
                            "weight": self.setWeight,
                            "field": self.setField}
        self.logger = logging.getLogger(self.__class__.__name__)
        self.weight_ = 1
        self.timeout_ = 3600
        self.timestamp_ = 0
        self.timer_ = None
        
        self.setCallback(callback)

        if(topic):
            self.setTopic(topic)
        elif(config):
            self.loadConfig(config)

        self.subscribe()

    def stop(self):
        self.mqtt_.disconnect()

    def subscribe(self):
        self.mqtt_.subscribeToTopic(self.topic_, self.updateTemperature)
        print("will sign function ", self.updateTemperature)

    def setTopic(self, config):
        self.topic_ = config

    def setWeight(self, config):
        self.weight_ = config

    def setField(self, config):
        self.field_ = config

    def updateTemperature(self, arg):
        if self.field_:
            data = json.loads(arg)
            temperature = data[self.field_]
        else:
            temperature = arg
        temperature = float(temperature)

        print("here updateTemperature ", self, " with: ", temperature)

        self.temperature_ = temperature
        self.timestamp_ = datetime.datetime.now().timestamp()

        if self.timer_:
            self.timer_.cancel()
        self.timer_ = Timer(self.timeout_, self.timeoutClearValeue)
        self.timer_.start()
        
        self.propagate(None, self.temperature_)

    def timeoutClearValeue(self):
        self.temperature_ = float('nan')
        self.propagate(None, self.temperature_)

    def __str__(self):
        return "MQTT-driven temperature input from {} is {}".format(self.topic_, self.value())


if __name__ == "__main__":
    host = "mqtt.tinker.haus"
    port = 1883

    def updatefunc():
        print("needchangenow !!\n")

    mqttBroker = MqttProxy(host, port)

    m1 = MqttTemperature("hsh/sensors-office/temperature/value",
                         callback=updatefunc)
    m2 = MqttTemperature("hsh/sensors-kitchen/temperature/value",
                         callback=updatefunc)

    while True:
        import time

        print("Temperature 1 is ", m1.get())
        print("Temperature 2 is ", m2.get())

        time.sleep(1)
