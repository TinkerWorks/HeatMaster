from temperature.DaikinTemperature import DaikinTemperature
from temperature.mqtttemperature   import MqttTemperature


class TemperatureFactory:


    def loadConfig(config):
        print(config)

        classFinder = {"mqtt": MqttTemperature,
                       "daikin" : DaikinTemperature}

        for ts in config:
            print ("Temperature sensor: ", ts)
            for k,v in ts.items():
                print (" Key: ", k, " v ", v)
                keyClass = classFinder[k]
                print (keyClass)

                o = keyClass()
                o.loadConfig(v)
