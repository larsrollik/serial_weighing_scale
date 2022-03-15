# Serial Weighing Scale
Arduino-based cheap precision weighing scale for readout via serial communication.

***

Precision weighing scales that include serial port communication usually come at considerable cost. This project showcases an affordable alternative.
Using readily available electronics parts, the scale's measurements can be read via serial communication by a simple Python class.

_Note:_ The design could easily be extended with an Arduino display to show the measurements.

### Bill of Materials
- Arduino Uno (including USB-A to USB-B cable)
- Load cell amplifier HX711 (Sparkfun), e.g. from mouser.co.uk: 474-SEN-13879
- Load cell (100g and 500g cells used), e.g. from mouser.co.uk: 474-SEN-14727 or 474-SEN-14728
- Jumper wires, pin headers, nylon spacers for electronics
- Acrylic or other material of choice for case and load cell mount

### Build
1. Load .ino onto Arduino
2. Assemble electronics, e.g. as described in this [HX711 wiring tutorial]
3. Move electronics into case
4. Calibrate scale with python class method `SerialScale.calibrate()`

### Usage
1. Connect scale via USB to machine that is going to read the measurements from the scale
2. Interact via python `SerialScale` object:

  ```python
  from serial_weighing_scale.serial_scale_object import SerialWeighingScale

serial_port = "/dev/ttyACM0"  # for Unix systems. "COM1" on Windows systems
scale = SerialWeighingScale(port=serial_port)

scale.tare()  # Tare scale
scale.read_value()  # Take single measurement
scale.read_median(n_readings=5)  # Get median of specified number of measurements

```

### TODO
- [ ] Add calibration routine to .ino & .py
- [ ] Add test curve to .py
- [ ] Add case and mount drawings for 3D printing

### Contributors
Code & electronics by Lars Rollik.
Case & load cell mount by Simon Townsend ([Advanced Manufacturing FabLabs], Sainsbury Wellcome Centre).
Thanks to Benjamin Hahl for useful input on the design.

[Advanced Manufacturing FabLabs]: https://www.sainsburywellcome.org/web/content/fablab
[HX711 wiring tutorial]: https://learn.sparkfun.com/tutorials/load-cell-amplifier-hx711-breakout-hookup-guide
