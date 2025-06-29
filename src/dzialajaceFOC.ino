#include <SimpleFOC.h>
#include <Adafruit_BNO08x.h>
#include <PID_v1.h>

//============= IMU ================

Adafruit_BNO08x bno085(-1);
sh2_SensorValue_t sensorValue;

//============= Motor ================
MagneticSensorI2C sensor = MagneticSensorI2C(AS5600_I2C);

BLDCMotor motor = BLDCMotor(7);
//BLDCMotor motor = BLDCMotor(7,21.5, 140);

BLDCDriver3PWM driver = BLDCDriver3PWM(6, 5, 4, 3);


float target = 1;
Commander command = Commander(Serial);
void doTarget(char* cmd) { command.scalar(&target, cmd); }
void doMotor(char* cmd) { command.motor(&motor, cmd); }


void setReports(void) {
  Serial.println("Setting desired reports");
  if (! bno085.enableReport(SH2_ACCELEROMETER)) {
    Serial.println("Could not enable game vector");
  }
}

void print(String name, float value){
  Serial.print(">");
  Serial.print(name);
  Serial.print(":");
  Serial.println(value);
}

void setup() {
  Serial.begin(115200);

  //============= IMU ================
  if(!bno085.begin_I2C()){
    Serial.println("IMU nie dziala");
  }
  Serial.println("IMU dziala");



  //============= MOTOR ================
  // pinMode(2, OUTPUT);
  // digitalWrite(2, HIGH);
  SimpleFOCDebug::enable(&Serial);

  sensor.init();

  driver.voltage_power_supply = 24.0;
  driver.init();

  motor.linkSensor(&sensor);
  motor.linkDriver(&driver);
  motor.useMonitoring(Serial);

  motor.foc_modulation = FOCModulationType::SinePWM;

  motor.controller = MotionControlType::angle;

  motor.PID_velocity.P = 1.2;
  motor.PID_velocity.I = 40.0f;
  motor.PID_velocity.D = 0.0f;

  motor.P_angle.P = 20.0f; 
  motor.P_angle.I = 1.0f;
  motor.P_angle.D = 100.0f;

  motor.LPF_velocity.Tf = 0.01f;

  motor.voltage_limit = 30.0;
  motor.velocity_limit = 2.0;
  
  motor.init();
  motor.initFOC();

  command.add('T', doTarget, "target angle");
  command.add('M',doMotor,'motor');

  motor.monitor_downsample = 0;

  Serial.println(F("Motor ready."));
  _delay(1000);

  setReports();
}


void loop() {
  motor.loopFOC();
  motor.move(6);
  motor.monitor();

  print("Angle", sensor.getPreciseAngle());
  print("Velocity", sensor.getVelocity());

  if (bno085.wasReset()) {
    Serial.print("sensor was reset ");
  }

  if (!bno085.getSensorEvent(&sensorValue)) {
    return;
  }

  switch (sensorValue.sensorId) {
    case SH2_ACCELEROMETER:    
      print("x", sensorValue.un.accelerometer.x);
      print("y", sensorValue.un.accelerometer.y);
      print("z", sensorValue.un.accelerometer.z);
      break;
  }

  command.run();
}
