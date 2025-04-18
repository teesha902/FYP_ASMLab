#include <Wire.h> // I2C communication for RTC & OLED
#include <Adafruit_GFX.h> // Graphics library for OLED
#include <Adafruit_SSD1306.h> // OLED display driver
#include <DS3231.h> // RTC library
#include <Servo.h> // Servo library

// Screen settings 
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32
#define OLED_RESET -1
#define SCREEN_ADDRESS 0x3C 

// Create display object
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Create RTC object
DS3231 rtc;
RTCDateTime now; // Object to store time data

// Servo motors
Servo servo1, servo2;

// Pin assignments
#define LED1 11
#define LED2 A1
#define BUTTON_1 10 // Select between dual/single feeding mode
#define BUTTON_2 9  // Immediate feeding
#define BUTTON_3 8  // Show feeding schedule
#define BUTTON_4 7  // 5-minute feeding event
#define SERVO_OPEN_ANGLE 110
#define SERVO_CLOSE_ANGLE 135
#define SERVO_OPEN_TIME 100 // change to give more/less food 

// Feeding schedule - this can be changed according to experimental setup
// Use the format {HH, MM, SS} in 24 hour time. Any number of feeding times can be added here, each as a different element in the array
const int feedingTimes[][3] = {
    {9, 30, 0},    
    {10, 07, 0}, 
    {15, 34, 0},   
    {20, 00, 00}
};
const int numFeedingTimes = sizeof(feedingTimes) / sizeof(feedingTimes[0]);

//FUNCTION DECLARATIONS
void triggerFeedingA();
void triggerFeedingB();
void triggerFeedingBoth();

const unsigned char PROGMEM epd_bitmap_fish [] = {
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x0f, 0x80, 
	0x00, 0x06, 0x00, 0xff, 0xf0, 0x00, 0x07, 0x01, 0xc0, 0x3c, 0x00, 0x07, 0x07, 0x00, 0x0e, 0x00, 
	0x07, 0x8e, 0x00, 0x03, 0x80, 0x06, 0xd8, 0x00, 0x01, 0xc0, 0x06, 0xf0, 0x00, 0x30, 0xc0, 0x06, 
	0x70, 0x00, 0x00, 0x60, 0x06, 0x70, 0x00, 0x00, 0x60, 0x06, 0xf0, 0x00, 0x00, 0xc0, 0x06, 0xd8, 
	0x00, 0x01, 0xc0, 0x07, 0x8e, 0x00, 0x03, 0x80, 0x07, 0x07, 0x00, 0x0e, 0x00, 0x07, 0x01, 0xc0, 
	0x3c, 0x00, 0x06, 0x00, 0xff, 0xf0, 0x00, 0x04, 0x00, 0x0f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
};

//toggle variables
enum FeedingMode { SIDE_A, SIDE_B, BOTH }; 
FeedingMode currentMode = SIDE_A; // Start with Side A
unsigned long lastButton1PressTime = 0; // Track time of last button press
bool isModeConfirmed = false; // To know if we are waiting for 5s timeout

//button 4 states
enum Button4Phase {
    INACTIVE,
    INTRO,
    TIMER,
    FEEDING_EVENT
};
Button4Phase button4Phase = INACTIVE;
unsigned long button4StartTime = 0;
bool feedingTriggered = false;

