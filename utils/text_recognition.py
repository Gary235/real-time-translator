import numpy
import cv2
import pytesseract
from pytesseract import Output
from langdetect import detect
from googletrans import Translator

from utils.image import get_grayscale
from enums import Colors, LanguageAcronyms


TOP_RANGE = 7
BLOCK_PADDING = 5
font = cv2.FONT_HERSHEY_PLAIN
font_scale = 1

translator = Translator(service_urls=['translate.googleapis.com'])


def get_sentence_by_top(top, sentences):
	if sentences.get(top, False):
		return sentences.get(top, None)

	for i in range(top - TOP_RANGE, top + TOP_RANGE):
		if sentences.get(i, False):
			return sentences.get(i, None)

	return None

def group_sentences(image_data, sentences):
	n_boxes = len(image_data['text'])
	for i in range(n_boxes):
		if int(image_data['conf'][i]) <= 60:
			continue

		current_top = image_data['top'][i]
		current_sentence = get_sentence_by_top(current_top, sentences)

		if current_sentence:
			# So that we account for the spaces between words
			left_diff = image_data['left'][i] - (image_data['left'][i - 1] + image_data['width'][i - 1])

			current_sentence['text'].append(image_data['text'][i])
			current_sentence['width'] += image_data['width'][i] + left_diff

		elif image_data['text'][i]:
			sentences[current_top] = {}
			sentences[current_top]['height'] = image_data['height'][i] + BLOCK_PADDING
			sentences[current_top]['left'] = image_data['left'][i] - BLOCK_PADDING
			sentences[current_top]['width'] = image_data['width'][i] + BLOCK_PADDING
			sentences[current_top]['text'] = [image_data['text'][i]]

def detect_language(text):
	try:
		language = detect(text)
	except:
		language = LanguageAcronyms.AUTO.value

	return language

def put_text_in_place(sentence, translated_text, image_array, top):
	(translated_w, translated_h), _ = cv2.getTextSize(translated_text, font, font_scale, thickness=1)
	(x, y, w, h) = (sentence['left'], top - BLOCK_PADDING, sentence['width'], sentence['height'])

	# There may be differences of width/height between the original and translated text
	width = max(w, translated_w)
	height = max(h, translated_h)

	image_array = cv2.rectangle(
		image_array,
		(x, y),
		(x + width, y + height),
		Colors.BLACK.value,
		cv2.FILLED
	)
	image_array = cv2.putText(
		image_array,
		translated_text,
		(x, y + height),
		font,
		font_scale,
		Colors.WHITE.value,
		thickness=1
	)

def translate(sentences, image_array):
	for top, sentence in sentences.items():
		sentence_text = " ".join(sentence["text"])
		if not sentence_text:
			continue

		language = detect_language(sentence_text)
		if language != LanguageAcronyms.SPANISH.value:
			sentence_text = (translator
		    .translate(sentence_text, LanguageAcronyms.SPANISH.value, language)
				.text
			)

		put_text_in_place(sentence, sentence_text, image_array, top)


# --------------------------------------------------------------------------


def recognize_and_translate(processed_image, image_array):
	sentences = {}

	processed_image = get_grayscale(numpy.array(processed_image))
	image_data = pytesseract.image_to_data(
		processed_image,
		config='-l eng+spa+jpn --psm 6',
		output_type=Output.DICT
	)

	group_sentences(image_data, sentences)
	translate(sentences, image_array)

	return image_array
