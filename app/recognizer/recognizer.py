import speech_recognition as sr

from enum import Enum


class RecognizerTypes(Enum):
    SPHINX = 'Sphinx'
    GOOGLE_SPEECH_RECOGNITION = 'Google Speech Recognition'
    GOOGLE_CLOUD_SPEECH = 'Google Cloud Speech'
    WIT_AI_KEY = 'Wit.ai'
    MICROSOFT_BING_VOICE_RECOGNITION = 'Microsoft Bing Voice Recognition'
    HOUNDIFY = 'Houndify'
    IBM_SPEECH_TO_TEXT = 'IBM Speech to Text'


class Recognizer:
    def __init__(self, type, device_index=0):
        if not type:
            raise Exception('Should add type of recognizer')
        self.recognizer = sr.Recognizer()
        try:
            RecognizerTypes(type)
        except ValueError as vr:
            raise ValueError('Type is not correct', *vr.args)
        self.type = type
        if device_index is None:
            raise Exception('Device is not defined')
        self.device_index = device_index

    def listen(self):
        with sr.Microphone(device_index=self.device_index) as source:
            print('Начните что-то говорить')
            audio = self.recognizer.listen(source)
        print('Запись закончена')
        return audio

    def from_file(self, file_name):
        with sr.AudioFile(file_name) as source:
            print('Из аудио файла - {}'.format(file_name))
            audio = self.recognizer.record(source)
        print('Считывание закончено')
        return audio

    def recognition(self, audio, *args, **kwargs):
        begin_text = 'Распознавание ведется с помощью - {}'
        recognition_text = None
        if self.type == RecognizerTypes.SPHINX:
            print(begin_text.format(RecognizerTypes.SPHINX.value))
            recognition_text = self._sphrinx(audio, *args, **kwargs)
        if self.type == RecognizerTypes.GOOGLE_SPEECH_RECOGNITION:
            print(begin_text.format(RecognizerTypes.GOOGLE_SPEECH_RECOGNITION.value))
            recognition_text = self._google_speech(audio, *args, **kwargs)
        if self.type == RecognizerTypes.GOOGLE_CLOUD_SPEECH:
            print(begin_text.format(RecognizerTypes.GOOGLE_CLOUD_SPEECH.value))
            recognition_text = self._google_cloud_speech(audio, *args, **kwargs)
        if self.type == RecognizerTypes.WIT_AI_KEY:
            print(begin_text.format(RecognizerTypes.WIT_AI_KEY.value))
            recognition_text = self._wit_ai_key(audio, *args, **kwargs)
        if self.type == RecognizerTypes.MICROSOFT_BING_VOICE_RECOGNITION:
            print(begin_text.format(RecognizerTypes.MICROSOFT_BING_VOICE_RECOGNITION.value))
            recognition_text = self._microsoft_bing(audio, *args, **kwargs)
        if self.type == RecognizerTypes.HOUNDIFY:
            print(begin_text.format(RecognizerTypes.HOUNDIFY.value))
            recognition_text = self._houndify(audio, *args, **kwargs)
        if self.type == RecognizerTypes.IBM_SPEECH_TO_TEXT:
            print(begin_text.format(RecognizerTypes.IBM_SPEECH_TO_TEXT.value))
            recognition_text = self._ibm(audio, *args, **kwargs)
        return recognition_text

    def _sphrinx(self, audio):
        # recognize speech using Sphinx
        try:
            return self.recognizer.recognize_sphinx(audio)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

    def _google_speech(self, audio):
        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def _google_cloud_speech(self, audio):
        # recognize speech using Google Cloud Speech
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""INSERT THE CONTENTS OF THE GOOGLE CLOUD SPEECH JSON CREDENTIALS FILE HERE"""
        try:
            return self.recognizer.recognize_google_cloud(audio,
                                                          credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        except sr.UnknownValueError:
            print("Google Cloud Speech could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech service; {0}".format(e))

    def _wit_ai_key(self, audio):
        # recognize speech using Wit.ai
        WIT_AI_KEY = "INSERT WIT.AI API KEY HERE"  # Wit.ai keys are 32-character uppercase alphanumeric strings
        try:
            return self.recognizer.recognize_wit(audio, key=WIT_AI_KEY)
        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))

    def _microsoft_bing(self, audio):
        # recognize speech using Microsoft Bing Voice Recognition
        BING_KEY = "INSERT BING API KEY HERE"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
        try:
            return self.recognizer.recognize_bing(audio, key=BING_KEY)
        except sr.UnknownValueError:
            print("Microsoft Bing Voice Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

    def _houndify(self, audio):
        # recognize speech using Houndify
        HOUNDIFY_CLIENT_ID = "INSERT HOUNDIFY CLIENT ID HERE"  # Houndify client IDs are Base64-encoded strings
        HOUNDIFY_CLIENT_KEY = "INSERT HOUNDIFY CLIENT KEY HERE"  # Houndify client keys are Base64-encoded strings
        try:
            return self.recognizer.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY)
        except sr.UnknownValueError:
            print("Houndify could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Houndify service; {0}".format(e))

    def _ibm(self, audio):
        # recognize speech using IBM Speech to Text
        IBM_USERNAME = "INSERT IBM SPEECH TO TEXT USERNAME HERE"  # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        IBM_PASSWORD = "INSERT IBM SPEECH TO TEXT PASSWORD HERE"  # IBM Speech to Text passwords are mixed-case alphanumeric strings
        try:
            return self.recognizer.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
        except sr.UnknownValueError:
            print("IBM Speech to Text could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from IBM Speech to Text service; {0}".format(e))
