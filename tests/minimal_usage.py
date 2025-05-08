import logging

from serial_weighing_scale import SerialWeighingScale

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    serial_param = {
        "serial_port": "/dev/ttyACM0",
        "baudrate": 115200,
        "timeout": 1,
    }

    # scale = connect_serial_scale()
    scale = SerialWeighingScale(**serial_param)
    scale.start()

    # # measure time until scale is ready
    # start_time = time.time()
    # while not scale.is_ready:
    #     time.sleep(0.1)
    #
    # elapsed_time = time.time() - start_time
    #
    # print("Scale ready", elapsed_time)
    # scale.read_weight()
    # scale.tare()
    #
    # # query every .25 seconds and print the weight, continue until interrupted
    # try:
    #     while True:
    #         weight = scale.read_weight()
    #         print("Weight:", weight)
    #         time.sleep(0.25)
    # except KeyboardInterrupt:
    #     pass
    print("")
    print("NEXT")
    print("")

    scale = SerialWeighingScale(**serial_param)
    scale.start()
    scale.identify()
    scale.read_weight()

    print("Scale:", scale.is_ready)
