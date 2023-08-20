import tkinter
from PIL import Image, ImageTk

from classes.screen_capture import ScreenCapture

class App:
	def __init__(self, window, window_title):
		self.window = window
		self.window.title(window_title)

		# open video source (by default this will try to open the computer webcam)
		self.screen = ScreenCapture()

		# Create a canvas that can fit the above video source size
		self.canvas = tkinter.Canvas(window, width=self.screen.width, height=self.screen.height)
		self.canvas.pack()

		# After it is called once, the update method will be automatically called every delay milliseconds
		self.delay = 500
		self.update()

		self.window.mainloop()

	def update(self):
		# Get a frame from the video source
		shot = self.screen.get_shot()

		self.photo = ImageTk.PhotoImage(image=Image.fromarray(shot))
		self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

		self.window.after(self.delay, self.update)

App(tkinter.Tk(), "Real Time Translator")
