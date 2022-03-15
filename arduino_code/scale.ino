/*
   Adapted example from HX711 library for SerialWeightScale. Lars Rollik, nov2021.
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
      LoadCell.tareNoDelay();

      if (LoadCell.getTareStatus() == true) {
        //  Serial.println("Tare complete");
      }
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


void calibrate() {
  /*
     TODO
  */
}
