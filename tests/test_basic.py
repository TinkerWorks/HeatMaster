import sys
print(sys.path)

#TODO: This is a way, but overriding __import__ might be better
from mock import Mock
if 'RPi' not in sys.modules.keys():
    sys.modules['RPi'] = Mock()
if 'RPi.GPIO' not in sys.modules.keys():
    sys.modules['RPi.GPIO'] = Mock()

from heatmaster.ConfigurationLoader.Parser import Parser
from heatmaster.ConfigurationLoader.AutoGenerated import AutoGenerated

from heatmaster.thermostate.thermostategroup import ThermostateGroup
from heatmaster.temperature.mqttproxy import MqttProxy
from heatmaster.heater.heater import Heater
from heatmaster.utils.trigger import Trigger
from heatmaster.heatmaster import HeatMaster
from heatmaster.utils import logging

from heatmaster.actuators.electrovalve import Electrovalve

from threading import Event
import time
import logging
import unittest
import threading

import paho.mqtt.client as mqtt

Electrovalve.OPEN_TIME_SECONDS  = 1
Electrovalve.CLOSE_TIME_SECONDS = 2

class BasicTest(unittest.TestCase):
    def test_BasicTest(self):
        import sys
        import os
        absFilePath = os.path.abspath(__file__)
        path, filename = os.path.split(absFilePath)
        confFile = path + "/config-test-simple.json"

        self.client = self.connect_mqtt()
        self.initial_temp = 25

        ps = Parser(confFile)
        hm = HeatMaster(config = ps.getConfiguration())
        self.startPublishing()
        hm.run(10)
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
