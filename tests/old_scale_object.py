#
# class SerialWeighingScale:
#
#
# class OLDSerialWeighingScale:
#     _scale = None
#     port = None
#     baudrate = DEFAULT_SERIAL_PORT
#     timeout = DEFAULT_TIMEOUT
#     write_timeout = DEFAULT_TIMEOUT
#     tare_on_connect = DEFAULT_TARE_ON_CONNECT
#     auto_connect = DEFAULT_BAUD_RATE
#
#     CMD_to_read = b"w"
#     CMD_to_tare = b"t"
#     CMD_to_calibrate = b"c"
#     write_read_delay = 0.01
#
#     def __init__(
#         self,
#         port=DEFAULT_SERIAL_PORT,
#         baudrate=DEFAULT_BAUD_RATE,
#         timeout=DEFAULT_TIMEOUT,
#         write_timeout=DEFAULT_TIMEOUT,
#         auto_connect=DEFAULT_AUTO_CONNECT,
#         tare_on_connect=DEFAULT_TARE_ON_CONNECT,
#     ):
#         """
#
#         """
#         super(SerialWeighingScale, self).__init__()
#         self.port = port or self.port
#         self.baudrate = baudrate or self.baudrate
#         self.timeout = timeout or self.timeout
#         self.write_timeout = write_timeout or self.write_timeout
#         self.tare_on_connect = tare_on_connect or self.tare_on_connect
#
#         if auto_connect:
#             self.connect()
#
#     @property
#     def connected(self):
#         if self._scale is None:
#             return False
#         else:
#             return self._scale.is_open
#
#     @connected.setter
#     def connected(self, value):
#         if value is not None and not value and self._scale is not None:
#             self._scale.close()
#
#     def connect(self):
#         """Connect via serial port"""
#         self._scale = serial.Serial(
#             port=self.port,
#             baudrate=self.baudrate,
#             timeout=self.timeout,
#             write_timeout=self.write_timeout,
#         )
#
#         # make sure this is a scale
#         retry = 10
#         for this_try in range(retry):
#             logging.debug(f"Trying to read first weight. Retry #{this_try}")
#             if self.scale_is_ready():
#                 break
#             time.sleep(0.01)
#
#         if self.tare_on_connect:
#             self.tare_scale()
#
#         return self
#
#     def _clear_read_queue(self):
#         queue = self._scale.readlines()
#         # print("queue", queue)
#         return queue
#
#     def scale_is_ready(self):
#         return self.read_weight() is not None
#
#     def _decode_answer(self, raw_answer=None):
#         # print("Raw answer:", raw_answer)
#         decoded_answer = raw_answer.decode().split("\r")[0]
#         return decoded_answer
#
#     def _send_command(self, command=None):
#         self._clear_read_queue()
#         if self._scale is None or command is None:
#             print(
#                 f"Cannot write to scale -- self._scale: {self._scale}, command: {command}"
#             )
#             return None
#         self._scale.write(command)
#         time.sleep(self.write_read_delay)
#         decoded_answer = self._decode_answer(raw_answer=self._scale.readline())
#         return decoded_answer
#
#     def tare_scale(self):
#         """Tare scale"""
#         return (
#             self._send_command(command=self.CMD_to_tare) == self.CMD_to_tare
#         )  # fixme: does not return true
#
#     def read_weight(self):
#         """Read single value"""
#         command = struct.pack('!c', "w".encode())
#         answer = self._send_command(command=command)  # self.CMD_to_read)
#         try:
#             answer = float(answer)
#         except ValueError:
#             logging.debug(f"Could not typecast reading: {answer}")
#             answer = None
#
#         return answer
#
#     def read_weight_repeated(
#         self,
#         n_readings: int = N_READINGS,
#         delay_between_readings: float = DELAY_BETWEEN_READINGS,
#     ):
#         """Read repeatedly."""
#         readings = []
#         for _ in range(n_readings):
#             new_reading = self.read_weight()
#             if new_reading is not None:
#                 readings.append(new_reading)
#             time.sleep(delay_between_readings)
#
#         return readings
#
#     def read_weight_reliable(
#         self,
#         n_readings: int = N_READINGS,
#         delay_between_readings: float = DELAY_BETWEEN_READINGS,
#         measure: Callable = statistics.median,
#     ):
#         """Read repeatedly, then use `measure` to get measure of central tendency
#
#         :param n_readings:
#         :param delay_between_readings:
#         :param measure: `mean` or `median` or function
#         :return:
#         """
#         assert isinstance(measure, Callable)
#         readings = self.read_weight_repeated(
#             n_readings=n_readings, delay_between_readings=delay_between_readings
#         )
#         if len(readings) < 1:
#             print("No valid readings", readings)
#             return None
#
#         return measure(readings)
#
#     def calibrate(self, known_mass=None):
#         """Calibrate scale with known mass.
#
#         :param known_mass: known mass of any object that can be placed on scale for calibration
#         :return: calibration value that has to be entered in `serial_scale.ino`
#         """
#         # - known_mass_encoded = str(known_mass).encode()
#         # - initialize: cmd = self.CMD_to_calibrate + known_mass_encoded
#         # - add weight delay, then send: new_calibration_value = self._send_command(b"a")
#         # - clear serial queue in between with: self._clear_read_queue()
#         raise NotImplementedError(
#             f"Use `known_mass={known_mass}` with Arduino IDE serial monitor to calibrate. "
#             f"See README for commands."
#         )
