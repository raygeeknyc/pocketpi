import logging
import time
import RPi.GPIO as GPIO
import threading
import sys

logging.getLogger().setLevel(logging.INFO)
# Demo pin definitions:
redPin = 2
greenPin = 3
bluePin = 4


RED = (True, False, False)
GREEN = (False, True, False)
BLUE = (False, False, True)
WHITE = (True, True, True)
YELLOW = (True, True, False)
CYAN = (False, True, True)
MAGENTA = (True, False, True)
OFF = (False, False, False)

class RgbLed:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    def __init__(self, redPin, greenPin, bluePin, common_anode=True):
        if common_anode:
            self._ON_STATE=GPIO.LOW
            self._OFF_STATE=GPIO.HIGH
        else:
            self._ON_STATE=GPIO.HIGH
            self._OFF_STATE=GPIO.LOW

        self._redPin = redPin
        self._greenPin = greenPin
        self._bluePin = bluePin

        GPIO.setup(self._redPin, GPIO.OUT)
        GPIO.setup(self._greenPin, GPIO.OUT)
        GPIO.setup(self._bluePin, GPIO.OUT)
        self.setColor(OFF)

    def setColor(self, rgb):
        self._color = rgb
        GPIO.output(self._redPin, self._ON_STATE if rgb[0] else self._OFF_STATE)
        GPIO.output(self._greenPin, self._ON_STATE if rgb[1] else self._OFF_STATE)
        GPIO.output(self._bluePin, self._ON_STATE if rgb[2] else self._OFF_STATE)

    def stop(self):
        self._stop = True

    def cycle(self, interval_secs):
        self._interval_secs = interval_secs
        self.setColor(RED)
        self._stop = False
        while not self._stop:
            time.sleep(self._interval_secs)
            self._cycleColor()

    def _cycleColor(self):
        if self._color is RED:
            self.setColor(GREEN)
        elif self._color is GREEN:
            self.setColor(BLUE)
        elif self._color is BLUE:
            self.setColor(CYAN)
        elif self._color is CYAN:
            self.setColor(YELLOW)
        elif self._color is YELLOW:
            self.setColor(WHITE)
        elif self._color is WHITE:
            self.setColor(OFF)
        elif self._color is OFF:
            self.setColor(RED)

def runDemo(demo):
    print("OFF")
    demo.setColor(OFF)
    time.sleep(2)
    print("R")
    demo.setColor(RED)
    time.sleep((1))
    print("G")
    demo.setColor(GREEN)
    time.sleep((1))
    print("B")
    demo.setColor(BLUE)
    time.sleep((1))
    print("OFF")
    demo.setColor(OFF)
    time.sleep(2)
    demo.setColor(CYAN)
    time.sleep((0.5))
    demo.setColor(YELLOW)
    time.sleep((0.5))
    demo.setColor(MAGENTA)
    time.sleep((0.5))
    demo.setColor(WHITE)
    time.sleep((0.5))
    demo.setColor(OFF)
    sleepLed = threading.Thread(target = demo.cycle, args=(2,))
    sleepLed.start()
    response = raw_input("waiting for you before stopping... ")
    demo.stop()
    print "waiting for LED to stop cycling"
    sleepLed.join()
    demo.setColor(OFF)

if __name__ == "__main__":
    led = RgbLed(redPin, greenPin, bluePin, common_anode=False)
    led.setColor(OFF)
    if len(sys.argv) > 1:
        r,g,b = sys.argv[1].split(",")
        logging.debug("R,G,B=({},{},{})".format(r,g,b))
        led.setColor((int(r),int(g),int(b)))
        time.sleep(5)
    else:
        runDemo(led)
        GPIO.cleanup()
    sys.exit()
