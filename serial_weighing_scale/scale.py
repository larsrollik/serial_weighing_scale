import logging
import statistics
import time
from collections.abc import Callable

from serial_weighing_scale.connection import SerialConnection


class Scale(SerialConnection):
    _identity_response = "<SerialWeighingScale>"

    def __init__(self, serial_port: str, baudrate: int = 115200, timeout: float = 1) -> None:
        # init serial connection
        super().__init__(serial_port=serial_port, baudrate=baudrate, timeout=timeout)

    def start(self, timeout=10) -> None:
        """
        Start the scale.
        """
        # connect, then wait for identity response / is_ready
        self.connect()

        # wait for identity response
        start_time = time.time()
        while time.time() - start_time < timeout:
            # check if the scale is ready
            if self.is_ready and self.identify():
                logging.info(f"Scale is ready: {self.serial_port}")
                break

        else:
            raise TimeoutError(
                f"Timeout while waiting for identity response ({self._identity_response}) "
                f"from {self.serial_port}"
            )

    @property
    def is_ready(self) -> bool:
        """
        Check if the scale is ready.
        (Once reading weight returns float)
        """
        weight = self.read_weight()
        return weight is not None

    def read_weight(self) -> float | None:
        """
        Get the weight from the scale.
        """
        self.send(command="w", order="c")
        weight_result = self.read_line()

        # Convert to float
        try:
            weight = round(float(weight_result), 2)
            return weight
        except ValueError:
            logging.error(f"Failed to convert weight result to float: {weight_result}")
            return None

    def tare(self) -> None:
        """
        Tare the scale.
        """
        self.send(command="t", order="c")

    def identify(self) -> bool:
        """
        Identify the device connected to the serial port.
        This method sends a command to the device and waits for a response.
        """
        self.send(command="i", order="c")
        response = self.read_line()
        return response == self._identity_response

    def get_calibration_factor(self) -> float | None:
        """
        Get the calibration factor from the scale.
        """
        self.send(command="f", order="c")

        calibration_result = self.read_line()

        # Convert to float
        try:
            calibration_factor = float(calibration_result)
            return calibration_factor
        except ValueError:
            logging.error(f"Failed to convert calibration result to float: {calibration_result}")
            return None

    def read_weight_repeated(self, n_readings: int, inter_read_delay: float) -> list:
        """Reads the weight repeatedly, returns a list of readings."""
        readings = []
        for _ in range(n_readings):
            reading = self.read_weight()
            if reading is not None:
                readings.append(reading)
            time.sleep(inter_read_delay)
        return readings

    def read_weight_reliable(
        self,
        n_readings: int,
        inter_read_delay: float,
        measure: Callable = statistics.median,
    ) -> float:
        """
        Reads the weight reliably by taking repeated readings
        and applying the provided statistical measure.
        """
        readings = self.read_weight_repeated(
            n_readings=n_readings, inter_read_delay=inter_read_delay
        )
        return measure(readings)


if __name__ == "__main__":
    print("TEST")

    s = Scale(serial_port="/dev/ttyACM1", baudrate=115200, timeout=1)
    s.connect()
    s.read_weight()
