# **Auto-Feeder System Program**  

This document explains the **functionality**, **button operations**, and **customization options** for the Auto-Feeder System. The system automates feeding schedules using an **Arduino, OLED display, RTC module (Real-Time Clock), and servo motors**.

---

## **1. Hardware Requirements**  
- **Arduino Board** (e.g., Arduino Uno)  
- **OLED Display (SSD1306, I2C communication)** *(for displaying messages and status information)*  
- **DS3231 RTC Module** *(keeps track of time, requires setup if battery loses power)*  
- **Servo Motors** *(release food at scheduled times and manual triggers)*  
- **Push Buttons** *(for feeding control and mode selection)*  
- **LED Indicators** * (used in feeding events)*  

---

## **2. Button Functionalities**  

| **Button**  | **Functionality** |
|-------------|-------------------|
| **Button 1** (Mode Selection) | Cycles between **Side A**, **Side B**, and **Both** feed modes. The selected mode is confirmed after 3 seconds. |
| **Button 2** (Immediate Feeding) | **Triggers feeding immediately** based on the **selected mode** after a 5-second countdown. |
| **Button 3** (View Feeding Schedule) | **Displays the scheduled feeding times** programmed into the device (can be changed)**. |
| **Button 4** (5-Minute Feeding Event) | **Starts a 5-minute feeding event**. The event consists of a **1-minute countdown**, a **feeding event at 1:00**, and a **final countdown until 5:00**. |

---

## **3. How to Change the Scheduled Feeding Times**  
The scheduled feeding times are defined in the `feedingTimes` array. To modify them, **edit the values at line 42** in the code:

```cpp
// Line 42: Feeding schedule (Change times here)
const int feedingTimes[][3] = {
    {9, 30, 0},    // 9:30 AM
    {10, 07, 0},   // 10:07 AM
    {15, 34, 0},   // 3:34 PM
    {20, 00, 00}   // 8:00 PM
};
```

### **Format:**
- `{hour, minute, second}`
- Use **24-hour format** (e.g., `{15, 00, 00}` for 3:00 PM).  
- You can **add or remove entries** to change the number of scheduled feedings.  

---

## **4. How and When to Set the RTC (Real-Time Clock)**  

The **RTC (DS3231)** is responsible for keeping track of the current time, even when the system is turned off. It has a **small battery inside** to maintain time when the main power is off.

### **When to Set the RTC**
- **If uploading program into a new device for the first time**
- **If the RTC loses power** (e.g., the backup battery dies), the clock **will reset** and feeding times will be inaccurate.
- **If the system is displaying the wrong time**, the RTC must be reset.

### **How to Set the RTC**
To set the RTC to **your computer's current time**, go to **line 88** in `setup()` and **uncomment the following line**:
```cpp
// Line 88: Uncomment this line to set RTC time
rtc.setDateTime(__DATE__, __TIME__); // Uncomment only when setting RTC
```
Then, **upload the code to the Arduino**. This will sync the RTC with your computer's time.

### **Why This Line Needs to Be Commented Again**
Once the RTC is set, **comment the line back** by adding `//` in front of it:
```cpp
// rtc.setDateTime(__DATE__, __TIME__);  // Comment this after first upload 
```
If this line is left **uncommented**, the RTC will reset **every time the Arduino restarts**.

---

## **5. Adjusting Feeding Amount (Servo Open Time)**
The **amount of food dispensed** is determined by the **servo open time**.  
Currently, the system delivers **2 mg of micropellets** per feeding by opening the servo arm for 150 ms.

To adjust the **feeding amount**, modify the value at **line 39**:

```cpp
// Line 39: Adjust food dispensing duration
#define SERVO_OPEN_TIME 150  // Adjust this value to change dispensing time
```

### **Important Notes:**
- **Increasing this value** will dispense more food.
- **Decreasing this value** will dispense less food.
- **If changed, the amount dispensed must be weighed manually** to ensure correct feeding portions.

---

## **5. Using the Serial Monitor to Debug Issues**  

The **Serial Monitor** is a tool in the **Arduino IDE** that helps check if the system is working correctly. It can be used to:  
- **Verify that the correct time is being read from the RTC**.  
- **Check if button presses are detected**.  
- **Detect if the servo is moving properly**.  

### **How to Open the Serial Monitor**
1. **Connect your Arduino to your computer using a USB cable**.  
2. **Open the Arduino IDE**.  
3. Click on **Tools > Port**, and select the correct port (e.g., `COM3` on Windows, `/dev/ttyUSB0` on Linux/Mac).  
4. Click on **Tools > Serial Monitor** (or press `Ctrl + Shift + M`).  
5. Set the **baud rate to `9600`** (bottom-right corner of the Serial Monitor).  

Now, the Serial Monitor will start **showing messages from the system**.



### **Checking if the RTC Time is Correct**
If the time displayed on the OLED screen is incorrect, check the Serial Monitor. It will print:
```
Time now: 2025-02-27 14:35:12
```
If the time is incorrect, follow the **RTC setting instructions (Section 4)** to fix it.


                          
### **Checking Button Presses**
When a button is pressed, the Serial Monitor will show messages like:
```
Button 1 pressed
Button 2 pressed
Button 3 pressed
Button 4 pressed
```
If pressing a button **does not print anything**, check:
- If the **button is wired correctly**.  
- If the **button is physically working**.  
- If the **button pull-up resistor is enabled** in the code (`pinMode(BUTTON_X, INPUT_PULLUP);`).  



### **Checking if the Servo is Moving**
When the servo operates, the Serial Monitor will print:
```
Triggering Feeding A...
Triggering Feeding B...
Triggering Feeding Both...
```
If you **don’t see these messages** when feeding should occur:
- The **servo may not be connected properly**.  
- The **servo pin configuration** (lines 99-100) may be incorrect.  

