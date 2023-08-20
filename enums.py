from enum import Enum

class LanguageAcronyms(Enum):
  SPANISH='es'
  ENGLISH='en'
  AUTO='auto'

class TesseractLanguageAcronyms(Enum):
  SPANISH='spa'
  ENGLISH='eng'
  JAPANESE='jpn'
  KOREAN='kor'

class Colors(Enum):
  WHITE=(240, 240, 240)
  BLACK=(20, 20, 20)
