from ConfigurationLoader.AutoGenerated import AutoGenerated
from temperature.DaikinTemperature import DaikinTemperature
from temperature.mqtttemperature   import MqttTemperature


class TemperatureFactory(AutoGenerated):
    def __init__(self, config):
        print(config)

        self.classFinder = {"mqtt": MqttTemperature,
                            "daikin" : DaikinTemperature}

        self.loadListConfig(config)
