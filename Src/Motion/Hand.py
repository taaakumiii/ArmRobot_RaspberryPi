import time
from Motor.Object import Motor
from Motor import Command
HAND_CHANNEL = 0
WRIST_CHANNEL = 1
ANGLE_OFFSET = 40


class Hand:
    def __init__(self):
        self._mHandMotor = Motor(HAND_CHANNEL, 0)
        self._mHandMotor.start()

        self._mWristMotor = Motor(WRIST_CHANNEL, ANGLE_OFFSET)
        self._mWristMotor.start()

    def __del__(self):
        self._mHandMotor.notifyCommand(Command.CLEANUP, None)
        self._mWristMotor.notifyCommand(Command.CLEANUP, None)
        time.sleep(1)
        self._mHandMotor.notifyCommand(Command.FINISH, None)
        self._mWristMotor.notifyCommand(Command.FINISH, None)

    def grab(self, staticallyTime=0.0):
        self._mHandMotor.notifyCommand(Command.SETPOS, [150, staticallyTime])

    def release(self, staticallyTime=0.0):
        self._mHandMotor.notifyCommand(Command.SETPOS, [90, staticallyTime])

    def roll(self, angle, staticallyTime=0.0):
        angle += ANGLE_OFFSET
        self._mWristMotor.notifyCommand(Command.SETPOS, [angle, staticallyTime])

    def wait_hand(self):
        self._mHandMotor.wait()

    def wait_wrist(self):
        self._mWristMotor.wait()
