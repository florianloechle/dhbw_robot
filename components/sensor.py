import time
import math
from shared.utils import omit_range


# try to import the GPIO module on the raspberry pi
# fallback to the mock implementation for dev and testing
try:
    import RPi.GPIO as gpio
except ImportError:
    import components.gpio as gpio


class Sensor():
    def __init__(self, pinConfiguration):
        pinTrigger, pinEcho = pinConfiguration
        # Pins
        self.pinTrigger = pinTrigger
        self.pinEcho = pinEcho

        # Setup pins as output
        gpio.setup(self.pinTrigger, gpio.OUT)
        gpio.setup(self.pinEcho, gpio.IN)

        # current distance
        self.distance = None

    def get_distance(self):
        """
        Get the current distance in cm.
        """

        gpio.output(self.pinTrigger, True)
        time.sleep(0.00001)
        gpio.output(self.pinTrigger, False)
        startZeit = time.time()
        while gpio.input(self.pinEcho) == 0:
            startZeit = time.time()

        while gpio.input(self.pinEcho) == 1:
            stopZeit = time.time()

        timeElapsed = stopZeit - startZeit
        #self.distance = omit_range((timeElapsed * 34300) / 2, self.distance, 4)
        return (timeElapsed * 34300) / 2
