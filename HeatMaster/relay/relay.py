try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError as e:
    print ("Running on PC, so ", e, " is FIIIIIINE!!!!")

class Relay:
    def __init__(self, pin):
        self.pin_ = pin

        try:
            # for some reason, disable GPIO Warnings
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)

            # initialize as output and turned ON
            GPIO.setup(self.pin_, GPIO.OUT)
            self.set(True)
        except NameError as e:
            print ("Running on PC, so ", e, " is FIIIIIINE!!!!")


    def set(self, onoff):
        try:
            if onoff:
                GPIO.output(self.pin_, 1)
                self.state_ = True
            else:
                GPIO.output(self.pin_, 0)
                self.state_ = False
        except NameError as e:
            print ("Running on PC, so ", e, " is FIIIIIINE!!!!")


    def on(self):
        self.set(True)

    def off(self):
        self.set(False)
