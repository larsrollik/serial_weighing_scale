/*
   Adapted example from HX711 library for `serial_weighing_scale`. Lars Rollik, nov2021.
   github.com/larsrollik/serial_weighing_scale
   -------------------------------------------------------------------------------------
   HX711_ADC
   Arduino library for HX711 24-Bit Analog-to-Digital Converter for Weight Scales
   Olav Kallhovd sept2017
   -------------------------------------------------------------------------------------
*/

#include <HX711_ADC.h>

const int HX711_dout = 2; // DATA
const int HX711_sck  = 3; // CLOCK

HX711_ADC LoadCell(HX711_dout, HX711_sck);

const float calibrationValue = -591.67; // calibration value (see example file "Calibration.ino")
const float scalingFactor = 5.28;

unsigned long stabilizingtime = 2000; // preciscion right after power-up can be improved by adding a few seconds of stabilizing time
boolean _tare = true; //set this to false if you don't want tare to be performed in the next step

void setup() {
  Serial.begin(57600); delay(10);

  LoadCell.begin();
  LoadCell.start(stabilizingtime, _tare);

  if (LoadCell.getTareTimeoutFlag()) {
    Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1);
  }
  else {
    LoadCell.setCalFactor(calibrationValue);
  }
}

void loop() {
  LoadCell.update();
  float i = LoadCell.getData() / scalingFactor;

  if (Serial.available() > 0) {
    char inByte = Serial.read();

    // Tare
    if (inByte == 't') {
      tare_scale();
    }

    // Calibrate
    if (inByte == 'c') {
      calibrate();
    }

    // Read weight
    if (inByte == 'w') {
      Serial.println(i);
    }

  } // serial
} // loop

void tare_scale() {
    LoadCell.tareNoDelay();

    if (LoadCell.getTareStatus() == true) {
      Serial.println("t");
    }
    else {
      Serial.println("n");  // tare did not work
    }
}

void calibrate() {
  /*
    Receives calibration command
    Receives float of known_mass
    Confirms by sending known_mass back

    Wait for "a" (known calibration mass "A"dded to scale)
    Then: get new calibration value -> Send back
  */
  Serial.println("c");
  float known_mass = Serial.read();
  tare_scale();
  Serial.println(known_mass);  // confirm receipt
  LoadCell.setCalFactor(1.0);

  boolean weight_added = false;
  while (weight_added == false) {
    char inByte = Serial.read();

    if (inByte == 'a') {
        LoadCell.update();
        LoadCell.refreshDataSet();
        float new_calibration_value = LoadCell.getNewCalibration(known_mass);
        Serial.println(new_calibration_value);
        weight_added = true;
    }
  }
}
