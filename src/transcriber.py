import speech_recognition as sr


class Transcriber:
    """This transcriber uses pre-processed audio format files to generate text from number of APIs."""
    def __init__(self, audio):
        "audio must be a sr.AudioSegment()"
        self._audio = audio

    def transcribe(self):
        r = sr.Recognizer()
        with self._audio as source:
            audio = r.record(source)
        try:
            text = r.recognize_google(audio)
            return text
        except Exception as e:
            return "Couldn't transcribe"



