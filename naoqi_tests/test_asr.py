##! @file test_asr.py
##! @brief  Listens for keywords with NAO’s microphone, sends the recognised word
##!         to a ChatGPT‑powered webhook, and plays the returned story via
##!         NAO’s built‑in Text‑to‑Speech (TTS).
##!
##! This script is intentionally kept as a *single, top‑level loop* to preserve
##! the original project logic.  No functions are introduced here so that the
##! behaviour remains byte‑for‑byte identical — only comments were added to make
##! the file fully Doxygen‑ready.
##!
##! ### Usage (example)
##! ```bash
##! python2 test_asr.py   # run inside the naoqi_env virtual‑env
##! ```
##!
##! @author Calvin Vandor
##! @date   2025‑05‑08
##! @copyright MIT

from naoqi import ALProxy
import requests
import time

# --------------------------------------------------------------------------- #
# Global configuration                                                         #
# --------------------------------------------------------------------------- #

##! @var str nao_ip
##! @brief IPv4 address of the NAO robot running the NAOqi SDK.
nao_ip = "192.168.1.120"

##! @var str WEBHOOK_URL
##! @brief Local Flask endpoint that transforms a word into a short story.
WEBHOOK_URL = "http://localhost:5000/generate_story"

# --------------------------------------------------------------------------- #
# Proxy initialisation                                                         #
# --------------------------------------------------------------------------- #

##! @brief ALSpeechRecognition proxy used for keyword spotting.
asr = ALProxy("ALSpeechRecognition", nao_ip, 9559)

##! @brief ALMemory proxy for retrieving recognised words and confidence.
memory = ALProxy("ALMemory", nao_ip, 9559)

##! @brief ALTextToSpeech proxy for audio output through NAO’s speakers.
tts = ALProxy("ALTextToSpeech", nao_ip, 9559)

##! @brief ALMotion proxy — motors are relaxed while listening.
motion = ALProxy("ALMotion", nao_ip, 9559)
motion.setStiffnesses("Body", 0.0)

# --------------------------------------------------------------------------- #
# Speech‑recognition setup                                                    #
# --------------------------------------------------------------------------- #

asr.pause(True)  # suspend recognition while configuring

##! @var list vocabulary
##! @brief Words NAO should detect.  *Case‑insensitive.*
vocabulary = ["hello", "story", "robot"]
asr.setVocabulary(vocabulary, True)

##! Increase ASR sensitivity (0–1) so NAO is more likely to match a word.
asr.setParameter("Sensitivity", 0.9)

asr.pause(False)            # resume recognition
asr.subscribe("Test_ASR")   # start listening

print("Listening… Say a word from:", vocabulary)

# --------------------------------------------------------------------------- #
# Main loop                                                                   #
# --------------------------------------------------------------------------- #

try:
    while True:
        # Retrieve recognised word + confidence from NAOqi memory
        word_data = memory.getData("WordRecognized")
        if word_data and len(word_data) >= 2:
            recognised_word = word_data[0].strip("<...>").strip()
            confidence      = word_data[1]

            # Ignore low‑confidence detections (< 0.6)
            if confidence < 0.6:
                time.sleep(0.5)
                continue

            print("Recognised:", recognised_word,
                  "(Confidence: {:.2f})".format(confidence))

            # ----------------------------------------------------------------
            # Call the local webhook to generate a story
            # ----------------------------------------------------------------

            response = requests.post(WEBHOOK_URL,
                                     json={"word": recognised_word})
            if response.status_code == 200:
                story = response.json().get("story",
                                            "I don't know what to say.")
                print("Generated Story:", story)

                ##! @brief Speak the story through NAO’s TTS.
                #        Newlines are stripped for smoother speech.
                story_clean = story.encode("utf‑8").replace(b"\n", b" ")

                print("NAO Speaking Story…")
                tts.say(story_clean)

        # Sleep briefly to prevent excessive CPU usage
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nStopping ASR…")
    asr.unsubscribe("Test_ASR")  # stop listening

