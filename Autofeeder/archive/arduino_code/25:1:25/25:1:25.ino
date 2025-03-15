#include <Wire.h>               // I2C for RTC module (communication w Arduino (master - requests time), RTC - slave)
#include <DS1307.h>             // Library for DS1307 RTC module ?
#include <Servo.h>              // Servo motor control library
#include <LiquidCrystal_I2C.h>  // LCD display library

LiquidCrystal_I2C lcd(0x27, 16, 2); //Initialise LCD 
    //0x27 = unique identifier for LCD module in I2C communication
    //16, 2 = chars (rows and cols)

Servo servo1, servo2;
DS1307 rtc(A4, A5);
// Define debounce delay (for button presses) 
#define DEBOUNCE_DELAY 50
  // ensures button press is counted only once, preventing false multiple activations - delay to ensure signal stabilised 
  // program waits 50ms before considering it "real" press

//define LED pins 
#define LED1 11
#define LED2 A1
//define buttons 
const int BUTTON1 = 7;  // 5-min feed (1x)
const int BUTTON2 = 8;  // 5-min feed (3x)
const int BUTTON3 = 9;  // Timed feeding at 12:00 PM
const int BUTTON4 = 10; // Timed input (future feature)
// Servo open/close angles
const int SERVO_OPEN_ANGLE = 110;
const int SERVO_CLOSE_ANGLE = 135;
bool servoActivated = false; // Flag to prevent multiple servo activations 
bool sideA = true; 
bool sideB = false; 

// Variables for button debounce - help check
bool lastButtonStateF1 = HIGH; //Remembers last button state (prevents multiple triggers from 1 press)
unsigned long lastDebounceTimeF1 = 0; //Stores time of last button press (check debounce delay)

//set feeding times (use 24h time): 
//feeding at 09:30:00 
const int hr1 = 09
const int min1 = 30
const int sec1 = 00
  //can also set for more times in the day (e.g. hr2, min2, sec2)

void setup() {
    Serial.begin(115200);

    // Initialize RTC module
    rtc.begin();
    if (!rtc.begin()) {
      Serial.println("Couldn't find RTC");
      while (1); // Stop the program
    }
    rtc.halt(false); //ensures clock is running after init
    //following lines help other devices (arduino) sync to RTC time keeping
    rtc.setSQWRate(SQW_RATE_1); 
    rtc.enableSQW(true); 

    // Check if RTC is already running ***
    if (!rtc.isrunning()) {
        Serial.println("RTC is NOT running, setting time...");
        rtc.adjust(DateTime(2025, 1, 31, 14, 30, 0));  // YYYY, MM, DD, HH, MM, SS
    } else {
        Serial.println("RTC is running, no need to set time.");
    }

    // Initialize LCD
    lcd.init();
    lcd.backlight(); //turn on backlight of LCD 

    // Initialize Servos - attach both to same pin/command
    servo1.attach(12);
    servo1.write(SERVO_CLOSE_ANGLE);
    delay(1000);
    servo2.attach(12);
    servo2.write(SERVO_CLOSE_ANGLE);
    delay(1000);

    // Initialize Buttons
    //default = set times 
    pinMode(BUTTON1, INPUT_PULLUP); //toggle - single/dual feeder mode
    pinMode(BUTTON2, INPUT_PULLUP); // immediate feeding (testing LED and servo)
    pinMode(BUTTON3, INPUT_PULLUP); // 1 shot in 5 min
    pinMode(BUTTON4, INPUT_PULLUP); // 3 shot in 5 min

    // Initialize LEDs
    pinMode(LED1, OUTPUT);
    pinMode(LED2, OUTPUT);

    // Display startup message
    showStartupSequence(); ??
}

//check time for default feedings + check if button pressed
void loop() {
    // Fetch current time
    String currentTime = rtc.getTimeStr();
    int hour = currentTime.substring(0, 2).toInt();
    int minute = currentTime.substring(3, 5).toInt();
    int second = currentTime.substring(6, 8).toInt();

    // Display menu options
    displayMenu(); ///(necessary) ?

    // Read buttons and execute actions
    handleButtonPresses();

    // Run (if servo not alr activated)
    if (hour == hr1 && minute == min1 && second == sec1 && !servoActivated) {
        lcd.setCursor(0, 0);
        lcd.print("Feeding in process...");
        //Side 1  --> integrate w toggle status
        activateOneFeeding(servo1, LED1);
        servoActivated = true;
    }
    delay(500);
}

