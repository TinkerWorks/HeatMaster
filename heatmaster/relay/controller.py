import RPi.GPIO as GPIO


class Controller:
    def __init__(self, relays):
        GPIO.setmode(GPIO.BOARD)
        print("Ana are mere!!")

        self.relays = relays

    def turn_it_all_up(self):
        for relay in self.relays:
            GPIO.setup(relay, GPIO.OUT)
            GPIO.output(relay, 1)

    def turn_it_all_down(self):
        for relay in self.relays:
            GPIO.setup(relay, GPIO.OUT)
            GPIO.output(relay, 0)

    def turn_off_relay( relay_name ):
        pin = relays.room_to_relay_board ( relay_name )
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
