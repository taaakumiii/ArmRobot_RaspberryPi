import time
import Adafruit_PCA9685


class AE_PCA9685:
    __instance = None

    @staticmethod
    def getInstance():
        if AE_PCA9685.__instance is None:
            AE_PCA9685()
        return AE_PCA9685.__instance

    def __init__(self):
        if AE_PCA9685.__instance is not None:
            raise Exception("Singletonクラス")
        else:
            # Adafruit_PCA9685の初期化
            self.mPwm = Adafruit_PCA9685.PCA9685(address=0x40)  # address:PCA9685のI2C Channel 0x40
            self.mPwm.set_pwm_freq(60)  # 本当は50Hzだが60Hzの方がうまくいく
            print("init")

            AE_PCA9685.__instance = self

    def __del__(self):
        pass

    def SetPos(self, channel, pos):
        # pulse = 150～650 : 0 ～ 180deg
        pulse = (650 - 150) * pos / 180 + 150
        self.mPwm.set_pwm(channel, 0, int(pulse))

    def Cleanup(self, channel):
        # サーボを10degにセットしてから、インプットモードにしておく
        self.SetPos(channel, 90)
        time.sleep(1)
