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

const float calibration_factor = -3050.0; // CHANGE THIS VALUE FROM CALIBRATION RESULT
const float scaling_factor = 1.0;

unsigned long stabilizing_time = 2000; // preciscion right after power-up can be improved by adding a few seconds of stabilizing time
boolean _tare = true; //set this to false if you don't want tare to be performed in the next step

void setup() {
  Serial.begin(57600); delay(10);

  LoadCell.begin();
  LoadCell.start(stabilizing_time, _tare);

  if (LoadCell.getTareTimeoutFlag()) {
    Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1);
  }
  else {
    LoadCell.setCalFactor(calibration_factor);
  }
}

void loop() {
  LoadCell.update();
  float i = LoadCell.getData() / scaling_factor;

  if (Serial.available() > 0) {
    char inByte = Serial.read();

    // Tare
    if (inByte == 't') {
      tare_scale();
      Serial.println("t");
    }

    // Read weight
    if (inByte == 'w') {
      Serial.println(i);
    }

    // Calibrate
    if (inByte == 'c') {
      calibrate();
    }

  } // serial
} // loop

void tare_scale() {
  LoadCell.update();
  LoadCell.tareNoDelay();
}

void calibrate() {
  LoadCell.setCalFactor(1.0);
  tare_scale();

  float known_mass = Serial.parseFloat();
  Serial.println(known_mass);  // confirm receipt

  boolean weight_added = false;
  while (weight_added == false) {
    char inByte = Serial.read();
    LoadCell.update();

    if (inByte == 'a') {
        LoadCell.refreshDataSet();
        float new_calibration_factor = LoadCell.getNewCalibration(known_mass);

        // return new calibration factor. Requires this typecasting with print to format correctly.
        Serial.print("");
        Serial.print(new_calibration_factor);
        Serial.println("");

        weight_added = true;
    }
  }
}
