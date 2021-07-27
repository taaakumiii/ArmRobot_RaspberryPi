import math
import random
LINE_1 = 115
LINE_2 = 105
LINE_3 = 100
LINE_4 = 160
LINE_5 = 20


class ArmSim:
    mTheta_1 = 0
    mTheta_2 = 0
    mTheta_3 = 0
    __mX = 0
    __mY = 0
    mE = 0

    def __init__(self, x, y, theta_1=None, theta_2=None, theta_3=None):
        if (theta_1 is None) or (theta_2 is None) or (theta_3 is None):  # どれか1つでもからの場合ランダムにする
            theta_1 = random.randrange(90, 270, 1)
            theta_2 = random.randrange(90, 180, 1)
            theta_3 = random.randrange(0, 180, 1)

        self.mTheta_1 = theta_1
        self.mTheta_2 = theta_2
        self.mTheta_3 = theta_3
        self.__mX = x
        self.__mY = y

    def reset(self):
        self.mTheta_1 = random.randrange(90, 270, 1)
        self.mTheta_2 = random.randrange(90, 180, 1)
        self.mTheta_3 = random.randrange(-45, 0, 1)

    def set_theta(self, theta_1=None, theta_2=None, theta_3=None):
        if theta_1 is not None:
            self.mTheta_1 = theta_1

        if theta_2 is not None:
            self.mTheta_2 = theta_2

        if theta_3 is not None:
            self.mTheta_3 = theta_3

    def __repr__(self):
        return repr(self.mE)

    def update(self):
        self.mTheta_1 += random.randrange(-10, 10, 1)
        if self.mTheta_1 > 270:
            self.mTheta_1 = 270
        elif self.mTheta_1 < 90:
            self.mTheta_1 = 90

        self.mTheta_2 += random.randrange(-10, 10, 1)
        if self.mTheta_2 > 180:
            self.mTheta_2 = 180
        elif self.mTheta_2 < 90:
            self.mTheta_2 = 90

        self.mTheta_3 += random.randrange(-10, 10, 1)
        if self.mTheta_3 > 0:
            self.mTheta_3 = 0
        elif self.mTheta_3 < -45:
            self.mTheta_3 = -45

    def evaluate(self):
        result_x, result_y = self.__sim_calc()
        self.mE = math.fabs(self.__mX - result_x) + math.fabs(self.__mY - result_y)

    def __sim_calc(self):
        x1 = 0
        y1 = LINE_1

        a1_theta = 180 - (180 - self.mTheta_1) - 90
        x2 = x1 + LINE_2 * math.cos(math.radians(a1_theta))
        y2 = y1 + LINE_2 * math.sin(math.radians(a1_theta))
        # print(f'x2:{x2}, y2:{y2}')

        a2_theta = 180 - self.mTheta_2 - a1_theta
        x3 = x2 + LINE_3 * math.cos(math.radians(a2_theta))
        y3 = y2 - LINE_3 * math.sin(math.radians(a2_theta))
        # print(f'x3:{x3}, y3:{y3}')

        # a3_theta = 180 - (180 - (180 - a2_theta - 90) - 90) - 90
        a3_theta = 180 - (180 - ((180 - a2_theta - 90) + self.mTheta_3) + 90)
        x4 = x3 - LINE_4 * math.cos(math.radians(a3_theta))
        y4 = y3 - LINE_4 * math.sin(math.radians(a3_theta))
        # print(f'x4:{x4}, y4:{y4}')

        # a4_theta = 180 - (180 - ((180 - a3_theta - 90) + self.mTheta_3) + 90)
        a4_theta = a3_theta - 90
        # print(f'a4_theta:{a4_theta}')
        x5 = x4 + LINE_5 * math.cos(math.radians(a4_theta))
        y5 = y4 + LINE_5 * math.sin(math.radians(a4_theta))
        # print(f'x5:{x5}, y5:{y5}')
        return x5, y5


def calc_theta(x):
    N = 300
    obj_list = []
    for i in range(N):
        obj_list.append(ArmSim(x, 0))

    best = {
        'EvaluationValue': 99999,
        'Theta_1': 0,
        'Theta_2': 0,
        'Theta_3': 0
    }
    for i in range(1000):
        # print(f'{i + 1}回目')

        # 評価
        # ソート
        for obj in obj_list:
            obj.evaluate()
        obj_list = sorted(obj_list, key=lambda o: o.mE)

        # 一番良い値は保存
        if obj_list[0].mE < best['EvaluationValue']:
            best['EvaluationValue'] = obj_list[0].mE
            best['Theta_1'] = obj_list[0].mTheta_1
            best['Theta_2'] = obj_list[0].mTheta_2
            best['Theta_3'] = obj_list[0].mTheta_3

        # 上位20%は、そのまま
        # 中位A30%は、上位のパラメータをかけ合わせる
        # 中位B30%は、更新
        # 下位20%は、作り直し
        upper_row = (0, int((N*0.2)-1))
        middle_a_row = (int(upper_row[1]), int((N*0.3)-1))
        middle_b_row = (int(middle_a_row[1]), int((N * 0.6) - 1))
        lower_low = (int(middle_b_row[1]), N-1)

        # 中位a
        for index in range(middle_a_row[0], middle_a_row[1]):
            upper_index = random.randrange(upper_row[0], upper_row[1] + 1)
            theta_index = random.randrange(1, 4)
            if theta_index == 1:
                obj_list[index].set_theta(theta_1=obj_list[upper_index].mTheta_1)
            elif theta_index == 2:
                obj_list[index].set_theta(theta_2=obj_list[upper_index].mTheta_2)
            else:
                obj_list[index].set_theta(theta_3=obj_list[upper_index].mTheta_3)

        # 中位b
        for index in range(middle_b_row[0], middle_b_row[1]):
            obj_list[index].update()

        # 下位
        for index in range(lower_low[0], lower_low[1]):
            obj_list[index].reset()

    print('-----------------------------')
    print('EvaluationValue:', best['EvaluationValue'])
    print('Theta_1:', best['Theta_1'])
    print('Theta_2:', best['Theta_2'])
    print('Theta_3:', best['Theta_3'])

    return best['Theta_1'], best['Theta_2'], best['Theta_3']
