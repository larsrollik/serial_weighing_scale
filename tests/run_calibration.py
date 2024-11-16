import time

from serial_weighing_scale import connect_serial_scale


def wait():
    time.sleep(0.1)


port = "/dev/tty.usbmodem14201"
scale = connect_serial_scale(test_ports=[port])
while not scale.scale_is_ready():
    wait()


def do_run():
    known_mass = 59.52  # for ThorLabs BA1L/M bar
    port = "/dev/tty.usbmodem14201"
    scale = connect_serial_scale(test_ports=[port])
    while not scale.scale_is_ready():
        wait()

    print("calibrate")
    return_value = scale.calibrate(known_mass=known_mass)
    print(return_value)
    wait()

    print(scale)


if __name__ == "__main__":
    do_run()
