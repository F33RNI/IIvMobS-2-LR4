"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
"""

import sys
import webbrowser
import logging

import pyttsx3
import speech_recognition as sr


# Selected voice properties
VOICE_ID = 10
VOICE_RATE = 180
VOICE_VOLUME = 1.0


def talk(voice_engine: pyttsx3.engine.Engine, words: str) -> None:
    """Converts text to speech

    Args:
        voice_engine (pyttsx3.engine.Engine): initialized pyttsx3 voice engine
        words (str): words to say
    """
    logging.info(f"Saying: {words}")
    voice_engine.say(words)
    voice_engine.runAndWait()


def recognize_command(voice_engine: pyttsx3.engine.Engine) -> str:
    """Tries to recognize command in a recursion

    Args:
        voice_engine (pyttsx3.engine.Engine): initialized pyttsx3 voice engine

    Returns:
        str: recognized command
    """
    logging.info("Initializing recognizer")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        talk(voice_engine, "Speak now")
        recognizer.pause_threshold = 1
        # recognizer.adjust_for_ambient_noise(source, duration=1)
        logging.info("Listening...")
        audio = recognizer.listen(source)

    # Try to recognize
    try:
        command = recognizer.recognize_google(audio).lower()
        logging.info(f"Recognized command: {command}")
        talk(voice_engine, f"Recognized command: {command}")
        recognizer.pause_thresholds = 1

    # Recognition error -> recognize again in recursion
    except sr.UnknownValueError:
        talk(voice_engine, "Command is not recognized. Try again")
        command = recognize_command(voice_engine)
    return command


def execute_command(voice_engine: pyttsx3.engine.Engine, command: str) -> None:
    """Parses and executes command

    Args:
        voice_engine (pyttsx3.engine.Engine): initialized pyttsx3 voice engine
        command (str): command to execute
    """
    if "play music" in command:
        talk(voice_engine, "Playing music now")
        print("Playing music now")
        URL = "https://www.spotify.com"
        webbrowser.open(URL)

    elif "stop" in command:
        talk(voice_engine, "OK stopping now")
        print("OK stopping now")
        sys.exit()

    elif "tell me a joke" in command:
        talk(voice_engine, "Why don't scientists trust atoms? Because they make up everything!")
        print("Why don't scientists trust atoms? Because they make up everything!")

    elif "search video" in command:
        talk(voice_engine, "What video should I search for?")
        print("What video should I search for?")
        search = recognize_command(voice_engine)
        url = "https://www.youtube.com/results?search_query=" + search
        webbrowser.open(url)

    elif "find recipe" in command:
        talk(voice_engine, "What is the recipe?")
        print("What is the recipe?")
        recipe = recognize_command(voice_engine)
        url = "https://www.google.com/search?q=" + recipe + "+recipe"
        webbrowser.open(url)

    elif "read book" in command:
        talk(voice_engine, "What is the name of the book?")
        print("What is the name of the book?")
        name = recognize_command(voice_engine)
        url = "https://www.gutenberg.org/ebooks/search/?query=" + name
        webbrowser.open(url)

    elif "news" in command:
        talk(voice_engine, "Opening news")
        print("Opening news")
        url = "https://www.bbc.com/news"
        webbrowser.open(url)


def main() -> None:
    """Main entry"""
    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    # Initialize TTS
    logging.info("Initializing pyttsx3 voice engine")
    voice_engine = pyttsx3.init()
    voices = voice_engine.getProperty("voices")
    logging.info(f"Available: {len(voices)} voices")
    for i, voice in enumerate(voices):
        print(i, voice.id, voice)

    # Selecting voices
    voice_engine.setProperty("voice", voices[VOICE_ID].id)
    voice_engine.setProperty("rate", VOICE_RATE)
    voice_engine.setProperty("volume", VOICE_VOLUME)

    # Main TTS loop
    while True:
        try:
            execute_command(voice_engine, recognize_command(voice_engine))
            talk(voice_engine, "Now i'm listening again")

        except (SystemExit, KeyboardInterrupt):
            logging.warning("Interrupted! Exiting")
            break

    # Exit gracefully
    logging.info("Stopping voice engine")
    voice_engine.stop()
    logging.info("Done")


if __name__ == "__main__":
    main()
