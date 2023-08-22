import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import numpy

from classes.screen_capture import ScreenCapture

def validate_entry(text):
    return text.isdecimal()

class App:
	def __init__(self, window, window_title):
		self.window = window
		self.window.title(window_title)
		self.window.config(bg='#242424')

		self.delay = 500
		self.screen = None
		self._job = None
		self.shot = None

		self.frame = tkinter.Frame(self.window, bg='#242424')
		self.frame.pack(padx=20, pady=20)

		self.top_var = tkinter.StringVar(value='100')
		self.left_var = tkinter.StringVar(value='220')
		self.width_var = tkinter.StringVar(value='650')
		self.height_var = tkinter.StringVar(value='450')
		self.top_entry = ttk.Entry(self.frame, textvariable=self.top_var, validate="key", validatecommand=(self.window.register(validate_entry), "%S"))
		self.left_entry = ttk.Entry(self.frame, textvariable=self.left_var, validate="key", validatecommand=(self.window.register(validate_entry), "%S"))
		self.width_entry = ttk.Entry(self.frame, textvariable=self.width_var, validate="key", validatecommand=(self.window.register(validate_entry), "%S"))
		self.height_entry = ttk.Entry(self.frame, textvariable=self.height_var, validate="key", validatecommand=(self.window.register(validate_entry), "%S"))

		self.top_var.trace('w', self.on_entry_trace)
		self.left_var.trace('w', self.on_entry_trace)
		self.width_var.trace('w', self.on_entry_trace)
		self.height_var.trace('w', self.on_entry_trace)

		tkinter.Label(self.frame, text='top', fg='#f0f0f0', background='#242424').grid(column=0, row=0)
		self.top_entry.grid(column=0, row=1)
		tkinter.Label(self.frame, text='left', fg='#f0f0f0', background='#242424').grid(column=0, row=2)
		self.left_entry.grid(column=0, row=3)
		tkinter.Label(self.frame, text='width', fg='#f0f0f0', background='#242424').grid(column=0, row=4)
		self.width_entry.grid(column=0, row=5)
		tkinter.Label(self.frame, text='height', fg='#f0f0f0', background='#242424').grid(column=0, row=6)
		self.height_entry.grid(column=0, row=7)

		self.start_button = tkinter.Button(self.frame, text='Run', command=self.update_capture, border=0, borderwidth=0)
		self.start_button.grid(column=0, row=8, pady=10)
		self.stop_button = tkinter.Button(self.frame, text='Stop', command=self.stop_capture, border=0, borderwidth=0)
		self.stop_button.grid(column=0, row=9)

		self.canvas = tkinter.Canvas(self.frame, width=650, height=450, background='#f7f7f7', bd=0)
		self.canvas.grid(column=1, row=0, rowspan=14, padx=20)

		self.window.mainloop()

	def on_entry_trace(self, varname, elementname, mode):
		if all([self.top_var.get(), self.left_var.get(), self.width_var.get(), self.height_var.get()]):
			self.start_button.config(state=tkinter.ACTIVE)
		else:
			self.start_button.config(state=tkinter.DISABLED)

	def stop_capture(self):
		if self._job is not None:
			self.window.after_cancel(self._job)
			self._job = None
			self.screen = None
			self.canvas.config(background='#d40f3d')

	def update_capture(self):
		if not self.screen:
			self.canvas.config(width=int(self.width_var.get()) + 8, height=int(self.height_var.get()) + 8)
			self.screen = ScreenCapture(
				top=int(self.top_var.get()),
				left=int(self.left_var.get()),
				width=int(self.width_var.get()),
				height=int(self.height_var.get()),
			)

		self.canvas.config(background='#0fd430')
		new_shot = self.screen.get_shot()
		if self.shot is None or not numpy.array_equal(self.shot, new_shot):
			self.shot = new_shot
			self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.shot))
			self.canvas.create_image(5, 5, image=self.photo, anchor=tkinter.NW)

		# After it is called once, the update method will be automatically called every delay milliseconds
		self._job = self.window.after(self.delay, self.update_capture)

App(tkinter.Tk(), "Real Time Translator")
