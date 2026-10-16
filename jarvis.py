import datetime
import os
import sys
import webbrowser

try:
    import pyttsx3
    TTS_AVAILABLE = True
except Exception:
    TTS_AVAILABLE = False

try:
    import speech_recognition as sr
    STT_AVAILABLE = True
except Exception:
    STT_AVAILABLE = False


class JarvisEngine:
    def __init__(self):
        self.tts_engine = None
        self.recognizer = None

        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                # Set voice properties
                voices = self.tts_engine.getProperty("voices")
                if voices:
                    self.tts_engine.setProperty("voice", voices[0].id)
                self.tts_engine.setProperty("rate", 175)
                self.tts_engine.setProperty("volume", 1.0)
            except Exception as e:
                print(f"[Warning] TTS initialization failed: {e}")

        if STT_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.recognizer.energy_threshold = 300
                self.recognizer.dynamic_energy_threshold = True
            except Exception as e:
                print(f"[Warning] Speech recognition initialization failed: {e}")

    def speak(self, text):
        """Converts text to speech and prints it out to console."""
        print(f"Jarvis: {text}")
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"[TTS Error] {e}")

    def listen(self):
        """Listens to user input from microphone or falls back to console input."""
        if self.recognizer and STT_AVAILABLE:
            try:
                with sr.Microphone() as source:
                    print("\n[Listening... Speak into microphone]")
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    print("[Processing speech...]")
                    query = self.recognizer.recognize_google(audio, language="en-IN")
                    print(f"You said: {query}")
                    return query.lower().strip()
            except sr.WaitTimeoutError:
                print("[Listening timed out]")
            except sr.UnknownValueError:
                self.speak("I couldn't catch that clearly. Could you please repeat?")
                return ""
            except Exception as e:
                print(f"[Microphone Error] {e}. Falling back to text mode.")

        # Fallback to manual text input
        try:
            return input("\nYou: ").lower().strip()
        except (KeyboardInterrupt, EOFError):
            return "exit"

    def handle_query(self, query):
        """Process user intent based on query string."""
        if not query:
            return True

        if any(word in query for word in ["exit", "quit", "bye", "stop"]):
            self.speak("Goodbye! Have a great day ahead.")
            return False

        elif "time" in query:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {now}.")

        elif "date" in query or "day" in query:
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            self.speak(f"Today is {today}.")

        elif "hello" in query or "hi" in query or "hey" in query:
            self.speak("Hello! How can I help you today?")

        elif "who are you" in query or "your name" in query:
            self.speak("I am Jarvis, your personal Python AI voice assistant.")

        elif "open google" in query:
            self.speak("Opening Google in browser.")
            webbrowser.open("https://www.google.com")

        elif "open youtube" in query:
            self.speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        elif "search" in query:
            search_term = query.replace("search", "").replace("for", "").strip()
            if search_term:
                self.speak(f"Searching web for {search_term}")
                webbrowser.open(f"https://www.google.com/search?q={search_term}")
            else:
                self.speak("What would you like me to search for?")

        elif "joke" in query:
            self.speak("Why do programmers prefer dark mode? Because light attracts bugs!")

        else:
            self.speak(f"I heard: '{query}'. Enhanced conversational features are coming soon!")

        return True


def main():
    jarvis = JarvisEngine()
    jarvis.speak("Initializing systems... Hello, I am Jarvis. How can I assist you?")

    running = True
    while running:
        query = jarvis.listen()
        running = jarvis.handle_query(query)


if __name__ == "__main__":
    main()
