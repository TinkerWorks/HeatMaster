import paho.mqtt.client as mqtt
from temperature import Temperature
import datetime;

class MqttSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MqttSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MqttProxy(metaclass=MqttSingleton):
    def onConnect(self, client, userdata, flags, rc):
        # Subscribing in onConnectDispatcher() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        for topic, handler in topicAndHandler:
            self.client.subscribe(topic)

    def onMessage(self, client, userdata, msg):

        handler = self.topicAndHandler[msg.topic]
        #print("will call function ", handler)
        handler(msg.payload)

    def __init__(self, address, port):
        self.topicAndHandler = {}
        self.client = mqtt.Client()
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage

        print("Connect to ", address, ":", port)

        self.client.connect_async(address, port, 60)
        self.client.loop_start()

    def subscribeToTopic(self, topic, handler):
        #print("subscribe ", self, " to topic ", topic, " with handler ", handler)

        self.topicAndHandler[topic] = handler

        self.client.loop_stop()
        self.client.subscribe(topic)
        self.client.loop_start()


class MqttTemperature(Temperature):
    def __init__(self, address, port, topic, updateFunc = None):
        self.topic_ = topic
        self.mqtt_ = MqttProxy(address, port)
        self.temperature_ = float('nan')
        self.updateFunc_ = updateFunc

        self.mqtt_.subscribeToTopic(self.topic_, self.updateTemperature)
        print("will sign function ", self.updateTemperature)


    def updateTemperature(self, temp):
        print("updateTemperature with: ", temp)
        self.temperature_ = float(temp)
        self.timestamp_ = datetime.datetime.now().timestamp()

        if (self.updateFunc_ is not None):
            self.updateFunc_()

    def get(self):
        return self.temperature_

    def getTime(self):
        return self.timestamp_


if __name__ == "__main__":
    address = "mqtt.tinker.haus"
    port = 1883

    def updatefunc():
        print ("needchangenow !!\n")

    m1 = MqttTemperature(address, port, "raspberry-sensor-dev/temperature/current", updateFunc = updatefunc)
    m2 = MqttTemperature(address, port, "raspberry-sensor-dev/humidity/current", updateFunc = updatefunc)


    while True:
        import time

        print("Temperature 1 is ", m1.get())
        print("Temperature 2 is ", m2.get())

        time.sleep(1)
