import logging
import time

import numpy as np
import serial


class SerialWeighingScale:
    _scale = None
    port = None
    baudrate = 57600
    timeout = 0.1
    write_timeout = 0.1

    message_to_tare = b"t"
    message_to_read = b"w"
    write_read_delay = 0.001

    def __init__(
        self,
        port="/dev/ttyACM0",
        baudrate=57600,
        timeout=0.1,
        write_timeout=0.1,
        auto_connect=True,
    ):
        super(SerialWeighingScale, self).__init__()
        self.port = port or self.port
        self.baudrate = baudrate or self.baudrate
        self.timeout = timeout or self.timeout
        self.write_timeout = write_timeout or self.write_timeout

        if auto_connect:
            self.connect()
            self.tare_scale()

    def connect(self):
        self._scale = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout,
            write_timeout=self.write_timeout,
        )

    def calibrate(self):
        pass  # TODO: do calibration via serial connection. Also add calibration.ino and scale.ino to Github later.
        # ! get calibration factor for .ino, but also get scaling factor !

    def make_test_curve(self, plot_per_reading=True, savepath=None):
        # self._scale

        # def do_plotting(
        #     weight_reference: list = None,
        #     weight_measured: list = None,
        #     savepath: str = None,
        # ):
        #     pass
        #
        # reading_idx = 0
        # weight_reference = []
        # weight_measured = []

        pass  # TODO: while loop with user input, then plot entered/measured values + write to file if savepath provided
        # while True:
        #   input: a=add datapoint, p=plot, e=end+plot
        #       if add:
        #           input: test weight float
        #           ready to weigh? Y or Enter
        #               -> Weigh + add both reference/measured to readings (only AFTER reading was a success)
        #       elif plot:
        #           do plotting (if savepath is not None: write to file)
        #
        # do final plotting: do plotting (if savepath is not None: write to file)

    def tare_scale(self):
        self._scale.write(self.message_to_tare)
        time.sleep(self.write_read_delay)

    def read_value(self):
        self._scale.write(self.message_to_read)
        time.sleep(self.write_read_delay)
        answer = self._scale.readline()
        # print("Raw answer:", answer)
        answer = answer.decode().split("\r")[0]

        try:
            answer = float(answer)
        except ValueError:
            logging.debug("Could not typecast reading:", answer)
            answer = None

        return answer

    def read_median(self, n_readings=5):
        readings = []
        for _ in range(n_readings):
            readings.append(self.read_value())

        return np.median(readings)