void setup() {
  Serial.begin(9600); 
    Serial.println("Initializing Auto-Feeder...");

    // Initialize RTC FIRST
    Serial.println("Initializing RTC...");
    rtc.begin();
    delay(100);

    /*
     * !!! IMPORTANT: SETTING THE RTC TIME (ONLY NEEDED ONCE) !!!
     * 
     * - The line below sets the RTC to the current date & time from your computer.
     * - This should ONLY be done the FIRST TIME you upload the code to a new feeder device OR if the RTC battery dies.
     * - After setting the time once, you MUST COMMENT OUT the line, re-upload the code, and restart the device.
     * - Why? Because leaving it active will reset the RTC every time the device is powered on.
     *
     * >>> STEPS TO SET TIME ON FIRST UPLOAD:
     * 1. Uncomment the line below (`rtc.setDateTime(__DATE__, __TIME__);`).
     * 2. Upload the code to the microcontroller.
     * 3. After uploading, **comment out the line again** to prevent resetting the time every restart.
     * 4. Upload the modified code again (with the line commented out), to allow proper initialisation of the OLED screen.
     *
     * >>> WHEN TO DO THIS AGAIN?
     * - If you are uploading code to a new device for the first time OR if the RTC battery is removed or dies. 
     * - Repeat the steps above to reset the time.
     */
    //rtc.setDateTime(__DATE__, __TIME__); // Uncomment this line ONLY for the first upload, then comment it out

    // Initialize OLED AFTER RTC
    Serial.println("Initializing OLED...");
    if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
        Serial.println("SSD1306 OLED allocation failed!");
        for(;;); // Don't proceed, loop until screen is ready
    }
    display.clearDisplay();
    display.setTextColor(SSD1306_WHITE);
    Serial.println("OLED Ready!");
    
    // Initialize Servos
    servo1.attach(12);
    servo1.write(SERVO_CLOSE_ANGLE);
    delay(1000);
    servo2.attach(13);
    servo2.write(SERVO_CLOSE_ANGLE);
    delay(1000);

    // Set button & LED pins
    pinMode(LED1, OUTPUT);
    pinMode(LED2, OUTPUT);
    pinMode(BUTTON_1, INPUT_PULLUP);
    pinMode(BUTTON_2, INPUT_PULLUP);
    pinMode(BUTTON_3, INPUT_PULLUP);
    pinMode(BUTTON_4, INPUT_PULLUP);

    //for debugging - check if correct time
    now = rtc.getDateTime();
    Serial.print("Time now: ");
    Serial.print(now.year);   Serial.print("-");
    Serial.print(now.month);  Serial.print("-");
    Serial.print(now.day);    Serial.print(" ");
    Serial.print(now.hour);   Serial.print(":");
    Serial.print(now.minute); Serial.print(":");
    Serial.print(now.second); Serial.println("");
    
    //welcomeScreen();
    welcomeAnimation();
    display.clearDisplay();
    Serial.println("Setup Complete.");
}

void loop() {
  now = rtc.getDateTime();
  static int lastFedMinute = -1; // Keeps track of the last fed minute to prevent multiple feeds

  // Check now is time for scheduled feeding -- function
  for (int i = 0; i < numFeedingTimes; i++) {
      if (now.hour == feedingTimes[i][0] &&
          now.minute == feedingTimes[i][1]) {  

          // Check if we already fed during this minute
          if (lastFedMinute != now.minute) {
              Serial.println("Scheduled Feeding Time Matched!");
              displaySetFeedingTime(now);

              switch (currentMode) {
                  case SIDE_A:
                      Serial.println("Scheduled Feeding: Side A");
                      displayCountdown("side A");
                      triggerFeedingA();
                      displayFedConfirmation("side A");
                      break;
                  case SIDE_B:
                      Serial.println("Scheduled Feeding: Side B");
                      displayCountdown("side B");
                      triggerFeedingB();
                      displayFedConfirmation("side B");
                      break;
                  case BOTH:
                      Serial.println("Scheduled Feeding: Both sides");
                      displayCountdown("both sides");
                      triggerFeedingBoth();
                      displayFedConfirmation("both sides");
                      break;
              }
              lastFedMinute = now.minute; // Update last fed time
          }
      }
  }

  //toggle single left/single right/dual feeder, last 
  if (isButtonPressed(BUTTON_1)) {
    Serial.println("Button 1 pressed");
    handleModeSelection();
  } 
  //last option toggled to is chosen (after 3 seconds)
  handleModeConfirmation();

  //Immediate feeding in selected mode + 5 second countdown
  if (isButtonPressed(BUTTON_2)) {
    Serial.println("Button 2 pressed");
    handleImmediateFeeding(); 
  }
 
  // Show scheduled feeding times 
  if (isButtonPressed(BUTTON_3)) {
    Serial.println("Button 3 pressed");
    displayFeedingSchedule(feedingTimes, numFeedingTimes, currentMode);
  }

  if (isButtonPressed(BUTTON_4)) {
    Serial.println("Button 4 pressed");
    handleFiveMinuteFeeding();
  }
}


