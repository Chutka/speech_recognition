import os
import sys
import argparse
import speech_recognition as sr

from recognizer.recognizer import RecognizerTypes, Recognizer

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone(device_index=0) as source:
    print("Say something!")
    audio = r.listen(source, timeout=2)

# recognize speech using Sphinx
try:
    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))


# if __name__ == '__main__':
  # ap = argparse.ArgumentParser()
  # ap.add_argument()
