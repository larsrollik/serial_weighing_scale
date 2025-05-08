__author__ = "Lars B. Rollik"

from importlib.metadata import PackageNotFoundError, version

from serial_weighing_scale.scale import Scale

try:
    __version__ = version("subject_weight_db")
except PackageNotFoundError:
    __version__ = "2.0.2"

DEFAULT_TEST_PORTS = [f"/dev/ttyACM{x}" for x in range(5)]

# make compatibility pseudonym SerialWeighingScale
SerialWeighingScale = Scale


def connect_serial_scale(
    serial_port_list: list = DEFAULT_TEST_PORTS,
) -> SerialWeighingScale | None:
    """
    Connect to the first available serial scale from the provided list of serial ports.
    Parameters
    ----------
    serial_port_list

    Returns
    -------

    """
    from serial import SerialException

    serial_scale = None
    for serial_port in serial_port_list:
        try:
            serial_scale = SerialWeighingScale(serial_port=serial_port)
            serial_scale.start()
            break
        except SerialException:
            pass

    return serial_scale


__all__ = ["Scale", "SerialWeighingScale", "connect_serial_scale", "__version__"]