//HELPER FUNCTIONS:
// Displays startup sequence
void showStartupSequence() {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Starting AutoFeeder....");
    delay(2000);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Toggle dual/single feeder via button 1");
    delay(2000);
    lcd.clear()
}

// Displays the main menu on LCD (CHANGE)
void displayMenu() {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("1:5m-1x  2:5m-3x");
    lcd.setCursor(0, 1);
    lcd.print("3:12:00  4:Time2");
}

// Handles button presses with debounce
// BUTTON 1: toggle - single/dual feeder mode -> INSTEAD: toggle: single1, single2, both 
// BUTTON 2: immediate feeding (testing LED and servo)
// BUTTON 3: shot in 5 min
// BUTTON 4: 3 shot in 5 min

void handleButtonPresses() {
    int readingF1 = digitalRead(BUTTON1);
    int readingF2 = digitalRead(BUTTON2);
    int readingF3 = digitalRead(BUTTON3);
    int readingF4 = digitalRead(BUTTON4);
    // Calls debounceButton() to filter out noise before accepting button press

    if (debounceButton(readingF1, lastButtonStateF1, lastDebounceTimeF1)) {
      if (sideA && !sideB) { // if only sideA -> change to sideB
        sideA = false; 
        sideB = true; 
        activateOneFeeding(servo2, LED2)
      } else if (!sideA && sideB) { // if only sideB -> change to both
        sideA = true; 
        sideB = true;
        activateBoth() { 
      } else if (sideA && sideB) { // if both -> change to only sideA
        sideA = true; 
        sideB = false;
        activateOneFeeding(servo1, LED1)
      }

    }

    if (readingF2 == LOW) {

        runFeedingCycle(servo1, LED1, 3);
    }

    if (readingF3 == LOW) {
        lcd.setCursor(0, 0);
        lcd.print("Manual Feed 12:00");
        activateFeeding(servo1, LED1);
    }

    if (readingF4 == LOW) {

        lcd.setCursor(0, 0);
        lcd.print("Feature Coming...");
        delay(2000);
    }
}

// Debounce function for buttons - Ensures only intentional presses registered (then returns true)
bool debounceButton(int currentState, bool &lastState, unsigned long &lastTime) {
    //checks 3 conditions before accepting button is pressed
    if (currentState == LOW && lastState == HIGH && (millis() - lastTime) > DEBOUNCE_DELAY) {
      //if pressed: 
      lastTime = millis(); // -> updates last time pressed to (now)?
      lastState = currentState; //updates last state to current state 
      return true;
    }
    lastState = currentState;
    return false;
}

// Runs n feeding cycles with 5 min delay between each
void runFeedingCycle(Servo &servo, int ledPin, int cycles) {
    for (int i = 0; i < cycles; i++) {
        lcd.setCursor(0, 0);
        lcd.print("Feeding Cycle: ");
        lcd.print(i + 1);
        delay(300000); // 5 minutes

        activateFeeding(servo, ledPin);
    }
}

// Activates servo and LED for feeding
void activateOneFeeding(Servo &servo, int ledPin) { 
    //LED on for 5 seconds, then after closing: 
    //servo open for 200 ms 
    digitalWrite(ledPin, HIGH);
    delay(5000);
    digitalWrite(ledPin, LOW);
    servo.write(SERVO_OPEN_ANGLE);
    delay(200);
    servo.write(SERVO_CLOSE_ANGLE);
    lcd.clear();
    lcd.print("Feeding complete");
    delay(2000);
}

void activateBoth() { 
    digitalWrite(LED1, HIGH);
    digitalWrite(LED2, HIGH);
    delay(5000);
    digitalWrite(LED1, LOW);
    digitalWrite(LED2, LOW);
    servo1.write(SERVO_OPEN_ANGLE);
    servo2.write(SERVO_OPEN_ANGLE);
    delay(200);
    servo1.write(SERVO_CLOSE_ANGLE);
    servo2.write(SERVO_CLOSE_ANGLE);
    lcd.clear();
    lcd.print("Feeding complete");
    delay(2000);
}

