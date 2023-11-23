#include <Servo.h>

   Servo servoMotor;

void setup() {
  // Start serial communication
  Serial.begin(9600);

  // Attach the servo to pin 9
  servoMotor.attach(9);

  // Initialize the servo to 0 degrees
  servoMotor.write(0);
}

void loop() {
  if (Serial.available() > 0) {
    // Read the command from serial
    String command = Serial.readStringUntil('\n');

    // Check the command type
    if (command.charAt(0) == 'A') {
      // Get the angle value from the command
      int angle = command.substring(1).toInt();

      // Set the servo angle
      servoMotor.write(angle);

      // Send a confirmation message back to Python
      Serial.println("Angle set to " + String(angle));
    }
  }
}
