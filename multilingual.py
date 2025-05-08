from tkinter import *
import temperature  # Your existing sensor code
import RPi.GPIO as GPIO

class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()

        # Default settings
        self.language = 'en'
        self.temperature_c = 0.0
        self.target_temp = 26.0

        # GPIO setup
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)
        # self.SERVO_PIN = 17
        # GPIO.setup(self.SERVO_PIN, GPIO.OUT)
        # self.servo_pwm = GPIO.PWM(self.SERVO_PIN, 50)
        # self.servo_pwm.start(0)

        # Init sensor
        temperature.setup()

        # Language translations
        self.translations = {
            'en': {
                'title': 'Temperature',
                'celsius': 'C',
                'fahrenheit': 'F',
                'lower': 'Lower',
                'higher': 'Raise',
                'english': 'English',
                'french': 'French',
                'set_temp': 'Set Target Temp'
            },
            'fr': {
                'title': 'Temperature',
                'celsius': 'C',
                'fahrenheit': 'F',
                'lower': 'Diminuer',
                'higher': 'Augmenter',
                'english': 'Anglais',
                'french': 'Francais',
                'set_temp': 'Definir Temp Cible'
            }
        }

        self.create_widgets()
        self.poll_temperature()

    
    def create_widgets(self):
        # Labels for title and temperature
        self.label1 = Label(self)
        self.label1.grid(row=1, column=1, sticky=W)

        self.CelLabel = Label(self)
        self.CelLabel.grid(row=2, column=1, sticky=W)

        self.FarLabel = Label(self)
        self.FarLabel.grid(row=2, column=2, sticky=W)

        # Fan control buttons (optional, manual control)
        self.CoolButton = Button(self, command=self.LowerTemp)
        self.CoolButton.grid(row=4, column=0, padx=5, pady=5, sticky=W)

        self.setLowerButton = Button(self, command=self.setLower)
        self.setLowerButton.grid(row=3, column=4, sticky=W)

        self.setHigherButton = Button(self, command=self.setHigher)
        self.setHigherButton.grid(row=4, column=4, sticky=W)

        # Language selection
        self.english_btn = Button(self, command=lambda: self.set_language('en'))
        self.english_btn.grid(row=5, column=0, padx=5, pady=5, sticky=W)

        self.french_btn = Button(self, command=lambda: self.set_language('fr'))
        self.french_btn.grid(row=5, column=1, padx=5, pady=5, sticky=W)

        # Setpoint input
        self.setpoint_entry = Entry(self)
        self.setpoint_entry.grid(row=6, column=0, sticky=W)
        self.set_btn = Button(self, command=self.update_target_temp)
        self.set_btn.grid(row=6, column=1, sticky=W)

        self.update_labels()

    def update_labels(self):
        t = self.translations[self.language]
        self.label1["text"] = t['title']
        self.CelLabel["text"] = f"{self.temperature_c:.2f} {t['celsius']}"
        self.FarLabel["text"] = f"{self.celsius_to_fahrenheit(self.temperature_c):.2f} {t['fahrenheit']}"
        self.CoolButton["text"] = t['lower']
        self.setLowerButton["text"] = t['lower']
        self.setHigherButton["text"] = t['higher']
        self.english_btn["text"] = t['english']
        self.french_btn["text"] = t['french']
        self.set_btn["text"] = t['set_temp']

    def set_language(self, lang_code):
        self.language = lang_code
        self.update_labels()

    def LowerTemp(self):
        self.temperature_c -= 1
        self.update_labels()
        print("Temperature lowered manually")

    def setLower(self):
        self.target_temp -= 1
        print(f"Target temperature lowered to {self.target_temp}")

    def setHigher(self):
        self.target_temp += 1
        print(f"Target temperature raised to {self.target_temp}")

    def update_target_temp(self):
        try:
            self.target_temp = float(self.setpoint_entry.get())
            print(f"Target temperature set to {self.target_temp}")
        except ValueError:
            print("Invalid temperature entered")

    # def set_servo_angle(self, angle):
            # duty = 2 + (angle / 18)  # Convert angle (0-180) to duty cycle
            # GPIO.output(self.SERVO_PIN, True)
            # self.servo_pwm.ChangeDutyCycle(duty)
            # time.sleep(0.5)
            # GPIO.output(self.SERVO_PIN, False)
            # self.servo_pwm.ChangeDutyCycle(0)
    
    def poll_temperature(self):
        temp_c, temp_f = temperature.read_temperature()
        if temp_c is not None:
            self.temperature_c = temp_c
            self.update_labels()

            # Fan logic
            if temp_c > self.target_temp:
               # self.set_servo_angle(90)  # Fan ON
               print("fan on")
               
            else:
                #self.set_servo_angle(0) 
                print("fan off")
        else:
            print("Temperature read failed")

        self.after(2000, self.poll_temperature)  # Poll every 2 seconds

    @staticmethod
    def celsius_to_fahrenheit(c):
        return c * 9 / 5 + 32


# Run the GUI
root = Tk()
root.title("Temperature Controller")
root.geometry('800x400')
app = Application(root)
app.mainloop()

# Cleanup GPIO on close
GPIO.cleanup()
