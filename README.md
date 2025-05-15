Smart IoT Ice Dispenser – User Manual
Overview
The Smart IoT Dispenser is a bilingual, temperature-based automation system designed to open a micro servo-controlled gate when the internal temperature drops below a user-defined threshold. It also includes a segment display to show current temperature and a physical button for manual activation.
________________________________________
🛠️ Components
•	Raspberry Pi with GPIO Extension Board
•	DS18B20 Temperature Sensor
•	SG90 Micro Servo Motor
•	TM1638 Segment Display
•	Physical Push Button
•	Limit Switch
•	GUI-based Controller (Tkinter)
________________________________________
 

🔌 Wiring Guide
Component	Signal Pin	GPIO Pin #	Physical Pin #
Temperature Sensor	Data	GPIO4	Pin 7
Segment Display	DIO	GPIO27	Pin 13
Segment Display	CLK	GPIO22	Pin 15
Segment Display	STB	GPIO23	Pin 16
Segment Display	VCC / GND	3.3V / GND	Pin 1 / 14
Micro Servo	Signal	GPIO17	Pin 11
Limit Switch	Signal	GPIO18	Pin 12
Physical Button	Signal	GPIO25	Pin 22
________________________________________
🧑‍💻 GUI Instructions
1. Launch the App
To start the application by running the command "python3 multilingual.py".
Make sure pigpiod is running with the command "sudo pigpiod".
2. View Temperature
The main display shows the current temperature in Celsius and Fahrenheit.
3. Set Threshold
•	Use + / – buttons to raise or lower the target temperature.
•	Use the "Set Target Temp" field and click the apply button.
 

4. Dispense Ice (Open Servo Door)
•	Click the “Dispense Ice” button in the GUI
•	Or press the physical hardware button
•	The ice will automatically dispense if the temperature goes below the set value
5. Language Selection
•	Use the "English" or "Français" buttons to switch the interface language.

