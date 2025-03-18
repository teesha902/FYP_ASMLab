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

// Servo motor
Servo servo1;

// Pin assignments
#define LED1 11
#define BUTTON_1 10 // Shows welcome animation
#define BUTTON_2 9  // Immediate feeding
#define BUTTON_3 8  // Show feeding schedule
#define BUTTON_4 7  // 5-minute feeding event
#define SERVO_OPEN_ANGLE 110
#define SERVO_CLOSE_ANGLE 135
#define SERVO_OPEN_TIME 100 // Adjust this to change food amount

// Feeding schedule - this can be changed according to experimental setup
// Use the format {HH, MM, SS} in 24 hour time. Any number of feeding times can be added here, each as a different element in the array

const int feedingTimes[][3] = {
    {9, 30, 0},    
    {10, 07, 0}, 
    {15, 34, 0},   
    {20, 00, 00}
};
const int numFeedingTimes = sizeof(feedingTimes) / sizeof(feedingTimes[0]);

// Fish bitmap image
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

void setup() {
    Serial.begin(9600); 
    Serial.println("Initializing Auto-Feeder...");

    // Initialize RTC
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


    //rtc.setDateTime(__DATE__, __TIME__); // Uncomment for first-time setup, then comment & re-upload

    // Initialize OLED AFTER RTC
    Serial.println("Initializing OLED...");
    if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
        Serial.println("SSD1306 OLED allocation failed!");
        for(;;); // Halt execution if OLED fails to initialize
    }
    display.clearDisplay();
    display.setTextColor(SSD1306_WHITE);
    Serial.println("OLED Ready!");
    
    // Initialize Servo
    servo1.attach(12);
    servo1.write(SERVO_CLOSE_ANGLE);
    delay(1000);

    // Set button & LED pins
    pinMode(LED1, OUTPUT);
    pinMode(BUTTON_1, INPUT_PULLUP);
    pinMode(BUTTON_2, INPUT_PULLUP);
    pinMode(BUTTON_3, INPUT_PULLUP);
    pinMode(BUTTON_4, INPUT_PULLUP);

    // Debugging: Print current time
    now = rtc.getDateTime();
    Serial.print("Time now: ");
    Serial.print(now.year);   Serial.print("-");
    Serial.print(now.month);  Serial.print("-");
    Serial.print(now.day);    Serial.print(" ");
    Serial.print(now.hour);   Serial.print(":");
    Serial.print(now.minute); Serial.print(":");
    Serial.print(now.second); Serial.println("");

    // Show welcome animation
    welcomeAnimation();
    display.clearDisplay();
    Serial.println("Setup Complete.");
}

void loop() {
    now = rtc.getDateTime();
    static int lastFedMinute = -1; // Keeps track of the last fed minute to prevent multiple feeds

    // Check if it's time for a scheduled feeding
    for (int i = 0; i < numFeedingTimes; i++) {
        if (now.hour == feedingTimes[i][0] && now.minute == feedingTimes[i][1]) {  
            if (lastFedMinute != now.minute) { // Ensure feeding happens only once per minute
                Serial.println("Scheduled Feeding Time Matched!");
                displaySetFeedingTime(now);
                displayCountdown(); 
                triggerFeeding();
                displayFedConfirmation();
                lastFedMinute = now.minute; // Update last fed time
            }
        }
    }

    // Button 1 - Show welcome animation again
    if (isButtonPressed(BUTTON_1)) {
        Serial.println("Button 1 pressed - Showing Welcome Animation");
        welcomeAnimation();
    }

    // Button 2 - Immediate feeding
    if (isButtonPressed(BUTTON_2)) {
        Serial.println("Button 2 pressed - Immediate Feeding");
        displayCountdown();
        triggerFeeding();
        displayFedConfirmation();
    }

    // Button 3 - Show feeding schedule
    if (isButtonPressed(BUTTON_3)) {
        Serial.println("Button 3 pressed - Display Feeding Schedule");
        displayFeedingSchedule(feedingTimes, numFeedingTimes);
    }

    // Button 4 - 5-minute feeding event
    if (isButtonPressed(BUTTON_4)) {
        Serial.println("Button 4 pressed - 5-Minute Feeding Event");
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
        return digitalRead(buttonPin) == LOW;
    }
    return false;
}

// Helper method to format time in AM/PM
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

void triggerFeeding() {
    Serial.println("Feeding now...");
    digitalWrite(LED1, HIGH);
    delay(3000); // Keep LED on for 3 seconds
    servo1.write(SERVO_OPEN_ANGLE);          
    delay(SERVO_OPEN_TIME);
    servo1.write(SERVO_CLOSE_ANGLE);          
    delay(2000); // Keep LED on for 2 more seconds
    digitalWrite(LED1, LOW); // Turn off LED
}


