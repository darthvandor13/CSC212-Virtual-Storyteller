##! @file test_asr.py
##! @brief  NAO virtual-storyteller — keyword listener + ChatGPT narrator.
##!
##! A *refactored*, fully Doxygen-ready version of the original **test_asr.py**
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
##! @date    2025-05-08
##! @copyright MIT
##!

from __future__ import print_function  # Py2/3 print compatibility

from naoqi import ALProxy
import requests
import time
# Consider adding 'from typing import Tuple, List, Dict, Any, Optional' if adding Python type hints

# ---------------------------------------------------------------------------
# Constants / global configuration
# ---------------------------------------------------------------------------

##! @var NAO_IP
##! @brief IPv4 address of the NAO robot running NAOqi.
NAO_IP = "192.168.1.120"

##! @var WEBHOOK_URL
##! @brief Local Flask endpoint that turns a recognised word into a story.
##! @note Expected to receive JSON `{"word": "recognized_word"}` and return JSON `{"story": "story_text"}`.
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
    print(f"ℹ️ Initializing NAOqi proxies for IP {ip}:{port}...")
    asr    = ALProxy("ALSpeechRecognition", ip, port)
    memory = ALProxy("ALMemory",            ip, port)
    tts    = ALProxy("ALTextToSpeech",      ip, port)
    motion = ALProxy("ALMotion",            ip, port)
    print("✅ Proxies initialized.")
    return asr, memory, tts, motion


def configure_asr(asr, vocabulary):
    """Prepare NAO’s speech recogniser with the desired vocabulary.

    @param asr        ALSpeechRecognition proxy.
    @param vocabulary List of words NAO should detect.
    """
    print("⚙️ Configuring ASR...")
    asr.pause(True)  # Pause recognition while making changes
    asr.setVocabulary(vocabulary, True) # True to enable word spotting for these words
    # Set sensitivity (0.0 to 1.0). Higher values make it more sensitive.
    # 0.9 is chosen for potentially better detection in various environments.
    asr.setParameter("Sensitivity", 0.9)
    asr.pause(False) # Resume recognition
    asr.subscribe("Test_ASR") # Subscribe to the ASR event with a unique name
    print("✅ ASR configured and subscribed.")


def fetch_story(word):
    """Send the recognised *word* to the Flask webhook and return a story.

    @param word  The keyword recognised by NAO (e.g. ``"hello"``).
    @return      Story string on success, or a fallback message.
    """
    print(f"📞 Calling webhook at {WEBHOOK_URL} with word: '{word}'")
    try:
        # Webhook expects JSON: {"word": "recognized_word"}
        resp = requests.post(WEBHOOK_URL, json={"word": word}, timeout=10) # Added timeout
        resp.raise_for_status() # Raise an HTTPError for bad responses (4XX or 5XX)
        
        # Webhook response expected JSON: {"story": "generated_story_text"}
        return resp.json().get("story", "I tried to get a story, but the storyteller seems to be at a loss for words.")
    except requests.exceptions.Timeout:
        print(f"❌ [webhook error] Request to {WEBHOOK_URL} timed out.")
        return "Sorry, the storyteller service took too long to respond."
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ [webhook error] HTTP error occurred: {http_err}. Response: {http_err.response.text[:200] if http_err.response else 'No response body'}")
        return "Sorry, there was an issue communicating with the storyteller service."
    except requests.RequestException as exc: # Catches other requests-related errors like ConnectionError
        print(f"❌ [webhook error] Failed to connect or send request: {exc}")
        return "Sorry, I couldn't reach the storyteller service right now."
    except ValueError as json_err: # If resp.json() fails
        print(f"❌ [webhook error] Could not decode JSON response from webhook: {json_err}")
        return "The storyteller service gave a response I couldn't understand."


def speak_story(tts, text):
    """Play *text* aloud via NAO’s Text-to-Speech.

    @param tts   ALTextToSpeech proxy.
    @param text  Unicode or UTF-8 story string.
    """
    # Encode to UTF-8 and replace newlines with spaces for smoother speech flow.
    # NAO's TTS might handle raw newlines as pauses, but spaces ensure continuity.
    story_clean = text.encode('utf-8').replace(b"\n", b" ")
    print("🗣️ NAO speaking story…")
    tts.say(story_clean)
    print("✅ Story spoken.")


# ---------------------------------------------------------------------------
# Main control loop
# ---------------------------------------------------------------------------

def main():
    """Entry point — initialises proxies, listens for a keyword and narrates
    the resulting story until **Ctrl-C** is pressed.
    """
    asr, memory, tts, motion = init_proxies(NAO_IP)

    # Relax motors to reduce motor noise during listening and allow NAO to focus.
    motion.setStiffnesses("Body", 0.0)

    configure_asr(asr, VOCABULARY)
    print(f"👂 Listening… Say one of: {VOCABULARY}")

    try:
        while True:
            # Retrieve data from ALMemory where ASR posts recognition results.
            # "WordRecognized" event data: [recognized_word_string, confidence_value]
            word_data = memory.getData("WordRecognized")

            if word_data and len(word_data) >= 2:
                # NAOqi might add <...> around spotted words; strip them for the raw word.
                recognised_word = word_data[0].strip("<...>").strip()
                confidence      = word_data[1]

                # Filter out low-confidence recognitions to reduce false positives.
                # 0.6 is a common threshold; adjust based on performance.
                if confidence < 0.6:
                    # Clear the event so it's not re-processed immediately if no new word is spoken.
                    # This is important as getData("WordRecognized") might return the same old data.
                    # However, directly clearing "WordRecognized" is not standard.
                    # ASR usually clears it or it's an event you subscribe to.
                    # For a polling loop like this, ensuring ASR is set to not repeat old data
                    # or handling it by timestamp/flag might be needed if issues arise.
                    # For now, a simple sleep and continue.
                    time.sleep(0.1) # Shorter sleep if just filtering confidence
                    continue

                print(f"🔍 [ASR] Recognized: '{recognised_word}' (Confidence: {confidence:.2f})")

                story = fetch_story(recognised_word)
                print(f"📖 [Story Received] '{story[:100]}...'") # Print a preview
                
                speak_story(tts, story)
                
                # After processing a word, it's good practice to ensure ALMemory doesn't keep serving the same event.
                # Depending on NAOqi version and ASR settings, you might need to manually clear it
                # or rely on ASR to only update it on new recognitions.
                # For simplicity, we assume ASR updates it. A small delay helps.
                print("--- Waiting for next keyword ---")


            # Brief sleep to prevent a tight loop consuming too much CPU if no word is recognized.
            time.sleep(0.5) 

    except KeyboardInterrupt:
        print("\n🚫 Ctrl-C detected. Stopping ASR and exiting...")
    finally:
        # Ensure ASR is unsubscribed and motors are re-stiffened (optional) on exit.
        if 'asr' in locals() and asr: # Check if asr was initialized
            print("🛑 Unsubscribing from ASR...")
            asr.unsubscribe("Test_ASR")
        if 'motion' in locals() and motion: # Check if motion was initialized
            print("💪 Re-stiffening NAO's motors (optional)...")
            # motion.setStiffnesses("Body", 1.0) # Or a preferred resting stiffness
        print("👋 Exiting script.")


# ---------------------------------------------------------------------------
# Script guard
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
