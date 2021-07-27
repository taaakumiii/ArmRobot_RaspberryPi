import logging
import time
from Motor.Manager import Manager
from Motor import Command
from Motor.AE_PCA9685 import AE_PCA9685


class Motor(Manager):
    _mChannel = 0
    _mOffset = 0
    _mServo = None
    _mPresentValue = 0

    def __init__(self, channel, offset):
        super(Motor, self).__init__()
        self._mChannel = channel
        self._mOffset = offset
        self._mServo = AE_PCA9685.getInstance()

    def __del__(self):
        self._mServo.Cleanup(self._mChannel)

    def executeCommand(self, cmd, params):
        logging.info(f'pin: {self._mChannel}, cmd: {cmd}, params: {params}')

        if Command.SETPOS == cmd:
            angle = params[0] + self._mOffset
            staticallyTime = params[1]
            self._mServo.SetPos(self._mChannel, angle)
            time.sleep(staticallyTime)

        elif Command.CLEANUP == cmd:
            self._mServo.Cleanup(self._mChannel)

    '''
    def _setPos(self, pointAngle):
        # 没
        if self._mPresentValue < pointAngle:
            step = 1
        else:
            step = -1
        for value in range(self._mPresentValue, pointAngle, step):
            print(value)
            angle = value + self._mOffset
            self._mServo.SetPos(self._mChannel, angle)
            time.sleep(0.01)

        angle = pointAngle + self._mOffset
        self._mServo.SetPos(self._mChannel, angle)
        self._mPresentValue = pointAngle
    '''
