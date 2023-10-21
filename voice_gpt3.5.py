import openai
import pyttsx3
import speech_recognition as sr
import key
import time

openai.api_key=key.api_key
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skipping unknown Error')
         
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        speak_text("Hii .  Welcome. I am your Personal voice enable Chat-Bot. ")
        speak_text("Say 'Hello' to start recording your question.")
        print("Say 'Hello' to start recording your question...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower()=="hello":
                    filename = "input.wav"
                    speak_text("Speak out your Question.")
                    print("Speak out your Question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said : {text}")
                        response = generate_response(text)
                        print(f"GRT-3 says : {response}")
                        speak_text(response)
            except Exception as e:
                print("Error Occured : {}".format(e))

if __name__ =="__main__":
    main()