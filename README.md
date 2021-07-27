# ArmRobot_RaspberryPi
## 概要
1. カメラによるサイコロの認識  
    「1~6の目 + サイコロ未配置状態」7分別
1. 認識結果から、偶数/奇数の分別をロボットアームにより実施

## 環境
- 環境  
Python 3.7  


- 実行コマンド  
    `python main.py`  

- 実行環境構築  
    - Python2 -> Python3.7  
        `$ cd /usr/bin`  
        `$ sudo unlink python`  
        `$ sudo ln -s python3 python`  
        
    - nnabla    
        `$ sudo pip install nnabla`  

    - numpyまわり  
        `$ sudo pip install -U numpy`  
        `$ sudo apt install libatlas-base-dev`  
        `$ sudo apt-get install libhdf5-serial-dev`  

    - fswebcam  
        `$ sudo apt-get install fswebcam`  

    - adafruit-pca9685(サーボ操作に利用)  
        `$ sudo pip install adafruit-pca9685`

    - opencvまわり  
        `$ sudo pip install opencv-contrib-python==4.1.0.25`  
        `$ sudo apt install libjasper1`  
        `$ sudo apt install libqtgui4`  
        `$ sudo apt install libqt4-test`  

## 利用機器
RaspberryPi 3 Model b+  
4K WEBカメラ(https://www.amazon.co.jp/dp/B08N649SS7)  
6軸アームロボット(https://www.amazon.co.jp/dp/B07M7TK6KR)