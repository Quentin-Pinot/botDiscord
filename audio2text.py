import speech_recognition as sr

def Audio2Text(audio_file=None):
    recognizer = sr.Recognizer()
    
    try:
        if audio_file:
            with sr.AudioFile(audio_file) as source:
                print("Processing audio file...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.record(source)
        else:
            with sr.Microphone() as source:
                print("Speak now...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
        
        text = recognizer.recognize_google(audio, language="fr-FR")
        return text
    
    except sr.UnknownValueError:
        return "Speech Recognition could not understand the audio"
    except sr.RequestError:
        return "Could not request results, check your internet connection"