// Display scheduled feeding time
void displaySetFeedingTime(const RTCDateTime& time) {
    display.clearDisplay();
    display.setTextSize(1);

    String feedingText = "Feeding!";
    String timeText = "Time: " + formatTime(time.hour, time.minute);

    int feedingX = (SCREEN_WIDTH - feedingText.length() * 6) / 2;
    int timeX = (SCREEN_WIDTH - timeText.length() * 6) / 2;

    display.setCursor(feedingX, 0);
    display.print(feedingText);

    display.setCursor(timeX, 12);
    display.print(timeText);

    display.display();
    delay(2000);
}

// BUTTON 2 FUNCTIONALITY 
//5 second countdown before feeding event
void displayCountdown() {
    for (int i = 5; i > 0; i--) {
        display.clearDisplay();
        display.setTextSize(1);

        String countdownText = "Feeding in " + String(i) + " sec";
        int countdownX = (SCREEN_WIDTH - countdownText.length() * 6) / 2;
        int centerY = (SCREEN_HEIGHT - 8) / 2; 

        display.setCursor(countdownX, centerY);
        display.print(countdownText);

        display.display();
        delay(1000);
    }

    // Show "Feeding now!" message
    display.clearDisplay();
    display.setTextSize(1);

    int nowX = (SCREEN_WIDTH - 9 * 6) / 2;  // Center "Feeding now!"
    int centerY = (SCREEN_HEIGHT - 8) / 2;

    display.setCursor(nowX, centerY);
    display.print("Feeding now!");

    display.display();
    delay(1000);
}
// Display message confirming feeding
void displayFedConfirmation() {
    display.clearDisplay();
    display.setTextSize(1);

    String fedText = "Feeding Complete!";
    int fedTextX = (SCREEN_WIDTH - fedText.length() * 6) / 2;
    int centerY = (SCREEN_HEIGHT - 8) / 2;

    display.setCursor(fedTextX, centerY);
    display.print(fedText);
    display.display();

    delay(5000);
    display.clearDisplay();
    display.display();
}


//BUTTON 3 FUNCTIONALITY 
void displayFeedingSchedule(int feedingTimes[][3], int numFeedingTimes) {
    const int scrollSpeed = 200; // Adjust speed for smoother scrolling (lower = slower)
    const int textHeight = 9; // Height of each line
    const int visibleLines = (SCREEN_HEIGHT - 12) / textHeight; // Max full lines visible
    const int totalScrollHeight = numFeedingTimes * textHeight; // Total height of all entries
    const int repeatScroll = 3; // Number of times scrolling should repeat
    const int headerY = 0; // Position of the "Feeding Times" header
    const int startScrollY = headerY + 10; // Feeding times start below the header
    const int pauseDuration = 2000; // 2-second pause before scrolling

    for (int r = 0; r < repeatScroll; r++) { // Repeat scrolling 3 times
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

//BUTTON 4 FUNCTIONALITY
void handleFiveMinuteFeeding() {
    display.clearDisplay();
    display.setTextSize(1);
    display.setCursor(10, 5);
    display.print("5 Min Feeding Event");
    display.display();
    delay(2000);

    // Countdown first minute
    for (int i = 60; i > 0; i--) {
        display.clearDisplay();
        display.setTextSize(1);
        String countdownText = "Feeding in " + String(i) + " sec";
        int countdownX = (SCREEN_WIDTH - countdownText.length() * 6) / 2;
        int centerY = (SCREEN_HEIGHT - 8) / 2;

        display.setCursor(countdownX, centerY);
        display.print(countdownText);
        display.display();
        delay(1000);
    }

    // Trigger feeding
    displayCountdown();
    triggerFeeding();
    displayFedConfirmation();

    // Final countdown to complete 5-minute duration
    for (int i = 240; i > 0; i--) { 
        display.clearDisplay();
        display.setTextSize(1);

        int minutes = i / 60;
        int seconds = i % 60;
        String countdownText = "Time left: " + String(minutes) + ":" + (seconds < 10 ? "0" : "") + String(seconds);

        int countdownX = (SCREEN_WIDTH - countdownText.length() * 6) / 2;
        int centerY = (SCREEN_HEIGHT - 8) / 2;

        display.setCursor(countdownX, centerY);
        display.print(countdownText);
        display.display();
        delay(1000);
    }

    // Display "Feeding Event Over" message
    display.clearDisplay();
    display.setTextSize(1);
    int completeX = (SCREEN_WIDTH - 20 * 6) / 2;
    int centerY = (SCREEN_HEIGHT - 8) / 2;

    display.setCursor(completeX, centerY);
    display.print("Feeding Event Over!");
    display.display();

    delay(5000);
    display.clearDisplay();
    display.display();
}