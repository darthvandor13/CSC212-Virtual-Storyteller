##! @file test_asr.py
##! @brief  NAO virtual‑storyteller — keyword listener + ChatGPT narrator.
##!
##! A *refactored*, fully Doxygen‑ready version of the original **test_asr.py**
##! script.  The runtime behaviour is identical, but the logic is organised
##! into small, testable functions so that Doxygen can generate a richer API
##! reference (parameter tables, call graphs, etc.).
##!
##! ```mermaid
##! graph TD
##!     A[main()] --> B[init_proxies()]
##!     B --> C[configure_asr()]
##!     C --> D[listen loop]
##!     D --> E[fetch_story()] --> F[speak_story()]
##! ```
##!
##! @author  Calvin Vandor
##! @date    2025‑05‑08
##! @copyright MIT
##!

from __future__ import print_function  # Py2/3 print compatibility

from naoqi import ALProxy
import requests
import time

# ---------------------------------------------------------------------------
# Constants / global configuration
# ---------------------------------------------------------------------------

##! @var NAO_IP
##! @brief IPv4 address of the NAO robot running NAOqi.
NAO_IP = "192.168.1.120"

##! @var WEBHOOK_URL
##! @brief Local Flask endpoint that turns a recognised word into a story.
WEBHOOK_URL = "http://localhost:5000/generate_story"

##! @var VOCABULARY
##! @brief Words NAO should detect via ALSpeechRecognition.
VOCABULARY = ["hello", "story", "robot"]

# ---------------------------------------------------------------------------
# Helper functions (documented for Doxygen)
# ---------------------------------------------------------------------------

def init_proxies(ip, port=9559):
    """Create and return NAOqi proxies used by this demo.

    @param ip   NAO’s IPv4 address (e.g. ``192.168.1.120``).
    @param port NAOqi port; default = 9559.
    @return     Tuple ``(asr, memory, tts, motion)``.
    """
    asr    = ALProxy("ALSpeechRecognition", ip, port)
    memory = ALProxy("ALMemory",            ip, port)
    tts    = ALProxy("ALTextToSpeech",      ip, port)
    motion = ALProxy("ALMotion",            ip, port)
    return asr, memory, tts, motion


def configure_asr(asr, vocabulary):
    """Prepare NAO’s speech recogniser with the desired vocabulary.

    @param asr        ALSpeechRecognition proxy.
    @param vocabulary List of words NAO should detect.
    """
    asr.pause(True)
    asr.setVocabulary(vocabulary, True)
    asr.setParameter("Sensitivity", 0.9)
    asr.pause(False)
    asr.subscribe("Test_ASR")


def fetch_story(word):
    """Send the recognised *word* to the Flask webhook and return a story.

    @param word  The keyword recognised by NAO (e.g. ``"hello"``).
    @return      Story string on success, or a fallback message.
    """
    try:
        resp = requests.post(WEBHOOK_URL, json={"word": word})
        if resp.status_code == 200:
            return resp.json().get("story", "I don't know what to say.")
    except requests.RequestException as exc:
        print("[webhook error]", exc)
    return "Sorry, I couldn't reach the storyteller service."


def speak_story(tts, text):
    """Play *text* aloud via NAO’s Text‑to‑Speech.

    @param tts   ALTextToSpeech proxy.
    @param text  Unicode or UTF‑8 story string.
    """
    story_clean = text.encode('utf-8').replace(b"\n", b" ")
    print("NAO speaking …")
    tts.say(story_clean)


# ---------------------------------------------------------------------------
# Main control loop
# ---------------------------------------------------------------------------

def main():
    """Entry point — initialises proxies, listens for a keyword and narrates
    the resulting story until **Ctrl‑C** is pressed.
    """
    asr, memory, tts, motion = init_proxies(NAO_IP)

    # Relax motors while listening
    motion.setStiffnesses("Body", 0.0)

    configure_asr(asr, VOCABULARY)
    print("Listening… say one of: {}".format(VOCABULARY))

    try:
        while True:
            word_data = memory.getData("WordRecognized")
            if word_data and len(word_data) >= 2:
                recognised_word = word_data[0].strip("<...>").strip()
                confidence      = word_data[1]
                if confidence < 0.6:
                    time.sleep(0.5)
                    continue

                print("[ASR]", recognised_word, "(conf = {:.2f})".format(confidence))

                story = fetch_story(recognised_word)
                print("[story]", story)
                speak_story(tts, story)

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopping ASR…")
        asr.unsubscribe("Test_ASR")


# ---------------------------------------------------------------------------
# Script guard
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()

