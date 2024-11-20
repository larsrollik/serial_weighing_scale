import logging
import statistics
import time
from typing import Any
from typing import Callable
from typing import Union

from serial_weighing_scale._serial_connection import SerialConnection

DEFAULT_SERIAL_PORT = "/dev/ttyACM0"
DEFAULT_BAUD_RATE = 115200
DEFAULT_TIMEOUT = 0.2
# DEFAULT_WRITE_TIMEOUT = 0.1
DEFAULT_TARE_ON_CONNECT = True
DEFAULT_AUTO_CONNECT = True

# Default CMD commands
DEFAULT_CMD_TO_READ = "w"
DEFAULT_CMD_TO_TARE = "t"
DEFAULT_CMD_TO_CALIBRATE = "c"
DEFAULT_WRITE_READ_DELAY = 0.5

N_READINGS = 5


class SerialWeighingScale:
    _scale = None
    serial_port = None
    baudrate = DEFAULT_BAUD_RATE
    timeout = DEFAULT_TIMEOUT
    # write_timeout = DEFAULT_WRITE_TIMEOUT
    tare_on_connect = DEFAULT_TARE_ON_CONNECT
    auto_connect = DEFAULT_AUTO_CONNECT

    message_to_read = DEFAULT_CMD_TO_READ
    message_to_tare = DEFAULT_CMD_TO_TARE
    message_to_calibrate = DEFAULT_CMD_TO_CALIBRATE
    write_read_delay = DEFAULT_WRITE_READ_DELAY

    def __init__(
        self,
        serial_port: Union[str, None] = None,
        baudrate: Union[int, None] = None,
        timeout: Union[float, None] = None,
        tare_on_connect: bool = DEFAULT_TARE_ON_CONNECT,
        auto_connect: bool = DEFAULT_AUTO_CONNECT,
        **kwargs: Any,
    ):
        self.serial_port = serial_port or DEFAULT_SERIAL_PORT
        self.baudrate = baudrate or DEFAULT_BAUD_RATE
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.tare_on_connect = tare_on_connect
        self.auto_connect = auto_connect
        self._scale = None

        if self.auto_connect:
            self.connect()

    @property
    def connected(self):
        """Returns whether the scale is connected."""
        return self._scale is not None and self._scale.ser.is_open

    @connected.setter
    def connected(self, value: bool):
        """Setter to connect or disconnect the scale."""
        if value:
            self.connect()
        else:
            self._scale.close()
            self._scale = None

    def connect(self):
        """Connects to the scale."""
        if self._scale is None:
            logging.debug(
                f"Connecting to {self.serial_port} with rate {self.baudrate} / timeout {self.timeout}"
            )
            self._scale = SerialConnection(
                serial_port=self.serial_port,
                baudrate=self.baudrate,
                timeout=self.timeout,
            )
            self._scale.connect()

            if self.tare_on_connect:
                self.tare()
        return self

    def scale_is_ready(self) -> bool:
        """Returns whether the scale is ready by checking if weight is read successfully."""
        return self.read_weight() is not None

    def tare(self):
        """Sends a tare command to the scale."""
        if self._scale:
            self._scale.send("t")
            print("Tare command sent.")

            # # Wait for the response for up to 5 seconds
            # start_time = time.time()
            # while time.time() - start_time < 5:
            #     response = self._scale.readline()
            #     if response == "t":
            #         print("Tare command confirmed.")
            #         break
            # else:
            #     # If the loop completes without finding the expected response
            #     print("Error: Tare command not confirmed within 5 seconds.")
        else:
            raise ValueError("Scale is not connected")

    def read_weight(self) -> float:
        """Reads the weight from the scale."""
        if self._scale:
            response = self._scale.send_and_readline(
                data=DEFAULT_CMD_TO_READ, delay=self.write_read_delay
            )

            try:
                return round(float(response), 3)
            except ValueError:
                print(f"Failed to convert '{response}' to float.")
                return
        else:
            raise ValueError("Scale is not connected")

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
        """Reads the weight reliably by taking repeated readings and applying the provided statistical measure."""
        readings = self.read_weight_repeated(n_readings, inter_read_delay)
        return measure(readings)

    def calibrate(self, known_mass: float):
        """Calibrate the scale with a known mass."""
        if self._scale:
            self._scale.send("c")
            self._scale.send(known_mass)
            print(f"Calibration command sent for known mass: {known_mass}")
            # Wait for the user to place the known mass on the scale
            input("Place the known mass on the scale and press Enter when ready...")

            # After mass is placed, confirm and send 'a' to complete the calibration
            self._scale.write_message("a")
            calibration_result = self._scale.read_response()
            print(f"Calibration result: {calibration_result}")
        else:
            raise ValueError("Scale is not connected")


if __name__ == "__main__":
    s = SerialWeighingScale(serial_port="/dev/ttyACM1", timeout=1)
    s.connect()
    s.scale_is_ready()

    print(" ")
