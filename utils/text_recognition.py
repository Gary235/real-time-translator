import numpy
import cv2
import pytesseract
from pytesseract import Output
from langdetect import detect

from utils.image import get_grayscale
from googletrans import Translator
from enums import Colors, LanguageAcronyms


TOP_RANGE = 7
BLOCK_PADDING = 5
font = cv2.FONT_HERSHEY_PLAIN
font_scale = 1

translator = Translator(service_urls=['translate.googleapis.com'])

def box_sentences(image, image_array):
  sentences = {}

  image = get_grayscale(numpy.array(image))
  image_data = pytesseract.image_to_data(image, config='-l eng+spa+jpn --psm 6', output_type=Output.DICT)

  def get_sentence(top):
    if sentences.get(top, False):
      return sentences.get(top, None)

    for i in range(top - TOP_RANGE, top + TOP_RANGE):
      if sentences.get(i, False):
        return sentences.get(i, None)

    return None

  n_boxes = len(image_data['text'])
  for i in range(n_boxes):
    if int(image_data['conf'][i]) <= 60:
      continue

    # previous_top = image_data['top'][i - 1] if i > 0 else None
    # change_in_top = previous_top != current_top and previous_top != None

    current_top = image_data['top'][i]
    current_sentence = get_sentence(current_top)

    if current_sentence:
      left_diff = image_data['left'][i] - (image_data['left'][i - 1] + image_data['width'][i - 1])

      current_sentence['text'].append(image_data['text'][i])
      current_sentence['width'] += image_data['width'][i] + left_diff

    elif image_data['text'][i]:
      sentences[current_top] = {}
      sentences[current_top]['height'] = image_data['height'][i] + BLOCK_PADDING
      sentences[current_top]['left'] = image_data['left'][i] - BLOCK_PADDING
      sentences[current_top]['width'] = image_data['width'][i] + BLOCK_PADDING
      sentences[current_top]['text'] = [image_data['text'][i]]

  for top, sentence in sentences.items():
    sentence_text = " ".join(sentence["text"])
    if not sentence_text:
      continue

    try:
      language = detect(sentence_text)
    except:
      language = LanguageAcronyms.AUTO.value

    if language != LanguageAcronyms.SPANISH.value:
      sentence_text = translator.translate(sentence_text, dest=LanguageAcronyms.SPANISH.value).text

    text_size, _ = cv2.getTextSize(sentence_text, font, font_scale, 1)
    text_w, text_h = text_size
    (x, y, w, h) = (sentence['left'], top - BLOCK_PADDING, sentence['width'], sentence['height'])

    width = max(w, text_w)
    height = max(h, text_h)

    image_array = cv2.rectangle(
      image_array,
      (x, y),
      (x + width, y + height),
      Colors.BLACK.value,
      cv2.FILLED
    )
    image_array = cv2.putText(
      image_array,
      sentence_text,
      (x, y + height),
      font,
      font_scale,
      Colors.WHITE.value,
      thickness=1
    )

  return image_array
