"""
TASK 1 - Voice Assistant (Beginner Tier)
-----------------------------------------
A simple Python voice assistant that:
  - Listens to spoken commands using the microphone (speech_recognition)
  - Responds with text-to-speech (pyttsx3)
  - Greets the user, tells date/time, and performs a web search

Install requirements first:
    pip install SpeechRecognition pyttsx3 pyaudio

Note: pyaudio can be tricky to install on some systems.
  - Windows: pip install pyaudio
  - Mac:     brew install portaudio && pip install pyaudio
  - Linux:   sudo apt-get install python3-pyaudio
"""

import datetime
import webbrowser

import speech_recognition as sr
import pyttsx3

# ---------- Setup text-to-speech engine ----------
engine = pyttsx3.init()
engine.setProperty("rate", 170)  # speaking speed


def speak(text: str) -> None:
    """Speak the given text out loud and also print it."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def listen() -> str:
    """
    Capture audio from the microphone and convert it to text.
    Returns an empty string if speech was not understood.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening... (speak now)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
            return ""

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        # Graceful error handling as required by the feature checklist
        speak("Sorry, I didn't understand that. Could you please repeat?")
        return ""
    except sr.RequestError:
        speak("Speech service is unavailable right now.")
        return ""


def handle_command(command: str) -> bool:
    """
    Decide what to do based on keywords in the command.
    Returns False if the assistant should stop, True otherwise.
    """
    if not command:
        return True

    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you today?")

    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")

    elif "date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")

    elif "search" in command:
        # e.g. "search for python tutorials"
        topic = command.replace("search for", "").replace("search", "").strip()
        if topic:
            speak(f"Searching the web for {topic}")
            webbrowser.open(f"https://www.google.com/search?q={topic}")
        else:
            speak("What would you like me to search for?")

    elif "stop" in command or "exit" in command or "quit" in command:
        speak("Goodbye! Have a great day.")
        return False

    else:
        speak("I can help with greetings, telling the time or date, "
              "or searching the web. Please try one of those.")

    return True


def main():
    speak("Voice assistant activated. Say 'hello', ask for the 'time' or "
          "'date', say 'search for <topic>', or say 'stop' to quit.")
    running = True
    while running:
        command = listen()
        running = handle_command(command)


# ---------- Text-only fallback (no microphone needed) ----------
def text_mode():
    """
    Fallback mode for testing without a microphone.
    Type commands instead of speaking them.
    """
    print("Running in TEXT MODE (type commands instead of speaking).")
    speak("Voice assistant activated in text mode.")
    running = True
    while running:
        command = input("\nType a command (or 'stop' to quit): ").lower()
        running = handle_command(command)


if __name__ == "__main__":
    mode = input("Choose mode - (1) Voice  (2) Text  [default 2]: ").strip()
    if mode == "1":
        main()
    else:
        text_mode()
