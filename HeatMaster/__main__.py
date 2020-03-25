import time
import RPi.GPIO as GPIO

from relay.initializer import Initialiser
from relay.controller import Controller

GPIO.setmode(GPIO.BOARD)


def main():
    li = Initialiser()
    lc = Controller(li.relays)

    GPIO.setwarnings(False)

    #switch
    GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    #RELAY
    GPIO.setup(29, GPIO.OUT)

    def handle_switch(pin):

        switch = GPIO.input(31)

        print ("Switch is ", switch)

        relay = 13

        if switch:
            GPIO.output(29, 1)

        else:
            GPIO.output(29, 0)



    GPIO.add_event_detect(31, GPIO.BOTH, handle_switch)

    print( "Turn it all ON !!! \n")
    lc.turn_it_all_up()

    while(True):
        handle_switch(0);

        time.sleep(10)


if __name__ == "__main__":
    main()
