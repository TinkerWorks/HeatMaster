from heatmaster.ConfigurationLoader.AutoGenerated import AutoGenerated
from enum import Enum
import RPi.GPIO as GPIO
import threading


class Relay(AutoGenerated):

    OPEN_TIME_SECONDS = 1.25 * 60
    CLOSE_TIME_SECONDS = 6.5 * 60

    class State(Enum):
        OPENNING = 1
        CLOSING = 2
        OPEN = 3
        CLOSED = 4

    def setPin(self, config):
        self.pin_ = int(config)

    def __init__(self, config=None, pin=None):
        super().__init__()
        self.classFinder = {"pin": self.setPin}

        if(config):
            self.loadConfig(config)
        elif(pin):
            self.setPin(pin)
        else:
            err = "Relay has to be initialized with a pin or a config"
            raise ValueError(err)

        self.progresstimer = None
        
        # for some reason, disable GPIO Warnings
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        # initialize as output and turned ON
        GPIO.setup(self.pin_, GPIO.OUT)
        self.set(True)

    def set(self, onoff):
        if self.progresstimer is not None:
            self.progresstimer.cancel()
        if onoff:
            GPIO.output(self.pin_, 1)
            self.state_ = Relay.State.OPENNING
            self.progresstimer = threading.Timer(Relay.OPEN_TIME_SECONDS,
                                                 self.confirmOpen)
            self.progresstimer.start()
        else:
            GPIO.output(self.pin_, 0)
            self.state_ = Relay.State.CLOSING
            self.progresstimer = threading.Timer(Relay.CLOSE_TIME_SECONDS,
                                                 self.confirmCLOSED)
            self.progresstimer.start()

    def confirmOpen(self):
        self.state_ = Relay.State.OPEN
        self.progresstimer = None

    def confirmCLOSED(self):
        self.state_ = Relay.State.CLOSED
        self.progresstimer = None

    def on(self):
        self.set(True)

    def off(self):
        self.set(False)

    def state(self):
        return self.state_

    def stateStr(self):
        return self.state_.name

    def __str__(self):
        return "Relay for pin {} is {}".format(self.pin_, self.stateStr())
