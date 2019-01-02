from gtts import gTTS
import logging
import speech_recognition as sr
import os
import audio_helper

ENGINE_WITAI='witai'
ENGINE_GOOGLE='gtts'

recogniser = sr.Recognizer()


def recognition(engine='', api_key=''):
    global recogniser
    logging.info('Listening...')

    try:
        with sr.Microphone() as source:
            audio = recogniser.record(source, duration=2)

        result = None

        if ENGINE_WITAI == engine:
            result = recogniser.recognize_wit(audio, key=api_key)
        elif ENGINE_GOOGLE == engine:
            result = recogniser.recognize_google(audio, language='en-GB').lower()

        os.system('play audio/confirmation.wav')
        print('Recognised: %s' % result)

        return result

    except sr.UnknownValueError:
        logging.warning('Speech not recognised')
        return False
    except sr.RequestError:
        logging.error('Request error')
        synthesis('Sorry, please try again')
        return False


def synthesis(text_to_say):
    language = 'ro'
    tts = gTTS(text=text_to_say, lang=language)
    tts.save('tts.mp3')
    audio_helper.play_audio('tts.mp3')