void welcomeAnimation() {
    int fishWidth = 40;  // Width of bitmap in pixels
    int fishHeight = 40; // Height of bitmap in pixels
    int fishX = -fishWidth; // Start completely off-screen (left)
    int fishY = (SCREEN_HEIGHT - fishHeight) / 2; // Center vertically
    int maxX = SCREEN_WIDTH; // Stop moving when fish reaches the right edge

    while (fishX < maxX) { // Stop fish at maxX to prevent wrap-around
        display.clearDisplay();
        display.setTextColor(SSD1306_WHITE);
        display.drawBitmap(fishX, fishY, epd_bitmap_fish, fishWidth, fishHeight, 1);
        display.display();

        fishX++; // Move fish to the right
        delay(7); // Adjust speed if needed (lower value = faster)
    }

    display.clearDisplay();
    display.setTextSize(1);
    String readyText = "Auto-Feeder Ready!";
    int readyWidth = readyText.length() * 6;
    int readyX = (SCREEN_WIDTH - readyWidth) / 2;
    display.setCursor(readyX, SCREEN_HEIGHT / 2 - 4);
    display.print(readyText);
    display.display();
    delay(3000);
    
    display.clearDisplay();
    display.display();
}


// helper method to improve button responsiveness
bool isButtonPressed(int buttonPin) {
    if (digitalRead(buttonPin) == LOW) {  
        delay(50);                        
        if (digitalRead(buttonPin) == LOW) {  
            return true;
        }
    }
    return false;
}
// helper method to get mode name
String getMode(FeedingMode mode) {
    switch (mode) {
        case SIDE_A: return "Single Feeder - A";
        case SIDE_B: return "Single Feeder - B";
        case BOTH: return "Dual Feeder";
    }
    return ""; // Fallback, shouldn't happen
}
//helper method to format time in AM/PM time
String formatTime(int hour, int minute) {
    String period = "AM";
    if (hour >= 12) {
        period = "PM";
        if (hour > 12) hour -= 12;
    }
    if (hour == 0) hour = 12;

    char buffer[12];
    snprintf(buffer, sizeof(buffer), "%02d:%02d %s", hour, minute, period.c_str());
    return String(buffer);
}

void displaySetFeedingTime(const RTCDateTime& time) {
    display.clearDisplay();
    display.setTextSize(1);

    String feedingText = "Feeding!";
    String timeText = "Time: " + formatTime(time.hour, time.minute);

    int feedingWidth = feedingText.length() * 6;
    int timeWidth = timeText.length() * 6;

    int feedingX = (SCREEN_WIDTH - feedingWidth) / 2;
    int timeX = (SCREEN_WIDTH - timeWidth) / 2;

    display.setCursor(feedingX, 0);
    display.print(feedingText);

    display.setCursor(timeX, 12);
    display.print(timeText);

    display.display();
    delay(2000);
}


