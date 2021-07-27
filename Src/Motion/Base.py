import time
from Motor.Object import Motor
from Motor import Command
CHANNEL = 5
ANGLE_OFFSET = 35


class Base:
    def __init__(self):
        self._mMotor = Motor(CHANNEL, ANGLE_OFFSET)
        self._mMotor.start()

    def __del__(self):
        self._mMotor.notifyCommand(Command.CLEANUP, None)
        time.sleep(1)
        self._mMotor.notifyCommand(Command.FINISH, None)

    def roll(self, angle, staticallyTime=0.0):
        self._mMotor.notifyCommand(Command.SETPOS, [angle, staticallyTime])

    def wait(self):
        self._mMotor.wait()
