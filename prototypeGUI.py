from tkinter import *

class Application(Frame): #child class of Frame
	def __init__(self, master):
		super(Application, self).__init__(master)
		self.grid()
		self.create_widgets()
	#second part, creating widgets, uses grid system. 
	#grids start at (0,0)
	def create_widgets(self):
		self.label1 = Label(self, text = "Temperature")
		self.label1.grid(row = 0, column = 3, sticky = W) #how to assigne widget to cell
		# for the celsius temperature
		self.CelLabel = Label(self, text = "24 C") #fake values
		self.CelLabel.grid(row=1, column=3, sticky=W)
		#for the farhenhiet temperature
		self.FarLabel = Label(self, text = "72.5 F") #fake values
		self.FarLabel.grid(row=1, column=4, sticky=W)
		#for the cooling agent to dispense?
		self.CoolButton = Button(self, text="Lower ", command=self.LowerTemp)
		self.CoolButton.grid(row= 3, column= 3, sticky=W)
		#
	
	def LowerTemp(self):
		print("temperature lowered")
		#actual logic for lowering (turn on fake fan) below.

root = Tk()
root.title("Prototype GUI")
root.geometry('800x400')
app = Application(root)
app.mainloop()
