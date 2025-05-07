import logging
import time

from serial_weighing_scale import SerialWeighingScale

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # scale = connect_serial_scale()
    scale = SerialWeighingScale(serial_port="/dev/ttyACM1", baudrate=115200, timeout=1)
    scale.connect()

    # measure time until scale is ready
    start_time = time.time()
    while not scale.is_ready:
        time.sleep(0.1)

    elapsed_time = time.time() - start_time

    print("Scale ready", elapsed_time)
    scale.read_weight()
    print("Scale:", scale.is_ready)
