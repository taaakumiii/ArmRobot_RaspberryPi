import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
ERROR_TYPE_RECOG_ERROR = [8, 21]


class SwitchBoxManager:
    def __init__(self):
        self.__mInputPin = 24
        GPIO.setup(self.__mInputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.__mLedPin_list = [8, 7, 12, 16, 20, 21]
        for pin in self.__mLedPin_list:
            GPIO.setup(pin, GPIO.OUT)

    def clearLed(self):
        for pin in self.__mLedPin_list:
            GPIO.output(pin, GPIO.LOW)

    def waitSwitch(self):
        while True:
            if GPIO.input(self.__mInputPin) == GPIO.HIGH:
                break
            time.sleep(0.01)

    def setDiceEyes(self, num):
        self.clearLed()
        for pin in self.__mLedPin_list[:num]:
            GPIO.output(pin, GPIO.HIGH)

    def setErrorPut(self, kind):
        self.clearLed()
        if kind == 0:
            for pin in ERROR_TYPE_RECOG_ERROR:
                GPIO.output(pin, GPIO.HIGH)
