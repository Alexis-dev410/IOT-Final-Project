from tkinter import *

class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.label1 = Label(self, text="Temperature")
        self.label1.grid(row=0, column=3, sticky=W)

        # for the Celsius temperature
        self.CelLabel = Label(self, text="24 C")
        self.CelLabel.grid(row=1, column=3, sticky=W)

        # for the Fahrenheit temperature
        self.FarLabel = Label(self, text="75.2 F")
        self.FarLabel.grid(row=1, column=4, sticky=W)

        # cooling button
        self.CoolButton = Button(self, text="Lower", command=self.LowerTemp)
        self.CoolButton.grid(row=3, column=3, sticky=W)

    def LowerTemp(self):
        current_c = int(self.CelLabel["text"].split()[0])
        new_c = current_c - 1
        new_f = new_c * 9 / 5 + 32

        self.CelLabel["text"] = f"{new_c} C"
        self.FarLabel["text"] = f"{new_f:.1f} F"

root = Tk()
root.title("Prototype GUI")
root.geometry('800x400')
app = Application(root)
app.mainloop()
