import time
import random
import math

from Motion import Hand
from Motion import Arm
from Motion import Base
from Utility.Calc import calc_theta


class Sequence:
    def __init__(self):
        self._mHand = Hand.Hand()
        self._mArm = Arm.Arm()
        self._mBase = Base.Base()

    def __del__(self):
        del self._mHand
        del self._mArm
        del self._mBase

    def _all_wait(self):
        self._mHand.wait_hand()
        self._mHand.wait_wrist()

        self._mArm.wait_first()
        self._mArm.wait_second()
        self._mArm.wait_third()

        self._mBase.wait()

    def initialize(self):
        self._mArm.bend_third(60)
        self._mArm.bend_second(90)
        self._mArm.bend_first(-45, 0.5)
        self._all_wait()

        self._mBase.roll(0, 0.5)
        self._all_wait()

        self._mHand.roll(0, 0.5)
        self._all_wait()

    def grab(self):
        self._mHand.roll(0, 0.5)
        self._mHand.release()
        self._all_wait()

        # 1段目の降下
        self._mArm.bend_third(-15)
        self._mArm.bend_second(100)
        self._mArm.bend_first(-20, 1.5)
        self._all_wait()

        # 2段目の降下
        self._mHand.release()
        self._mArm.bend_third(-22)
        self._mArm.bend_second(125)
        self._mArm.bend_first(-40, 2.0)
        self._all_wait()

        self._mHand.grab(2.0)
        self._all_wait()

    def lift(self):
        self._mArm.bend_third(30, 0.5)
        self._all_wait()

        self._mHand.roll(90, 1.0)

        self._mArm.bend_second(90)
        self._mArm.bend_first(-60, 1.0)
        self._all_wait()

    def put(self, kind):
        if kind == 'EVEN':
            self._mBase.roll(85)
        else:
            self._mBase.roll(50)

        self._mArm.bend_first(-50, 1.0)
        self._all_wait()

        # self._mArm.bend_first(-10, 1.0)
        # self._all_wait()

        if kind == 'EVEN':
            self._mArm.bend_second(95, 1.0)

            self._mArm.bend_third(-10)
            self._mArm.bend_second(125)
            self._mArm.bend_first(-45, 1.5)
        else:
            self._mArm.bend_second(40, 1.0)

            self._mArm.bend_third(-43)
            self._mArm.bend_second(70)
            self._mArm.bend_first(-55, 1.5)

        self._all_wait()

        # 引っ掛かり防止のため、2回リリース
        self._mHand.release(1.0)
        self._all_wait()

    def shoot_pos(self):
        self._mArm.bend_third(100)
        self._mArm.bend_second(100)
        self._mArm.bend_first(-45, 0.5)
        self._all_wait()

        self._mBase.roll(0, 0.5)
        self._all_wait()

        self._mHand.roll(0, 0.5)
        self._all_wait()

    def error(self):
        for i in range(3):
            self._mHand.grab(1.0)
            self._all_wait()

            self._mHand.release(1.0)
            self._all_wait()

    '''
    def test(self, x, y):
        a = y + 50  # ロボット位置が50mm下がっているため
        h = math.fabs(x - 50)
        distance = math.sqrt((a ** 2) + (h ** 2))

        theta_0 = math.degrees(math.atan((h/a)))
        cov_theta_0 = theta_0 - 90
        self._mBase.roll(cov_theta_0)

        theta_1, theta_2, theta_3 = calc_theta(distance)
        cov_theta_1 = theta_1 - 180
        cov_theta_2 = -(theta_2 - 180)
        cov_theta_3 = theta_3 - 180

        self._mHand.release(1.0)
        self._all_wait()

        self._mArm.bend_third(cov_theta_1)
        self._mArm.bend_second(cov_theta_2)
        self._mArm.bend_first(cov_theta_3)
        self._all_wait()

        time.sleep(3)  # 静定待ち

        self._mHand.grab(1.0)
        self._all_wait()
    '''
