import paho.mqtt.client as mqtt
from temperature.temperature import Temperature
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

    def __init__(self):
        self.classFinder = {"host": self.setHost, "port" : self.setPort}
        self.topicAndHandler = {}
        self.client = mqtt.Client()
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage


    def setHost(self, host):
        self.host_ = host

    def setPort(self, port):
        self.port_ = int(port)

    def loadConfig(self, config):
        print(config)

        for k, v in config.items():
            print (" Key: ", k, " : ", v)
            keyClass = self.classFinder[k]
            print (keyClass)

            o = keyClass(v)

        self.connect()

    def connect(self, host = "", port = 0):
        if(host is not ""):
            self.host_ = host
        if(port is not 0):
            self.port_ = port

        print("Connect to ", self.host_, ":", self.port_)

        self.client.connect_async(self.host_, self.port_, 60)
        self.client.loop_start()

        print("MQTT broker proxy started")

    def subscribeToTopic(self, topic, handler):
        #print("subscribe ", self, " to topic ", topic, " with handler ", handler)

        self.topicAndHandler[topic] = handler

        self.client.loop_stop()
        self.client.subscribe(topic)
        self.client.loop_start()


class MqttTemperature(Temperature):
    def __init__(self, topic = None, updateFunc = None):
        self.topic_ = topic
        self.mqtt_ = MqttProxy()
        self.temperature_ = float('nan')
        self.updateFunc_ = updateFunc

        if(self.topic_ is not None):
            self.subscribe()

    def subscribe(self):
        self.mqtt_.subscribeToTopic(self.topic_, self.updateTemperature)
        print("will sign function ", self.updateTemperature)

    def setTopic(self, topic):
        self.topic_ = topic
        self.subscribe()

    def loadConfig(self, config):
        print(config)

        classFinder = {"topic": self.setTopic}

        for k,v in config.items():
            print (" Key: ", k, " v ", v)
            keyClass = classFinder[k]
            print (keyClass)

            o = keyClass(v)
            #.loadConfig(v)


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
    host = "mqtt.tinker.haus"
    port = 1883

    def updatefunc():
        print ("needchangenow !!\n")

    mqttBroker = MqttProxy(host, port)

    m1 = MqttTemperature("raspberry-sensor-dev/temperature/current", updateFunc = updatefunc)
    m2 = MqttTemperature("raspberry-sensor-dev/humidity/current", updateFunc = updatefunc)


    while True:
        import time

        print("Temperature 1 is ", m1.get())
        print("Temperature 2 is ", m2.get())

        time.sleep(1)
