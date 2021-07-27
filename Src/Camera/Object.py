from PIL import Image
import logging
import subprocess
import cv2

# from picamera import PiCamera
import numpy as np
import time

import nnabla as nn
import nnabla.functions as F
import nnabla.parametric_functions as PF

PATH = './tmp.jpg'
PATH_POS = './pos_tmp.jpg'
NNP_PATH = 'Camera/results.nnp'

OBJECT_THRESHOLD = 500


def _cv2pil(image):
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = new_image[:, :, ::-1]
    elif new_image.shape[2] == 4:  # 透過
        new_image = new_image[:, :, [2, 1, 0, 3]]
    new_image = Image.fromarray(new_image)
    return new_image


def _recognize(im):
    # データ生成
    x = []
    y = []
    x.append(np.array(im))
    xt = np.array(x)

    def network(x, test=False):
        # Input:x -> 1,50,50
        # Affine_2 -> 250
        h = PF.affine(x, (250,), name='Affine_2')
        # ReLU
        h = F.relu(h, True)
        # Dropout
        if not test:
            h = F.dropout(h)

        # Affine -> 7
        h = PF.affine(h, (7,), name='Affine')
        # Softmax
        h = F.softmax(h)
        # CategoricalCrossEntropy -> 1
        # h = F.categorical_cross_entropy(h, y)
        return h

    # Prepare input variable
    x = nn.Variable((1, 1, 50, 50))

    # Let input data to x.d
    x.d = np.array(im)
    # x.data.zero()

    # Build network for inference
    y = network(x, test=True)

    # Execute inference
    y.forward()
    logging.info(f'recog result: {y.d}')
    return y.d


