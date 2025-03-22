// Pin A = speed, Pin B = direction

const int motor1PinA = 3;
const int motor1PinB = 5;

const int motor2PinA = 6;
const int motor2PinB = 9;

int motorSpeed;

float f;

void setup() {
  pinMode(motor1PinA, OUTPUT);
  pinMode(motor1PinB, OUTPUT);

  pinMode(motor2PinA, OUTPUT);
  pinMode(motor2PinB, OUTPUT);

  Serial.begin(9600);
  Serial.setTimeout(1);
}

void loop() {
  
  // Read float type serial data
  
  if (Serial.available() >= sizeof(float)) {
    Serial.readBytes((char*)&f, sizeof(float));
    Serial.println(f);
    
    // Map motor speed based on float value
    
    if (f > 9.0) {
      motorSpeed = map(f,10.0,40.0,25,255);
      analogWrite(motor1PinA, motorSpeed);
      analogWrite(motor2PinA, motorSpeed);
    }

    if (f < 5.0) {
      motorSpeed = 0;
      analogWrite(motor1PinA, motorSpeed);
      analogWrite(motor2PinA, motorSpeed);
    }

  }
}
