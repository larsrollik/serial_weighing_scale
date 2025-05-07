# Serial Weighing Scale
Arduino-based cheap precision weighing scale for readout via serial communication.

***
Version: "2.0.1"

Precision weighing scales that include serial port communication usually come at considerable cost. This project showcases an affordable alternative.
Using readily available electronics parts, the scale's measurements can be read via serial communication by a simple Python class.


_Note:_ The design could easily be extended with an Arduino display to show the measurements.


### Bill of Materials
- Arduino Uno (including USB-A to USB-B cable)
- Load cell amplifier HX711 (Sparkfun), e.g. from mouser.co.uk: 474-SEN-13879
- Load cell (100g and 500g cells used), e.g. from mouser.co.uk: 474-SEN-14727 or 474-SEN-14728
- Jumper wires, pin headers, nylon spacers for electronics
- Acrylic or other material of choice for case and load cell mount
- HX711 arduino library from [olkal/HX711_ADC](https://github.com/olkal/HX711_ADC)


### Build
1. Load .ino onto Arduino (via Arduino IDE or commandline like `arduino --board arduino:avr:uno --port /dev/ttyACM0 --upload serial_scale.ino`)
2. Assemble electronics, e.g. as described in this [HX711 wiring tutorial]
3. Print 3D components from [drawings](./drawings_for_3D_printing) (Drawings named `model` are only for design, no need to print these)
4. Move electronics into case
5. Calibrate scale via Arduino IDE serial monitor commands. See below for communication protocol for calibration.


### Usage
1. Connect scale via USB to machine that is going to read the measurements from the scale
2. Interact via python `SerialScale` object:


##### Open connection with `SerialWeighingScale` object & perform standard operations on it
```python
import numpy as np
import time

from serial_weighing_scale import SerialWeighingScale

serial_port = "/dev/ttyACM0"  # for Unix systems. "COM1" on Windows systems
scale = SerialWeighingScale(port=serial_port)

while not scale.scale_is_ready():
    time.sleep(.1)

# Perform standard operations
scale.tare_scale()  # Tare scale
scale.read_weight()  # Take single measurement
scale.read_weight_repeated(n_readings=5)  # Get n readings
scale.read_weight_reliable(n_readings=5, measure=np.mean)  # Get statistic of n readings

```

##### Open connection by testing specific serial ports sequentially
```python
import time

from serial_weighing_scale import connect_serial_scale

scale = connect_serial_scale(test_ports=["/dev/ttyACM0", "/dev/ttyACM1"])
while not scale.scale_is_ready():
    time.sleep(.1)

```

##### Not yet implemented: Calibrate scale via python
```python
import time

from serial_weighing_scale import connect_serial_scale

scale = connect_serial_scale(test_ports=["/dev/ttyACM0", "/dev/ttyACM1"])
while not scale.scale_is_ready():
    time.sleep(.1)

known_mass = 45.05  # weight [gram] of object used for claibration
scale.calibrate(known_mass=known_mass)
```


### Communication protocol for messages between python and Arduino

- Tare scale: send "t" -> Tare scale & Arduino confirms with "t"
- Read scale: send "w" -> Arduino returns latest reading
- Calibrate scale: send "c" + weight of known mass
  - Arduino confirms by sending known mass value back
  - Send "a" once known mass was placed on scale -> Arduino performs calibration & returns new calibration factor that needs to be added to `serial_scale.ino`


### TODO
- [ ] Add calibration routine to .ino & .py
- [ ] Add test curve to .py


## NOTES
- calibration for first scale with 28.22g weight: -3150
- calibration for second scale with 45.05g weight: -2894

### Contributors
Code & electronics by Lars Rollik.
Scale 3D printing drawings by Simon Townsend ([Advanced Manufacturing FabLabs], Sainsbury Wellcome Centre).
Thanks to Benjamin Hahl for useful input on the design.

[Advanced Manufacturing FabLabs]: https://www.sainsburywellcome.org/web/content/fablab
[HX711 wiring tutorial]: https://learn.sparkfun.com/tutorials/load-cell-amplifier-hx711-breakout-hookup-guide
