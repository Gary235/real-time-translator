import cv2
import mss
import numpy
from PIL import Image

from utils.text_recognition import recognize_and_translate


class ScreenCapture:
	def __init__(self):
		self.monitor = {"top": 100, "left": 220, "width": 650, "height": 450}

		self.width = self.monitor.get('width')
		self.height = self.monitor.get('height')

	def get_shot(self):
		with mss.mss() as screenshot:
			self.shot = numpy.array(screenshot.grab(self.monitor))
			image = Image.frombytes(
				'RGB',
				(self.width, self.height),
				screenshot.grab(self.monitor).rgb,
				'raw'
			)
			self.shot = recognize_and_translate(image, self.shot)

		return cv2.cvtColor(self.shot, cv2.COLOR_BGR2RGB)
