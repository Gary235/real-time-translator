import cv2
import numpy
import mss
from PIL import Image

from utils.text_recognition import recognize_and_translate

with mss.mss() as screenshot:
	# Part of the screen to capture
	monitor = {"top": 100, "left": 220, "width": 900, "height": 640}

	lasting_image = numpy.array(screenshot.grab(monitor))
	while "Screen capturing":
		image_array = numpy.array(screenshot.grab(monitor))

		if not numpy.array_equal(lasting_image, image_array):
			lasting_image = image_array
			image = Image.frombytes(
				'RGB',
				(monitor.get('width'), monitor.get('height')),
				screenshot.grab(monitor).rgb,
				'raw'
			)
			image_array = recognize_and_translate(image, image_array)

		cv2.imshow("OpenCV/Numpy normal", image_array)

		# Press "q" to quit
		if cv2.waitKey(25) & 0xFF == ord("q"):
			cv2.destroyAllWindows()
			break
