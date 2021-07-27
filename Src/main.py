import logging
import Sequence

from Camera.Object import Camera
from SwitchBox.Manager import SwitchBoxManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(process)d %(levelname)s [ROBOT] %(message)s [%(funcName)s][%(pathname)s]'
)

camera = Camera()
switchBox = SwitchBoxManager()

seq = Sequence.Sequence()
seq.initialize()

while True:
    try:

        switchBox.waitSwitch()  # スイッチが押下されるまで無限待ち

        switchBox.clearLed()

        seq.shoot_pos()

        index = camera.execute()
        logging.info(f'recog index: {index}')
        if index == 0:
            switchBox.setErrorPut(kind=0)
            continue

        switchBox.setDiceEyes(index)

        seq.grab()

        seq.lift()

        if(index % 2) == 0:
            kind = 'EVEN'
        else:
            kind = 'ODD'
        seq.put(kind)

        seq.initialize()

    except KeyboardInterrupt:
        break

del seq

logging.info("finish")
