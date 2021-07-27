import time
import queue
import threading
THREAD_LOOP_TIME = 0.1

FINISH = 'FINISH'


class Manager(object):

    def __init__(self):
        self._mThread = threading.Thread(target=self.thread_main)
        self._mLock = threading.Lock()
        self._command_queue = queue.Queue()
        self._mIsOperating = False

    def __del__(self):
        pass

    def wait(self):
        while (not self._command_queue.empty()) or self._mIsOperating:
            # print('wait...')
            time.sleep(0.1)

    def executeCommand(self, cmd, params):
        # 仮想関数
        pass

    def thread_main(self):
        while True:
            time.sleep(THREAD_LOOP_TIME)

            if self._command_queue.empty():
                continue

            self._mIsOperating = True  # 動作中に移行
            self._mLock.acquire()  # セマフォ ロック
            cmd_params = self._command_queue.get()
            self._mLock.release()  # セマフォ 解放

            # コマンドを送信
            cmd = cmd_params[0]
            params = cmd_params[1]
            if cmd == FINISH:
                # 終了コマンドのみここで処理
                self._mIsOperating = False
                return

            self.executeCommand(cmd, params)
            self._mIsOperating = False

    def notifyCommand(self, cmd, params):
        self._mLock.acquire()  # セマフォ ロック
        self._command_queue.put([cmd, params])
        self._mLock.release()  # セマフォ 解放

    def start(self):
        self._mThread.start()
