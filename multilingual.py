from tkinter import *
from gpiozero import Button as GPIOButton, Servo, DigitalOutputDevice
import temperature  # Your existing DS18B20 script
import time
import threading
import os
import signal

# GPIO Assignments
LIMIT_SWITCH = GPIOButton(18, pull_up=False, bounce_time=0.1)  # GPIO18 - Emergency stop
MANUAL_BUTTON = GPIOButton(24, pull_up=True, bounce_time=0.1)  # GUI fallback
PHYSICAL_BUTTON = GPIOButton(25, pull_up=True, bounce_time=0.1)  # Physical dispense button
SERVO = Servo(17, initial_value=-1)  # GPIO17, start position

# TM1638 Segment Display Pins
STB = DigitalOutputDevice(23)
CLK = DigitalOutputDevice(22)
DIO = DigitalOutputDevice(27)

SEGMENT_DIGITS = [
    0b00111111,  # 0
    0b00000110,  # 1
    0b01011011,  # 2
    0b01001111,  # 3
    0b01100110,  # 4
    0b01101101,  # 5
    0b01111101,  # 6
    0b00000111,  # 7
    0b01111111,  # 8
    0b01101111   # 9
]

def _shift_out(data):
    for i in range(8):
        bit = (data >> i) & 1
        DIO.value = bit
        CLK.off()
        time.sleep(0.00001)
        CLK.on()
        time.sleep(0.00001)

def send_command(cmd):
    STB.off()
    _shift_out(cmd)
    STB.on()

def setup_segment_display():
    send_command(0x8F)  # Display on
    send_command(0x40)  # Auto-increment mode

def display_temperature(value):
    try:
        setup_segment_display()
        val = int(round(value * 100))
        digits = [int(d) for d in f"{val:04d}"]
        STB.off()
        _shift_out(0xC0)
        _shift_out(SEGMENT_DIGITS[digits[0]])
        _shift_out(0x00)
        _shift_out(SEGMENT_DIGITS[digits[1]])
        _shift_out(0x00)
        _shift_out(SEGMENT_DIGITS[digits[2]] | 0x80)
        _shift_out(0x00)
        _shift_out(SEGMENT_DIGITS[digits[3]])
        _shift_out(0x00)
        STB.on()
    except Exception as e:
        print(f"[Segment Error] {e}")

def clear_segment_display():
    STB.off()
    _shift_out(0xC0)
    for _ in range(8):
        _shift_out(0x00)
        _shift_out(0x00)
    STB.on()

