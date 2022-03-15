from serial import SerialException

from serial_weighing_scale.serial_scale_object import SerialScale

__author__ = "Lars B. Rollik"
__version__ = "0.0.0.dev1"

TEST_PORTS = [f"/dev/ttyACM{x}" for x in range(5)]


def connect_serial_scale(test_ports: list = TEST_PORTS):
    """Connect to the serial scale. Returns scale object.

    :param test_ports: list of serial port addresses to test for connection
    :return: SerialScale object
    """
    serial_scale = None
    for port in test_ports:
        try:
            serial_scale = SerialScale(port=port)
            break
        except SerialException:
            pass

    return serial_scale
