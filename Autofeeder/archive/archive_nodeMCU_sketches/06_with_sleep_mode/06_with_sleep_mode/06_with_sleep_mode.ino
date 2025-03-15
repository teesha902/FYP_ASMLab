#include <Wire.h>               // I2C communication for RTC module
#include <RTClib.h>             // Library for DS1307 RTC module
#include <Servo.h>              // Library for controlling servo motor
#include <Adafruit_GFX.h>       // Graphics library for TFT display
#include <Adafruit_TFTLCD.h>    // TFT display control library
#include <LowPower.h>           // Power saving and sleep mode

// Pin definitions
const int SERVO_PIN = 9;
const int LED_PIN = 7;
const int BUTTON1 = 2; // Button 1 (Event Mode)
const int BUTTON2 = 3; // Button 2 (Sleep/Wake Mode)
const int BUTTON3 = 4; // Button 3 (Return to Default Mode)
const int BUTTON4 = 5; // Button 4 (Show Menu)
const int TFT_CS = 10; // TFT Chip Select pin
const int TFT_DC = 9;  // TFT Data/Command pin
const int TFT_RST = 8; // TFT Reset pin

// TFT and RTC objects
Adafruit_TFTLCD tft(TFT_CS, TFT_DC, TFT_RST); // TFT display object
RTC_DS1307 rtc; // RTC module object
Servo myServo; // Servo motor object

// State variables
bool isSleeping = false; // Power-saving mode status
unsigned long lastInteractionTime = 0; // Tracks last user interaction
const int idleTime = 15000; // Auto sleep after 15 seconds - for power saving

void setup() {
  // Initialize Serial Monitor
  Serial.begin(9600);
  
  // Initialize RTC
  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }
  if (!rtc.isrunning()) {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__))); // Set RTC to compile time
  }
  
  // Initialize TFT Display
  tft.begin();
  tft.setRotation(1); // Rotate display to landscape
  tft.fillScreen(BLACK); // Clear the screen
  tft.setTextColor(WHITE); // White text color
  
  // Initialize Servo
  myServo.attach(SERVO_PIN);
  myServo.write(0); // Set servo to default position
  
  // Initialize LED and buttons
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON1, INPUT_PULLUP);
  pinMode(BUTTON2, INPUT_PULLUP);
  pinMode(BUTTON3, INPUT_PULLUP);
  pinMode(BUTTON4, INPUT_PULLUP);
  
  showWelcomeScreen(); // Displays welcome message
  lastInteractionTime = millis();
}

void loop() {
  if (isSleeping) {
    //Deep sleep mode for power saving 
    LowPower.powerDown(SLEEP_FOREVER, ADC_OFF, BOD_OFF);
      //SLEEP_FOREVER: sleep indefinitely until it woken (by button)
      //ADC_OFF: Turns off  Analog-to-Digital Converter - save power
      //BOD_OFF: Turns off Brown-Out Detector (monitors the power supply voltage)
    isSleeping = false;
    tft.fillScreen(BLACK);
    showStatus("Awake! Default mode active.");
  }

  // Event Handling - Check which button pressed -- activates corresponding mode
  if (!digitalRead(BUTTON1)) activateEventMode();
  else if (!digitalRead(BUTTON2)) toggleSleepMode();
  else if (!digitalRead(BUTTON3)) returnToDefaultMode();
  else if (!digitalRead(BUTTON4)) showMenu();

  // Run Default Mode (Servo open/close at set times)
  runDefaultMode();

  // Auto sleep after idle time
  if (millis() - lastInteractionTime > idleTime) {
    enterSleepMode();
  }
}

void runDefaultMode() {
  DateTime now = rtc.now();
  //dafault time to set everyday (e.g. 09:00 & 18:00)
  if ((now.hour() == 9 && now.minute() == 0) || (now.hour() == 18 && now.minute() == 0)) {
    openAndCloseServo();
  }
}

//EVENT/BUTTON  1
void activateEventMode() {
  lastInteractionTime = millis();
  showStatus("LED event starting...");

  // Pre-event countdown
  for (int i = 5; i > 0; i--) {
    showCountdown("Get ready to film!", i);
    delay(1000);
  }

  // 3-minute countdown
  showCountdown("Event running [3 min] ", 180);

  // Countdown before LED activation
  for (int i = 120; i > 0; i--) {
    if (i == 60) {
      digitalWrite(LED_PIN, HIGH);
      showCountdown("LED On for 5s", 5);
      delay(5000);
      digitalWrite(LED_PIN, LOW);
    }
    showCountdown("Countdown to feeding", i);
    delay(1000);
  }

  // Servo activation countdown
  for (int i = 5; i > 0; i--) {
    showCountdown("Servo opening in", i);
    delay(1000);
  }
  openAndCloseServo();

  // Timer for 2 minutes after servo opening
  showCountdown("Post-event timer [2 min]", 120);
  delay(120000);

  showStatus("Learning event complete!");
}

void showCountdown(const char* message, int seconds) {
  tft.fillScreen(BLACK);
  tft.setCursor(0, 0);
  tft.print(message);
  tft.print(" - ");
  tft.print(seconds);
  tft.println("s remaining");
}

//EVENT/BUTTON 2
void toggleSleepMode() {
  lastInteractionTime = millis();
  isSleeping = !isSleeping;
  if (isSleeping) {
    showStatus("Going to sleep...");
    delay(1000);
  }
}

//EVENT/BUTTON 3
void returnToDefaultMode() {
  lastInteractionTime = millis();
  showStatus("Returning to default mode...");
}

//EVENT/BUTTON 4 -- Shows available options on the display.
void showMenu() {
  lastInteractionTime = millis();
  tft.fillScreen(BLACK);
  tft.setCursor(0, 0);
  tft.println("Menu:");
  tft.println("1. LED Event Mode");
  tft.println("2. Sleep/Wake Toggle");
  tft.println("3. Default Mode");
  tft.println("4. Show Menu");
}

void enterSleepMode() {
  isSleeping = true;
  showStatus("Idle... Entering sleep mode");
  delay(1000);
}

//Opens and closes the servo for 150ms.
void openAndCloseServo() {
  myServo.write(90); // Open position
  delay(150);        // Stay open for 150 ms
  myServo.write(0);  // Close position
}

//Displays a startup message.
void showWelcomeScreen() {
  tft.fillScreen(BLACK);
  tft.setCursor(0, 0);
  tft.println("Dual Channel Feeder");
  tft.println("Initializing...");
  delay(2000);
  tft.fillScreen(BLACK);
  showStatus("Default mode active");
}

// Updates the display with a status message
void showStatus(const char* message) {
  tft.fillScreen(BLACK);
  tft.setCursor(0, 0);
  tft.println(message);
}

