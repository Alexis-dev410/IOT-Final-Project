import os
import glob
import time

# Load necessary kernel modules for 1-Wire communication
def setup():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    try:
        device_folder = glob.glob(base_dir + '28*')[0]  # Find the sensor folder
        global device_file
        device_file = device_folder + '/w1_slave'  # Path to sensor data file
    except IndexError:
        print("Error: DS18B20 sensor not found. Ensure it is connected properly.")
        exit(1)  # Exit if sensor is not detected

# Read raw temperature data from sensor
def read_file():
    try:
        with open(device_file, 'r') as f:
            lines = f.readlines()
        return lines
    except FileNotFoundError:
        print("Error: Sensor device file not found.")
        return None

# Extract temperature from raw data
def read_temperature():
    lines = read_file()
    
    if lines is None:  # Check if data is available
        return None, None

    try:
        while lines[0].strip()[-3:] != 'YES':  # Wait for valid data
            time.sleep(0.2)
            lines = read_file()
            if lines is None:
                return None, None

        temp_pos = lines[1].find('t=')
        if temp_pos != -1:
            temp_string = lines[1][temp_pos+2:]
            temp_celsius = round(float(temp_string) / 1000.0, 2)
            temp_fahrenheit = round(temp_celsius * 9.0 / 5.0 + 32.0, 2)
            return temp_celsius, temp_fahrenheit
    except (IndexError, ValueError) as e:
        print(f"Error reading temperature data: {e}")
        return None, None

# Loop to continuously read temperature data
def loop():
    while True:
        temp_c, temp_f = read_temperature()
        if temp_c is not None and temp_f is not None:
            print(f"Temperature: {temp_c}C / {temp_f}F")
        else:
            print("Skipping invalid reading...")
        time.sleep(2)  # Read temperature every 2 seconds

# Main execution
if __name__ == '__main__':
    print("Press Ctrl+C to end the program...")
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        print("\nProgram terminated. Bye!")
