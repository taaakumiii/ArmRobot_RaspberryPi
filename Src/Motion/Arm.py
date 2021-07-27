import time
from Motor.Object import Motor
from Motor import Command
FIRST_CHANNEL = 2
SECOND_CHANNEL = 3
THIRD_CHANNEL = 4
FIRST_ANGLE_OFFSET = 180
SECOND_ANGLE_OFFSET = 60
THIRD_ANGLE_OFFSET = 100


class Arm:
    def __init__(self):
        self._mFirstMotor = Motor(FIRST_CHANNEL, FIRST_ANGLE_OFFSET)
        self._mFirstMotor.start()

        self._mSecondMotor = Motor(SECOND_CHANNEL, SECOND_ANGLE_OFFSET)
        self._mSecondMotor.start()

        self._mThirdMotor = Motor(THIRD_CHANNEL, THIRD_ANGLE_OFFSET)
        self._mThirdMotor.start()

    def __del__(self):
        self._mFirstMotor.notifyCommand(Command.CLEANUP, None)
        self._mSecondMotor.notifyCommand(Command.CLEANUP, None)
        self._mThirdMotor.notifyCommand(Command.CLEANUP, None)
        time.sleep(1)
        self._mFirstMotor.notifyCommand(Command.FINISH, None)
        self._mSecondMotor.notifyCommand(Command.FINISH, None)
        self._mThirdMotor.notifyCommand(Command.FINISH, None)

    def bend_first(self, angle, staticallyTime=0.0):
        self._mFirstMotor.notifyCommand(Command.SETPOS, [angle, staticallyTime])

    def bend_second(self, angle, staticallyTime=0.0):
        self._mSecondMotor.notifyCommand(Command.SETPOS, [angle, staticallyTime])

    def bend_third(self, angle, staticallyTime=0.0):
        self._mThirdMotor.notifyCommand(Command.SETPOS, [angle, staticallyTime])

    def wait_first(self):
        self._mFirstMotor.wait()

    def wait_second(self):
        self._mSecondMotor.wait()

    def wait_third(self):
        self._mThirdMotor.wait()