// Trigger feeding of side A
void triggerFeedingA() {
    digitalWrite(LED1, HIGH); // Turn on LED 
    delay(3000); // Keep LED on for 3 seconds
    servo1.write(SERVO_OPEN_ANGLE);          
    delay(SERVO_OPEN_TIME);
    servo1.write(SERVO_CLOSE_ANGLE);          
    delay(2000); // Keep LED on for 2 more seconds
    digitalWrite(LED1, LOW); // Turn off LED
}
// Trigger feeding of side B
void triggerFeedingB() {
    digitalWrite(LED2, HIGH); // Turn on LED 
    delay(3000); // Keep LED on for 3 seconds
    servo2.write(SERVO_OPEN_ANGLE);          
    delay(SERVO_OPEN_TIME);
    servo2.write(SERVO_CLOSE_ANGLE);          
    delay(2000); // Keep LED on for 2 more seconds
    digitalWrite(LED2, LOW); // Turn off LED
}
// Trigger feeding of both sides simultanously
void triggerFeedingBoth() {
    digitalWrite(LED1, HIGH);
    digitalWrite(LED2, HIGH); 
    delay(3000);                 
    servo1.write(SERVO_OPEN_ANGLE);
    servo2.write(SERVO_OPEN_ANGLE);          
    delay(SERVO_OPEN_TIME);  
    servo1.write(SERVO_CLOSE_ANGLE);
    servo2.write(SERVO_CLOSE_ANGLE);          
    delay(2000);              
    digitalWrite(LED1, LOW);
    digitalWrite(LED2, LOW);  
}


//BUTTON 1 FUNCTIONALITY
void handleModeSelection() {
    // Toggle the mode
    if (currentMode == SIDE_A) {
        currentMode = SIDE_B;
    } else if (currentMode == SIDE_B) {
        currentMode = BOTH;
    } else if (currentMode == BOTH) {
        currentMode = SIDE_A;
    }
    // Show immediate feedback of toggling
    displayMode(currentMode);
    // Record the time for confirmation process
    lastButton1PressTime = millis();
    isModeConfirmed = true;
}
void handleModeConfirmation() {
    if (isModeConfirmed) {
        unsigned long elapsedTime = millis() - lastButton1PressTime;

        if (elapsedTime >= 3000 && elapsedTime < 8000) {
            display.clearDisplay();
            display.setTextSize(1);

            String selectedText = "Selected Mode:";
            String modeText = getMode(currentMode);

            int selectedWidth = selectedText.length() * 6;
            int modeWidth = modeText.length() * 6;

            int selectedX = (SCREEN_WIDTH - selectedWidth) / 2;
            int modeX = (SCREEN_WIDTH - modeWidth) / 2;

            // Vertically center the two lines as a block
            int blockHeight = 2 * 8; // Two lines, each 8 pixels high
            int blockY = (SCREEN_HEIGHT - blockHeight) / 2;

            display.setCursor(selectedX, blockY);
            display.print(selectedText);

            display.setCursor(modeX, blockY + 10); 
            display.print(modeText);

            display.display();
        } else if (elapsedTime >= 8000) {
            display.clearDisplay();
            display.display();

            isModeConfirmed = false; // Reset the flag
        }
    }
}
//Get mode and center of screen when displaying
void displayMode(FeedingMode mode) {
    display.clearDisplay();
    display.setTextSize(1);

    String modeText = getMode(mode);
    int modeWidth = modeText.length() * 6;
    int modeX = (SCREEN_WIDTH - modeWidth) / 2;
    int modeY = (SCREEN_HEIGHT - 8) / 2; // Center vertically

    display.setCursor(modeX, modeY);
    display.print(modeText);

    display.display();
}


