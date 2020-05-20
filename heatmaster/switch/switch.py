import RPi.GPIO as GPIO

class Switch:
    def __init__(self, pin, led_pin):
        self.pin_ = pin
        self.led_pin_ = led_pin

        # for some reason, disable GPIO Warnings
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.pin_, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.state_ = GPIO.input(31)
        GPIO.add_event_detect(self.pin_, GPIO.BOTH, self.handle_switch)

        GPIO.setup(self.led_pin_, GPIO.OUT)
        GPIO.output(self.led_pin_, self.state_)

    def handle_switch(self, pin):
        self.state_ = GPIO.input(31)

        GPIO.output(self.led_pin_, self.state_)

        print ("Switch is ", self.state_)
