from heatmaster.ConfigurationLoader.AutoGenerated import AutoGenerated
from enum import Enum, auto
import RPi.GPIO as GPIO
import threading

from termcolor import colored

from heatmaster.utils import logging
logger = logging.getLogger(__name__)


class Electrovalve(AutoGenerated):

    OPEN_TIME_SECONDS = 1.25 * 60
    CLOSE_TIME_SECONDS = 6.5 * 60

    color = {'OPEN': 'green',
             'OPENNING': 'yellow',
             'CLOSED': 'red',
             'CLOSING': 'magenta'}

    class State(Enum):
        OPENNING = auto()
        CLOSING = auto()
        OPEN = auto()
        CLOSED = auto()

        def __str__(self):
            return colored(self.name, Electrovalve.color[self.name])

    def setPin(self, config):
        self.pin_ = int(config)
        # for some reason, disable GPIO Warnings
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        # initialize as output and turned ON
        GPIO.setup(self.pin_, GPIO.OUT)

    def setDefault(self, config):
        if config == "1":
            self.set(True)
        elif config == "0":
            self.set(False)
        else:
            logger.error("Unrecognized electrovalve default value {}".format(
                    config))

    def __init__(self, config=None, pin=None):
        super().__init__()
        self.classFinder = {"pin": self.setPin,
                            "default": self.setDefault}
        self.state_ = None
        self.progresstimer = None

        if(config):
            self.loadConfig(config)
        elif(pin):
            self.setPin(pin)
        else:
            err = "Electrovalve has to be initialized with a pin or a config"
            raise ValueError(err)

    def set(self, onoff):
        if onoff:
            if (self.state_ == Electrovalve.State.OPEN or
                    self.state_ == Electrovalve.State.OPENNING):
                return
            if self.progresstimer is not None:
                self.progresstimer.cancel()
            GPIO.output(self.pin_, 1)
            self.state_ = Electrovalve.State.OPENNING
            self.progresstimer = threading.Timer(Electrovalve.OPEN_TIME_SECONDS,
                                                 self.confirmOpen)
            self.progresstimer.start()
        else:
            if (self.state_ == Electrovalve.State.CLOSED or
                    self.state_ == Electrovalve.State.CLOSING):
                return
            if self.progresstimer is not None:
                self.progresstimer.cancel()
            GPIO.output(self.pin_, 0)
            self.state_ = Electrovalve.State.CLOSING
            self.progresstimer = threading.Timer(Electrovalve.CLOSE_TIME_SECONDS,
                                                 self.confirmCLOSED)
            self.progresstimer.start()

    def confirmOpen(self):
        self.state_ = Electrovalve.State.OPEN
        self.progresstimer = None

    def confirmCLOSED(self):
        self.state_ = Electrovalve.State.CLOSED
        self.progresstimer = None

    def on(self):
        self.set(True)

    def off(self):
        self.set(False)

    def state(self):
        return self.state_

    def stateStr(self):
#        if self.state_ is None:
#            return "None"
        return str(self.state_)

    def stateBool(self):
        if self.state_ == Electrovalve.State.OPEN:
            return True
        else:
            return False

    def __str__(self):
        return "Electrovalve on pin {} is {}".format(self.pin_, self.stateStr())