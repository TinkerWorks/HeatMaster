#!/usr/bin/env python3
import unittest
import sys

#TODO: This is a way, but overriding __import__ might be better
from mock import Mock,MagicMock
if 'RPi' not in sys.modules.keys():
    sys.modules['RPi'] = Mock()
if 'RPi.GPIO' not in sys.modules.keys():
    sys.modules['RPi.GPIO'] = Mock()

sys.stderr.write ( " sys.path is {} ".format(sys.path))

import RPi.GPIO as GPIO
from heatmaster.actuators.electrovalve import Electrovalve


class ElectrovalveTest(unittest.TestCase):

    TESTPIN = 67

    def test_BadInit(self):
        with self.assertRaises(ValueError):
            Electrovalve()

    def test_GoodInitPin(self):
        # reset GPIO module import to not interfere between tests
        GPIO.reset_mock()

        rl = Electrovalve(pin = self.TESTPIN)

        print(str(rl))

    def test_GoodInitConfig(self):
        # reset GPIO module import to not interfere between tests
        GPIO.reset_mock()

        config = {"pin": self.TESTPIN}
        rl = Electrovalve(config)

        print(str(rl))

    def test_SetPin(self):
        # reset GPIO module import to not interfere between tests
        GPIO.reset_mock()
        rl = Electrovalve(pin=self.TESTPIN)
        # Test the initial state of the pin to be set
        GPIO.output.assert_called_once_with(self.TESTPIN, 1)

        GPIO.reset_mock()
        rl.set(0)
        GPIO.output.assert_called_once_with(self.TESTPIN, 0)

        GPIO.reset_mock()
        rl.set(1)
        GPIO.output.assert_called_once_with(self.TESTPIN, 1)
