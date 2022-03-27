import logging
import statistics
import time
from typing import Callable

import serial


class SerialWeighingScale:
    _scale = None
    port = None
    baudrate = 57600
    timeout = 0.1
    write_timeout = 0.1
    tare_on_connect = True

    message_to_read = b"w"
    message_to_tare = b"t"
    message_to_calibrate = b"c"
    write_read_delay = 0.001

    def __init__(
        self,
        port="/dev/ttyACM0",
        baudrate=57600,
        timeout=0.1,
        write_timeout=0.1,
        auto_connect=True,
        tare_on_connect=True,
    ):
        """

        :param port:
        :param baudrate:
        :param timeout:
        :param write_timeout:
        :param auto_connect:
        :param tare_on_connect:
        """
        super(SerialWeighingScale, self).__init__()
        self.port = port or self.port
        self.baudrate = baudrate or self.baudrate
        self.timeout = timeout or self.timeout
        self.write_timeout = write_timeout or self.write_timeout
        self.tare_on_connect = tare_on_connect or self.tare_on_connect

        if auto_connect:
            self.connect()

    def connect(self):
        """Connect via serial port"""
        self._scale = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout,
            write_timeout=self.write_timeout,
        )
        if self.tare_on_connect:
            self.tare_scale()

    def _send_command(self, command=None):
        if self._scale is None or command is None:
            print(
                f"Cannot write to scale -- self._scale: {self._scale}, command: {command}"
            )
            return None
        self._scale.write(command)
        time.sleep(self.write_read_delay)
        raw_answer = self._scale.readline()
        # print("Raw answer:", answer)
        decoded_answer = raw_answer.decode().split("\r")[0]
        return decoded_answer

    def tare_scale(self):
        """Tare scale"""
        return self._send_command(command=self.message_to_tare) == self.message_to_tare

    def read_weight(self):
        """Read single value"""
        answer = self._send_command(command=self.message_to_read)
        try:
            answer = float(answer)
        except ValueError:
            logging.debug("Could not typecast reading:", answer)
            answer = None

        return answer

    def read_weight_repeated(
        self, n_readings: int = 5, delay_between_readings: float = 0.05
    ):
        """Read repeatedly."""
        readings = []
        for _ in range(n_readings):
            readings.append(self.read_weight())
            time.sleep(delay_between_readings)

        return readings

    def read_weight_reliable(
        self,
        n_readings: int = 5,
        delay_between_readings: float = 0.05,
        measure: Callable = statistics.median,
    ):
        """Read repeatedly, then use `measure` to get measure of central tendency

        :param n_readings:
        :param delay_between_readings:
        :param measure: `mean` or `median` or function
        :return:
        """
        assert isinstance(measure, Callable)
        readings = self.read_weight_repeated(
            n_readings=n_readings, delay_between_readings=delay_between_readings
        )
        return measure(readings)

    def calibrate(self, known_mass=None):
        """"""
        # Expect confirmation that calibration begun
        assert (
            self._send_command(command=self.message_to_calibrate)
            == self.message_to_calibrate
        )
        # Send known mass and expect confirmation of receipt
        known_mass_b = str(known_mass).encode()
        assert self._send_command(command=known_mass_b) == known_mass_b

        x = input("Add known mass now to scale. Confirm with Enter.")
        print(x)  # todo: if x is Enter, then proceed ?
        new_calibration_value = self._send_command(b"a")
        print("New calibration value:", new_calibration_value)

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