//BUTTON 2 FUNCTIONALITY
void handleImmediateFeeding() {
    // show which mode will be fed
    displayImmediateFeedingStart(currentMode);

    // countdown + feeding
    switch (currentMode) {
        case SIDE_A:
            displayCountdown("side A");
            triggerFeedingA();
            displayFedConfirmation("side A");
            break;

        case SIDE_B:
            displayCountdown("side B");
            triggerFeedingB();
            displayFedConfirmation("side B");
            break;

        case BOTH:
            displayCountdown("both sides");
            triggerFeedingBoth();
            displayFedConfirmation("both sides");
            break;
    }
}
void displayImmediateFeedingStart(FeedingMode mode) {
    display.clearDisplay();
    display.setTextSize(1);

    String feedingNowText = "Feeding Now";
    String modeText = getMode(mode);

    int feedingNowWidth = feedingNowText.length() * 6;
    int modeWidth = modeText.length() * 6;

    int feedingNowX = (SCREEN_WIDTH - feedingNowWidth) / 2;
    int modeX = (SCREEN_WIDTH - modeWidth) / 2;

    int centerY = (SCREEN_HEIGHT - 2 * 8) / 2; // Centering vertically (2 lines)

    display.setCursor(feedingNowX, centerY);
    display.print(feedingNowText);

    display.setCursor(modeX, centerY + 10);
    display.print(modeText);

    display.display();
    delay(2000);
}
//5 second countdown before feeding event
void displayCountdown(const char* side) {
    char feedingText[30]; 
    if (strcmp(side, "both sides") == 0) {
        strcpy(feedingText, "Feeding both sides");
    } else {
        snprintf(feedingText, sizeof(feedingText), "Feeding %s", side);
    }

    for (int i = 5; i > 0; i--) {
        display.clearDisplay();
        display.setTextSize(1);

        char countdownText[15];
        snprintf(countdownText, sizeof(countdownText), "in %d sec", i);

        int feedingTextWidth = strlen(feedingText) * 6;
        int countdownTextWidth = strlen(countdownText) * 6;

        int feedingX = (SCREEN_WIDTH - feedingTextWidth) / 2;
        int countdownX = (SCREEN_WIDTH - countdownTextWidth) / 2;

        int centerY = (SCREEN_HEIGHT - 2 * 8) / 2; 

        display.setCursor(feedingX, centerY);
        display.print(feedingText);

        display.setCursor(countdownX, centerY + 10);
        display.print(countdownText);

        display.display();
        delay(1000);
    }

    // Display "now!" message
    display.clearDisplay();
    display.setTextSize(1);

    int feedingTextWidth = strlen(feedingText) * 6;
    int nowWidth = 4 * 6; 

    int feedingX = (SCREEN_WIDTH - feedingTextWidth) / 2;
    int nowX = (SCREEN_WIDTH - nowWidth) / 2;

    int centerY = (SCREEN_HEIGHT - 2 * 8) / 2;

    display.setCursor(feedingX, centerY);
    display.print(feedingText);

    display.setCursor(nowX, centerY + 10);
    display.print("now!");

    display.display();
    delay(1000);
}
void displayFedConfirmation(const char* side) {
    display.clearDisplay();
    display.setTextSize(1);

    char fedText[30]; 
    if (strcmp(side, "both sides") == 0) {
        strcpy(fedText, "Fed both sides!");
    } else {
        snprintf(fedText, sizeof(fedText), "Fed %s!", side);
    }

    int fedTextWidth = strlen(fedText) * 6;
    int fedTextX = (SCREEN_WIDTH - fedTextWidth) / 2;

    int centerY = (SCREEN_HEIGHT - 8) / 2;

    display.setCursor(fedTextX, centerY);
    display.print(fedText);
    display.display();

    delay(5000);
    display.clearDisplay();
    display.display();
}



//BUTTON 3 functionality
void displayCurrentTime() {
    RTCDateTime now = rtc.getDateTime();
    String currentTime = formatTime(now.hour, now.minute);

    display.clearDisplay();
    display.setTextSize(1);

    String header = "Current Time";
    int headerX = (SCREEN_WIDTH - header.length() * 6) / 2;
    int timeX = (SCREEN_WIDTH - currentTime.length() * 6) / 2;
    int centerY = (SCREEN_HEIGHT - 2 * 8) / 2;

    display.setCursor(headerX, centerY);
    display.print(header);

    display.setCursor(timeX, centerY + 10);
    display.print(currentTime);

    display.display();
    delay(3000); // Show time for 3 seconds
}

