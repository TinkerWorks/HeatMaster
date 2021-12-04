import setuptest
import unittest
import threading

import paho.mqtt.client as mqtt

from heatmaster.ConfigurationLoader.Parser import Parser
from heatmaster.heatmaster import HeatMaster
assert setuptest


class BasicTest(unittest.TestCase):
    def test_BasicTest(self):
        import os
        absFilePath = os.path.abspath(__file__)
        path, filename = os.path.split(absFilePath)
        confFile = path + "/config-test-simple.json"

        self.client = self.connect_mqtt()
        self.initial_temp = 25

        ps = Parser(confFile)
        hm = HeatMaster(config=ps.getConfiguration())
        self.startPublishing()
        hm.run(5)
        self.stopPublishing()

    def connect_mqtt(self):
        client = mqtt.Client()
        client.connect("mqtt.tinker.haus", 1883)
        return client

    def startPublishing(self):
        self.lasttimer = threading.Timer(1, self.publishTemp)
        self.lasttimer.start()

    def stopPublishing(self):
        self.lasttimer.cancel()

    def publishTemp(self):
        self.startPublishing()
        self.client.publish("testtopic/temperature/current", payload=self.initial_temp)
        self.initial_temp += 0.95
