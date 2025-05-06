from gpiozero import DigitalOutputDevice
import time
import boto3
from datetime import datetime

# Updated GPIO Pin Assignments for TM1638
STB = DigitalOutputDevice(17)  # GPIO17, Pin 11 - Latch
CLK = DigitalOutputDevice(27)  # GPIO27, Pin 13 - Clock
DIO = DigitalOutputDevice(22)  # GPIO22, Pin 15 - Data

# Segment data for digits 0-9 (common cathode format)
NUMBERS = {
    0: 0x3F,
    1: 0x06,
    2: 0x5B,
    3: 0x4F,
    4: 0x66,
    5: 0x6D,
    6: 0x7D,
    7: 0x07,
    8: 0x7F,
    9: 0x6F
}

def shift_out(byte):
    for i in range(8):
        CLK.off()
        DIO.value = (byte >> i) & 1
        CLK.on()

def send_command(cmd):
    STB.off()
    shift_out(cmd)
    STB.on()

def set_digit(address, data):
    send_command(0x44)  # Fixed address mode
    STB.off()
    shift_out(0xC0 + address)
    shift_out(data)
    STB.on()

def set_display_on():
    send_command(0x8F)  # Display ON + brightness max

def display_number(num):
    set_display_on()
    # Clear all 8 digits
    for i in range(8):
        set_digit(i, 0x00)
    if num in NUMBERS:
        set_digit(0, NUMBERS[num])  # Display on first digit (address 0)

def log_to_dynamodb(number):
    try:
        dynamodb = boto3.resource('dynamodb',
            region_name='us-east-2',
            aws_access_key_id='', # removed for now because github doesnt like it
            aws_secret_access_key='') # removed for now because github doesnt like it

        table = dynamodb.Table('segment_display_logs')

        table.put_item(
            Item={
                'timestamp': datetime.now().isoformat(),
                'number': number,
                'display_pattern': hex(NUMBERS[number])
            }
        )
    except Exception as e:
        print(f"DynamoDB Error: {str(e)}")

def main():
    set_display_on()
    while True:
        for n in [1, 2, 3, 4, 5]:
            display_number(n)
            log_to_dynamodb(n)
            time.sleep(1)

if __name__ == "__main__":
    main()