void displayFeedingSchedule(int feedingTimes[][3], int numFeedingTimes, FeedingMode currentMode) {
    const int scrollSpeed = 200; // Adjust speed for smoother scrolling (lower = slower)
    const int textHeight = 9; // Height of each line
    const int visibleLines = (SCREEN_HEIGHT - 12) / textHeight; // Max full lines visible
    const int totalScrollHeight = numFeedingTimes * textHeight; // Total height of all entries
    const int repeatScroll = 3; // Number of times scrolling should repeat
    const int headerY = 0; // Position of the "Feeding Times" header
    const int startScrollY = headerY + 10; // Feeding times start below the header
    const int pauseDuration = 2000; // 2-second pause before scrolling

    for (int r = 0; r < repeatScroll; r++) { // Repeat scrolling 3 times
        displayCurrentTime();
        int scrollOffset = 0;

        // Display feeding schedule before scrolling starts
        display.clearDisplay();
        display.setTextSize(1);
        display.setTextColor(SSD1306_WHITE);

        // Display header (STATIC)
        int headerX = (SCREEN_WIDTH - 14 * 6) / 2; // Centered header
        display.setCursor(headerX, headerY);
        display.print("Feeding Times");

        // Display as many feeding times as fit on the screen
        for (int i = 0; i < min(numFeedingTimes, visibleLines); i++) {
            int yPosition = startScrollY + (i * textHeight);
            String timeText = formatTime(feedingTimes[i][0], feedingTimes[i][1]);
            int timeWidth = timeText.length() * 6;
            int timeX = (SCREEN_WIDTH - timeWidth) / 2;

            display.setCursor(timeX, yPosition);
            display.print(timeText);
        }

        display.display();
        delay(pauseDuration); // Pause for 2 seconds before scrolling

        // Start scrolling, keeping the header fixed
        int maxScrollOffset = totalScrollHeight - (visibleLines * textHeight) + textHeight;
        // Ensures last item scrolls out fully without pushing the first entry over the header

        while (scrollOffset <= maxScrollOffset) {
            display.clearDisplay();
            display.setTextSize(1);
            display.setTextColor(SSD1306_WHITE);

            // Keep the header fixed
            display.setCursor(headerX, headerY);
            display.print("Feeding Times");
            // Scroll feeding times (Prevent them from crossing over the header)
            for (int i = 0; i < numFeedingTimes; i++) {
                int yPosition = startScrollY + (i * textHeight) - scrollOffset;

                if (yPosition >= startScrollY && yPosition <= SCREEN_HEIGHT) { 
                    // Only draw visible times, ensuring they don't overwrite the header
                    String timeText = formatTime(feedingTimes[i][0], feedingTimes[i][1]);
                    int timeWidth = timeText.length() * 6;
                    int timeX = (SCREEN_WIDTH - timeWidth) / 2;

                    display.setCursor(timeX, yPosition);
                    display.print(timeText);
                }
            }

            display.display();
            delay(50); // Smooth scrolling delay
            scrollOffset += 1;
        }
    }

    // Clear screen after finishing
    display.clearDisplay();
    display.display();
}


