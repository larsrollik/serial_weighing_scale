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

// DEFINITIONS
#define CMD Serial
#define HX711_DOUT 2              // DATA
#define HX711_SCK 3               // CLOCK
#define SAMPLES_IN_USE 1          // number of samples to average for measurement, less will cause more noise but faster response
#define CALIBRATION_FACTOR -3150  // CHANGE THIS VALUE FROM CALIBRATION RESULT
#define SCALING_FACTOR 1.0
#define STABILIZING_TIME 2000  // precision right after power-up can be improved by adding a few seconds of stabilizing time
#define PERFORM_TARE true      // set to false if you don't want tare to be performed in the next step
#define DEBUG_PRINT false


// INSTANCE of LoadCell object
HX711_ADC LoadCell(HX711_DOUT, HX711_SCK);


void setup() {
  LoadCell.begin();
  LoadCell.start(STABILIZING_TIME, PERFORM_TARE);
  LoadCell.setSamplesInUse(SAMPLES_IN_USE);

  CMD.begin(115200);
  while (!CMD)
    ;

  if (LoadCell.getTareTimeoutFlag()) {
    CMD.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1)
      ;
  } else {
    LoadCell.setCalFactor(CALIBRATION_FACTOR);

    if (DEBUG_PRINT)
      CMD.println("READY");
  }
}

void loop() {
  //   LoadCell.refreshDataSet();
  //   LoadCell.update();
  //   float i = LoadCell.getData() / SCALING_FACTOR;

  if (CMD.available()) {
    char cmdChar = CMD.read();

    if (DEBUG_PRINT) {
      CMD.println("cmd: " + String(cmdChar));  // Print cmdChar for debugging
    }

    if (cmdChar == 'w') {
      unsigned long startTime = millis();

      LoadCell.refreshDataSet();
      LoadCell.update();
      float i = LoadCell.getData() / SCALING_FACTOR;
      CMD.println(i);

      if (DEBUG_PRINT) {
        unsigned long endTime = millis();  // Record the end time
        // Calculate and print the elapsed time
        unsigned long dt = endTime - startTime;
        CMD.println("Time taken (dt): " + String(dt) + " ms");
      }  //if
    }    //if

    if (cmdChar == 't') {

      if (DEBUG_PRINT) {
        CMD.println("taring");  // Print cmdChar for debugging
      }

      tare_scale();

      CMD.println("t");

    }  //if

    if (cmdChar == 'c') {

      calibrate();
    }  //if

  }  //cmd serial input
}  //loop

// Function to tare the scale
int tare_scale() {
  // LoadCell.tareNoDelay();  // Start tare without delay
  LoadCell.tare();  // Start tare (blocking)

  // unsigned long startTime = millis();  // Track the time to avoid infinite waiting

  // // Wait for the tare process to finish, with a timeout
  // if (LoadCell.getTareStatus() == true) {
  //   Serial.println("Tare complete");
  // }
  // while (LoadCell.getTareStatus() != true) {
  //   // Check if the process has taken too long
  //   if (millis() - startTime > 5000) {  // 5-second timeout, adjust as needed
  //     return 1;  // Tare failed due to timeout
  //   }
  //   delay(10);  // Small delay to avoid busy-waiting too aggressively
  // }

  // // If the tare is complete, send confirmation byte and return 0 (success)
  // CMD.write(0);  // Send confirmation byte (0) after tare completion
  // return 0;  // Tare succeeded
}


void calibrate() {
  LoadCell.setCalFactor(1.0);  // Reset calibration factor to default
  tare_scale();                // Tare the scale before calibration

  CMD.println("Make sure to send 'c' calibrate command and known mass float each without line ending!");
  CMD.println("Please enter the known mass (in grams) and press Enter:");
  while (!CMD.available()) {
    // Wait for the user to submit the known mass
    delay(100);
  }

  // Read the known mass input from serial
  float known_mass = CMD.parseFloat();
  CMD.print("Known mass received: ");
  CMD.println(known_mass);  // Confirm receipt of known mass

  CMD.println("Now, please place the known weight on the scale and press 'a' to begin calibration.");

  boolean weight_added = false;
  while (!weight_added) {
    if (CMD.available()) {
      char cmdChar = CMD.read();  // Read input from user
      LoadCell.update();          // Update load cell reading

      // Wait for user to confirm the weight is placed and press 'a'
      if (cmdChar == 'a') {
        LoadCell.refreshDataSet();  // Refresh data from the load cell
        float new_calibration_factor = LoadCell.getNewCalibration(known_mass);

        CMD.print("New calibration factor: ");
        CMD.println(new_calibration_factor);

        weight_added = true;  // Calibration is complete
      }
    }
    delay(10);  // Short delay to avoid excessive CPU usage
  }
}
