#!/usr/bin/env python3
import setuptest
import unittest
import RPi.GPIO as GPIO
from heatmaster.actuators.electrovalve import Electrovalve
assert setuptest


class ElectrovalveTest(unittest.TestCase):

    TESTPIN = 67

    def test_BadInit(self):
        with self.assertRaises(ValueError):
            Electrovalve()

    def test_GoodInitPin(self):
        # reset GPIO module import to not interfere between tests
        GPIO.reset_mock()

        rl = Electrovalve(pin=self.TESTPIN)

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
