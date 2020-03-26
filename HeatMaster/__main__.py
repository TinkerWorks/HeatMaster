import time
import RPi.GPIO as GPIO

from relay.initializer import Initialiser
from relay.controller import Controller

from switch.switch import Switch
from relay.relay import Relay

from temperature.temperature import MqttTemperature

from

def main():
    li = Initialiser()
    lc = Controller(li.relays)


    sw = Switch(31, 29)
    rls = []

    mqtemp = MqttTemperature("raspberry-sensor-dev/temperature/current")

    for rpin in li.relays:
        print("Setting up relay %d" % rpin)
        rl = Relay(rpin)
        rls.append(rl)


    while(True):
        print( "Turn it all ON !!! \n")
        for relay in rls:
            relay.on()

        time.sleep(1)

if __name__ == "__main__":
    main()
