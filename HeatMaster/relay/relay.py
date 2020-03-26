import RPi.GPIO as GPIO

class Relay:
    def __init__(self, pin):
        self.pin_ = pin

        # for some reason, disable GPIO Warnings
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        # initialize as output and turned ON
        GPIO.setup(self.pin_, GPIO.OUT)
        self.set(True)

    def set(self, onoff):
        if onoff:
            GPIO.output(self.pin_, 1)
            self.state_ = True
        else:
            GPIO.output(self.pin_, 0)
            self.state_ = False


    def on(self):
        self.set(True)

    def off(self):
        self.set(False)
