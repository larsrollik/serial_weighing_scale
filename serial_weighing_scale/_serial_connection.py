import time
from typing import Any
from typing import Union

from serial import Serial


class SerialConnection:
    serial_port: Union[str, None] = None
    baudrate: Union[int, None] = None
    timeout: float = 1
    connection: Union[Serial, None] = None

    def __init__(
        self,
        serial_port: Union[str, None] = None,
        baudrate: Union[int, None] = None,
        timeout: Union[float, None] = None,
        **kwargs: Any,
    ) -> None:
        self.serial_port = serial_port
        self.baudrate = baudrate or 115200
        self.timeout = timeout or 0.1

    def dict(self) -> dict[str, Union[str, int, float]]:
        return {
            "serial_port": self.serial_port,
            "baudrate": self.baudrate,
            "timeout": self.timeout,
        }

    @property
    def connected(self) -> bool:
        if self.connection is not None:
            return self.connection.is_open
        else:
            return False

    def connect(self) -> "SerialConnection":
        if not self.connected:
            self.connection = Serial(
                port=self.serial_port,
                baudrate=self.baudrate,
                timeout=self.timeout,
            )
        return self

    def disconnect(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    # def clear_buffer(self):
    #     """
    #     Clears the input and output buffers of the serial connection.
    #     """
    #     if self.connected:
    #         self.connection.reset_input_buffer()
    #         self.connection.reset_output_buffer()

    def clear_buffer(self) -> None:
        """
        Read and discard data until there's nothing left in the buffer
        """
        while self.connection.in_waiting > 0:
            self.connection.read(self.connection.in_waiting)

    def send(self, data):
        """
        Sends a line of data to the serial port.

        :param data: Data to be sent, should be a string or bytes
        """
        if isinstance(data, str):
            data = data.encode()  # Convert string to bytes if needed

        self.clear_buffer()
        self.connection.write(data)
        self.connection.flush()

    def read(self, n: int):
        """
        Reads n bytes from the serial port.

        :param n: Number of bytes to read
        :return: The bytes read from the serial port
        """
        # Read until n bytes are received or timeout occurs
        response = self.connection.read(n)
        return response

    def readline(self):
        """
        Reads a line of response from the serial port.

        :return: The line of data received from the serial port
        """
        # Read until a newline character is encountered or timeout occurs
        response = (
            self.connection.readline().decode().rstrip()
        )  # Decode bytes to string and strip newline
        return response

    def read_all_lines(self) -> str:
        """Reads all lines and returns only the last line."""
        lines = []
        while (
            self.connection.in_waiting > 0
        ):  # Check if there are any lines available in the buffer
            line = self.readline()  # Read line, decode and strip newline characters
            lines.append(line)
        # Return only the last line, or empty string if no lines
        return lines[-1] if lines else ""

    def send_and_read(self, data, delay: float = 0.05, n: int = 1):
        """
        Sends a line of data to the serial port and reads the response.

        :param data: Data to be sent, should be a string or bytes
        :return: The line of data received from the serial port
        """
        self.send(data)
        time.sleep(delay)

        return self.read(n)

    def send_and_readline(self, data, delay: float = 0.05):
        """
        Sends a line of data to the serial port and reads the response.

        :param data: Data to be sent, should be a string or bytes
        :return: The line of data received from the serial port
        """
        self.send(data)
        time.sleep(delay)

        return self.read_all_lines()
