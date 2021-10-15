import paho.mqtt.client as mqtt
from heatmaster.ConfigurationLoader.AutoGenerated import AutoGenerated


class MqttSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = \
                super(MqttSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MqttProxy(AutoGenerated, metaclass=MqttSingleton):

    def onConnect(self, client, userdata, flags, rc):
        # Subscribing in onConnectDispatcher() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        for topic, handler in self.topicAndHandler.items():
            self.client.subscribe(topic)

    def onMessage(self, client, userdata, msg):

        handlerList = self.topicAndHandler[msg.topic]
        for handler in handlerList:
            print("will call function ", handler)
            handler(msg.payload)

    def onLog(self, mqttc, obj, level, string):
        print(string)

    def __init__(self):
        super().__init__()

        self.topicAndHandler = {}
        self.client = mqtt.Client()
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.on_log = self.onLog

    def initializeConfig(config):
        mq = MqttProxy()
        mq.classFinder = {"host": mq.setHost,
                          "port": mq.setPort}
        mq.loadConfig(config)
        mq.connect()

    def setHost(self, config):
        self.host_ = config

    def setPort(self, config):
        self.port_ = int(config)

    def connect(self, host="", port=0):
        if(host != ""):
            self.host_ = host
        if(port != 0):
            self.port_ = port

        print("Connect to ", self.host_, ":", self.port_)

        self.client.connect_async(self.host_, self.port_, 60)
        self.client.loop_start()

        print("MQTT broker proxy started")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def subscribeToTopic(self, topic, handler):
        try:
            self.topicAndHandler[topic].append(handler)
        except KeyError:
            self.topicAndHandler[topic] = [handler]

        print("GOt to list: ", self.topicAndHandler[topic])

        self.client.loop_stop()
        self.client.subscribe(topic)
        self.client.loop_start()

    def publish(self, topic, payload, retain=False):
        self.client.publish(topic, payload=payload, retain=retain)