class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(padx=20, pady=20)
        self.language = 'en'
        self.temperature_c = 0.0
        self.target_temp = 23.0
        self.servo_open = False

        self.translations = {
            'en': {
                'title': 'Temperature',
                'celsius': 'C',
                'fahrenheit': 'F',
                'lower': '-',
                'higher': '+',
                'english': 'English',
                'french': 'French',
                'set_temp': 'Set Target Temp',
                'dispense': 'Dispense Ice',
                'threshold': 'Threshold'
            },
            'fr': {
                'title': 'Température',
                'celsius': 'C',
                'fahrenheit': 'F',
                'lower': '-',
                'higher': '+',
                'english': 'Anglais',
                'french': 'Français',
                'set_temp': 'Définir Temp Cible',
                'dispense': 'Distribuer Glace',
                'threshold': 'Seuil'
            }
        }

        temperature.setup()
        self.create_widgets()
        self.poll_temperature()
        self.check_manual_button()

    def create_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        t = self.translations[self.language]

        self.temp_display = Label(self, text="-- °C / -- °F", font=("Helvetica", 24))
        self.temp_display.grid(row=0, column=0, columnspan=3, pady=10)

        self.status_label = Label(self, text="", font=("Helvetica", 14))
        self.status_label.grid(row=1, column=0, columnspan=3)

        self.cool_button = Button(self, text=t['dispense'], font=("Helvetica", 14), command=self.activate_servo, width=20)
        self.cool_button.grid(row=2, column=0, columnspan=3, pady=10)

        self.threshold_display = Label(self, text=f"{t['threshold']}: {self.target_temp:.1f} °C", font=("Helvetica", 14))
        self.threshold_display.grid(row=3, column=0, columnspan=3)

        self.setLowerButton = Button(self, text=t['lower'], width=5, command=self.setLower)
        self.setLowerButton.grid(row=4, column=0)

        self.setHigherButton = Button(self, text=t['higher'], width=5, command=self.setHigher)
        self.setHigherButton.grid(row=4, column=2)

        self.setpoint_entry = Entry(self, width=5)
        self.setpoint_entry.grid(row=5, column=0)

        self.set_btn = Button(self, text=t['set_temp'], command=self.update_target_temp)
        self.set_btn.grid(row=5, column=1, columnspan=2)

        self.english_btn = Button(self, text=t['english'], command=lambda: self.set_language('en'), width=10)
        self.english_btn.grid(row=6, column=0, pady=10)

        self.french_btn = Button(self, text=t['french'], command=lambda: self.set_language('fr'), width=10)
        self.french_btn.grid(row=6, column=2, pady=10)

    def update_labels(self):
        t = self.translations[self.language]
        self.cool_button.config(text=t['dispense'])
        self.setLowerButton.config(text=t['lower'])
        self.setHigherButton.config(text=t['higher'])
        self.set_btn.config(text=t['set_temp'])
        self.english_btn.config(text=t['english'])
        self.french_btn.config(text=t['french'])
        self.threshold_display.config(text=f"{t['threshold']}: {self.target_temp:.1f} °C")

    def set_language(self, lang_code):
        self.language = lang_code
        self.create_widgets()
        self.update_labels()

    def setLower(self):
        self.target_temp -= 1
        self.update_labels()

    def setHigher(self):
        self.target_temp += 1
        self.update_labels()

    def update_target_temp(self):
        try:
            self.target_temp = float(self.setpoint_entry.get())
            self.update_labels()
        except ValueError:
            pass

    def poll_temperature(self):
        temp_c, temp_f = temperature.read_temperature()
        if temp_c is not None:
            self.temperature_c = temp_c
            self.temp_display.config(text=f"{temp_c:.2f} °C / {self.celsius_to_fahrenheit(temp_c):.2f} °F")
            display_temperature(temp_c)
            if temp_c < self.target_temp and not LIMIT_SWITCH.is_pressed:
                self.status_label.config(text="Cooling...")
                self.activate_servo()
            else:
                self.status_label.config(text="")
        else:
            self.temp_display.config(text="Error reading sensor")
        self.after(2000, self.poll_temperature)

    def check_manual_button(self):
        if (MANUAL_BUTTON.is_pressed or PHYSICAL_BUTTON.is_pressed) and not LIMIT_SWITCH.is_pressed:
            self.activate_servo()
        self.after(200, self.check_manual_button)

    def activate_servo(self):
        if self.servo_open or LIMIT_SWITCH.is_pressed:
            return
        self.servo_open = True
        threading.Thread(target=self.open_and_close_servo).start()

    def open_and_close_servo(self):
        for v in range(-100, 101):
            if LIMIT_SWITCH.is_pressed:
                break
            SERVO.value = v / 100
            time.sleep(0.04)
        time.sleep(5)
        for v in reversed(range(-100, 101)):
            if LIMIT_SWITCH.is_pressed:
                break
            SERVO.value = v / 100
            time.sleep(0.04)
        SERVO.value = -1
        self.servo_open = False

    @staticmethod
    def celsius_to_fahrenheit(c):
        return c * 9 / 5 + 32

def on_exit():
    print("Shutting down, clearing display...")
    clear_segment_display()
    root.destroy()

root = Tk()
root.title("Temperature Controller")
root.geometry('400x400')
app = Application(root)
root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()