//BUTTON 4 functionality
void handleFiveMinuteFeeding() {
    // Show event start message
    displayFiveMinuteFeedingStart(currentMode);

    // Countdown first minute
    displayCountdownOneMinute(currentMode);

    // Feeding event after 1 minute
    switch (currentMode) {
        case SIDE_A:
            displayCountdown("side A");
            triggerFeedingA();
            displayFedConfirmation("side A");
            break;
        case SIDE_B:
            displayCountdown("side B");
            triggerFeedingB();
            displayFedConfirmation("side B");
            break;
        case BOTH:
            displayCountdown("both sides");
            triggerFeedingBoth();
            displayFedConfirmation("both sides");
            break;
    }
    // Countdown remaining time (to reach 5:00 total)
    displayFinalCountdown();
}
// Show message that the 5-minute event has started
void displayFiveMinuteFeedingStart(FeedingMode mode) {
    display.clearDisplay();
    display.setTextSize(1);

    String feedingNowText = "5 Min Feeding Event";
    String modeText = getMode(mode);

    int feedingNowWidth = feedingNowText.length() * 6;
    int modeWidth = modeText.length() * 6;

    int feedingNowX = (SCREEN_WIDTH - feedingNowWidth) / 2;
    int modeX = (SCREEN_WIDTH - modeWidth) / 2;

    int centerY = (SCREEN_HEIGHT - 2 * 8) / 2; // Centering vertically

    display.setCursor(feedingNowX, centerY);
    display.print(feedingNowText);

    display.setCursor(modeX, centerY + 10);
    display.print(modeText);

    display.display();
    delay(2000);
}
// First-minute countdown (display numbers counting down from 60 to 0) and include side
void displayCountdownOneMinute(FeedingMode mode) {
    char modeText[20];

    // Ensure mode is correctly assigned
    switch (mode) {
        case SIDE_A: strcpy(modeText, "Side A"); break;
        case SIDE_B: strcpy(modeText, "Side B"); break;
        case BOTH: strcpy(modeText, "Both Sides"); break;
        default: strcpy(modeText, "Unknown"); break; // Fallback in case of error
    }

    for (int i = 60; i > 0; i--) {
        display.clearDisplay();
        display.setTextSize(1);

        char line1[] = "Feeding event for";
        char line2[20]; 
        snprintf(line2, sizeof(line2), "%s", modeText);  // Properly formatted mode name

        char line3[20];
        snprintf(line3, sizeof(line3), "starting in %d s", i);

        int line1Width = strlen(line1) * 6;
        int line2Width = strlen(line2) * 6;
        int line3Width = strlen(line3) * 6;

        int centerX1 = (SCREEN_WIDTH - line1Width) / 2;
        int centerX2 = (SCREEN_WIDTH - line2Width) / 2;
        int centerX3 = (SCREEN_WIDTH - line3Width) / 2;

        int centerY = (SCREEN_HEIGHT - 3 * 8) / 2; 

        display.setCursor(centerX1, centerY);
        display.print(line1);

        display.setCursor(centerX2, centerY + 10);
        display.print(line2);  // Now properly displays mode (Side A, Side B, Both Sides)

        display.setCursor(centerX3, centerY + 20);
        display.print(line3);

        display.display();
        delay(1000);
    }
}

// Countdown after feeding event (to complete the 5 minutes)
void displayFinalCountdown() {
    for (int i = 240; i > 0; i--) { // 4 minutes remaining
        display.clearDisplay();
        display.setTextSize(1);

        int minutes = i / 60;
        int seconds = i % 60;

        char countdownText[20]; 
        snprintf(countdownText, sizeof(countdownText), "Time left: %02d:%02d", minutes, seconds);

        int countdownTextWidth = strlen(countdownText) * 6;
        int countdownX = (SCREEN_WIDTH - countdownTextWidth) / 2;

        int centerY = (SCREEN_HEIGHT - 8) / 2;

        display.setCursor(countdownX, centerY);
        display.print(countdownText);

        display.display();
        delay(1000);
    }

    // Show event completion message
    display.clearDisplay();
    display.setTextSize(1);

    char completeText[] = "Feeding Event Over!";
    int completeTextWidth = strlen(completeText) * 6;
    int completeX = (SCREEN_WIDTH - completeTextWidth) / 2;

    int centerY = (SCREEN_HEIGHT - 8) / 2;

    display.setCursor(completeX, centerY);
    display.print(completeText);
    display.display();

    delay(5000);
    display.clearDisplay();
    display.display();
}
