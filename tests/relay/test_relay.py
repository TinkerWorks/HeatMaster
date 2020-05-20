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
from actuators.relay import Relay


class RelayTest(unittest.TestCase):

    TESTPIN = 67

    def test_BadInit(self):
        with self.assertRaises(ValueError):
            Relay()

    def test_GoodInitPin(self):
        # reset GPIO module import to not interfere between tests
        GPIO.reset_mock()

        rl = Relay(pin = self.TESTPIN)

        print(str(rl))

    def test_GoodInitConfig(self):
        # reset GPIO module import to not interfere between tests
        GPIO.reset_mock()

        config = {"pin": self.TESTPIN}
        rl = Relay(config)

        print(str(rl))

    def test_SetPin(self):
        # reset GPIO module import to not interfere between tests
        GPIO.reset_mock()
        rl = Relay(pin = self.TESTPIN)
        # Test the initial state of the pin to be set
        GPIO.output.assert_called_once_with(self.TESTPIN, 1)

        GPIO.reset_mock()
        rl.set(0)
        GPIO.output.assert_called_once_with(self.TESTPIN, 0)

        GPIO.reset_mock()
        rl.set(1)
        GPIO.output.assert_called_once_with(self.TESTPIN, 1)

        GPIO.reset_mock()
        rl.on()
        GPIO.output.assert_called_once_with(self.TESTPIN, 1)

        GPIO.reset_mock()
        rl.off()
        GPIO.output.assert_called_once_with(self.TESTPIN, 0)