class Camera:
    _mObject = None

    def __init__(self):
        nn.load_parameters(NNP_PATH)

    def __del__(self):
        pass

    def execute(self):
        # 写真の撮影
        subprocess.call(['fswebcam', '-r', '1920x1080', '-S', '20', '-F', '2', '-d', 'v4l2:/dev/video0', '-i', '0',
                         '-p', 'YUYV', PATH_POS])
        time.sleep(2)  # 写真の保存待ち

        # 撮影された写真から、マーカー位置を検出
        aruco = cv2.aruco
        p_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        img = cv2.imread(PATH_POS)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(img, p_dict)  # 検出

        m = np.empty((4, 2))
        if (ids is None) or len(ids) != 4:
            # マーカーが見つからない場合、暫定座標とする
            logging.warning(f'ids is Error: {ids}')
            m[0] = [767.25, 626.75]
            m[1] = [794.5, 270.75]
            m[2] = [1146.25, 288.5]
            m[3] = [1141, 634.5]
        else:
            try:
                for i, c in zip(ids.ravel(), corners):
                    m[i] = c[0].mean(axis=0)
            except:
                logging.warning(f'm[i] = c[0].mean(axis=0) Error')
                return 0

        # マーカー位置をもとにトリミング
        width, height = (500, 500)  # 変形後画像サイズ
        marker_coordinates = np.float32(m)
        true_coordinates = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
        trans_mat = cv2.getPerspectiveTransform(marker_coordinates, true_coordinates)
        img_trans = cv2.warpPerspective(img, trans_mat, (width, height))

        # 座標を求める
        # (1) グレースケール変換
        # (2) ぼかし処理
        # (3) 二値化処理
        img_trans = cv2.rotate(img_trans, cv2.ROTATE_90_CLOCKWISE)
        tmp = img_trans.copy()
        tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
        tmp = cv2.GaussianBlur(tmp, (11, 11), 0)
        th = 190  # 二値化の閾値(要調整）
        _, tmp = cv2.threshold(tmp, th, 255, cv2.THRESH_BINARY)

        # (4) ブロブ（＝塊）検出
        # (5) 検出結果の整理
        n, img_label, data, center = cv2.connectedComponentsWithStats(tmp)
        detected_obj = list()
        tr_x = lambda x: x * 100 / 600  # X軸 画像座標→実座標
        tr_y = lambda y: y * 120 / 500  # Y軸 　〃
        img_trans_marked = img_trans.copy()

        # 最大ブロブを取得
        max_size = 0
        max_index = 1
        for i in range(1, n):
            _, _, _, _, size = data[i]
            if size >= max_size:
                max_index = i
                max_size = size

        if max_size < OBJECT_THRESHOLD:
            logging.warning(f'object None{max_size}')
            return 0  # 閾値のモノがない場合は、サイコロはないと判断

        x, y, w, h, size = data[max_index]
        detected_obj.append(dict(x=tr_x(x),
                                 y=tr_y(y),
                                 w=tr_x(w),
                                 h=tr_y(h),
                                 cx=tr_x(center[max_index][0]),
                                 cy=tr_y(center[max_index][1])))

        img_trans_marked = img_trans_marked[y: y + h, x: x + w]
        try:
            im_crop = _cv2pil(img_trans_marked)
        except:
            logging.warning(f'!!!!!!!!! "im_crop = cv2pil(img_trans_marked)" ERROR!!')
            return 0

        im_crop = im_crop.convert('L')
        im_crop = im_crop.resize((50, 50))
        recog_index = _recognize(im_crop)
        index = np.argmax(recog_index)
        return index

    '''
    def execute_position(self):
        # 写真の撮影
        subprocess.call(['fswebcam', '-r', '1920x1080', '-S', '10', '-F', '5', '-d', 'v4l2:/dev/video0', '-i', '0',
                         '-p', 'YUYV', PATH_POS])

        time.sleep(2)  # 写真の保存待ち

        # 撮影された写真から、マーカー位置を検出
        aruco = cv2.aruco
        p_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        img = cv2.imread(PATH_POS)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(img, p_dict)  # 検出
        # img_marked = aruco.drawDetectedMarkers(img.copy(), corners, ids)  # 検出結果をオーバーレイ
        m = np.empty((4, 2))
        try:  # 後で調査
            for i, c in zip(ids.ravel(), corners):
                m[i] = c[0].mean(axis=0)
        except:
            return False, (0, 0)

        # マーカー位置をもとにトリミング
        width, height = (600, 500)  # 変形後画像サイズ
        marker_coordinates = np.float32(m)
        true_coordinates = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
        trans_mat = cv2.getPerspectiveTransform(marker_coordinates, true_coordinates)
        img_trans = cv2.warpPerspective(img, trans_mat, (width, height))
        cv2.imwrite(f'result.png', img_trans)

        # 座標を求める
        img_trans = cv2.rotate(img_trans, cv2.ROTATE_90_CLOCKWISE)
        tmp = img_trans.copy()

        # (1) グレースケール変換
        tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)

        # (2) ぼかし処理
        tmp = cv2.GaussianBlur(tmp, (11, 11), 0)

        # (3) 二値化処理
        th = 180  # 二値化の閾値(要調整）
        _, tmp = cv2.threshold(tmp, th, 255, cv2.THRESH_BINARY)
        cv2.imwrite(f'result2.png', tmp)

        # (4) ブロブ（＝塊）検出
        n, img_label, data, center = cv2.connectedComponentsWithStats(tmp)

        # (5) 検出結果の整理
        detected_obj = list()  # 検出結果の格納先
        tr_x = lambda x: x * 100 / 600  # X軸 画像座標→実座標
        tr_y = lambda y: y * 120 / 500  # Y軸 　〃
        img_trans_marked = img_trans.copy()
        for i in range(1, n):
            x, y, w, h, size = data[i]
            print(size)
            if size < OBJECT_THRESHOLD:  # 閾値未満の面積は無視
                continue

            detected_obj.append(dict(x=tr_x(x),
                                     y=tr_y(y),
                                     w=tr_x(w),
                                     h=tr_y(h),
                                     cx=tr_x(center[i][0]),
                                     cy=tr_y(center[i][1])))
            # 確認
            cv2.rectangle(img_trans_marked, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(img_trans_marked, (int(center[i][0]), int(center[i][1])), 5, (0, 0, 255), -1)

        # (6) 結果の表示
        cv2.imwrite(f'result3.png', img_trans_marked)

        if len(detected_obj) == 0:
            return False, (0, 0)

        return True, (detected_obj[0]["cx"], detected_obj[0]["cy"])
    '''
