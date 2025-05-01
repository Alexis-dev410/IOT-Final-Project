from tkinter import *
#samantha jones
class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.language = 'en'  # Default language
        self.translations = {
            'en': {
                'title': 'Temperature',
                'celsius': 'C',
                'fahrenheit': 'F',
                'lower': 'Lower',
                'english': 'English',
                'french': 'French'
            },
            'fr': {
                'title': 'Temperature',
                'celsius': 'C',
                'fahrenheit': 'F',
                'lower': 'Diminuer',
                'english': 'Anglais',
                'french': 'Francais'
            }
        }
        self.temperature_c = 24  # Initial temperature
        self.create_widgets()

    def create_widgets(self):
        

        # Labels and button
        self.label1 = Label(self)
        self.label1.grid(row=1, column=1, sticky=W)

        self.CelLabel = Label(self)
        self.CelLabel.grid(row=2, column=1, sticky=W)

        self.FarLabel = Label(self)
        self.FarLabel.grid(row=2, column=2, sticky=W)

        self.CoolButton = Button(self, command=self.LowerTemp)
        self.CoolButton.grid(row=4, column=0, padx=5, pady=5, sticky=W)

        # Language selection buttons
        self.english_btn = Button(self, text="English", command=lambda: self.set_language('en'))
        self.english_btn.grid(row=5, column=0, padx=5, pady=5, sticky=W)

        self.french_btn = Button(self, text="French", command=lambda: self.set_language('fr'))
        self.french_btn.grid(row=5, column=1, padx=5, pady=5, sticky=W)
        self.update_labels()

    def update_labels(self):
        t = self.translations[self.language]
        self.label1["text"] = t['title']
        self.CelLabel["text"] = f"{self.temperature_c} {t['celsius']}"
        self.FarLabel["text"] = f"{self.celsius_to_fahrenheit(self.temperature_c):.1f} {t['fahrenheit']}"
        self.CoolButton["text"] = t['lower']
        self.english_btn["text"] = t['english']
        self.french_btn["text"] = t['french']

    def set_language(self, lang_code):
        self.language = lang_code
        self.update_labels()

    def LowerTemp(self):
        self.temperature_c -= 1
        self.update_labels()
        print("temperature lowered")

    @staticmethod
    def celsius_to_fahrenheit(c):
        return c * 9 / 5 + 32

root = Tk()
root.title("Prototype GUI")
root.geometry('800x400')
app = Application(root)
app.mainloop()
