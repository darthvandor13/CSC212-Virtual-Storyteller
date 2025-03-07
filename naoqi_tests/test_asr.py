from naoqi import ALProxy
import requests
import time

# NAO's IP address
nao_ip = "192.168.1.120"

# Webhook URL for ChatGPT API
WEBHOOK_URL = "http://localhost:5000/generate_story"

# Connect to ASR (Speech Recognition)
asr = ALProxy("ALSpeechRecognition", nao_ip, 9559)

# Connect to Memory Proxy (to retrieve recognized words)
memory = ALProxy("ALMemory", nao_ip, 9559)

# Connect to NAO's Text-to-Speech
tts = ALProxy("ALTextToSpeech", nao_ip, 9559)

# Stop movements before listening
motion = ALProxy("ALMotion", nao_ip, 9559)
motion.setStiffnesses("Body", 0.0)

# Pause ASR before setting vocabulary
asr.pause(True)

# Define vocabulary (words NAO should recognize)
vocabulary = ["hello", "story", "robot"]
asr.setVocabulary(vocabulary, True)

# Increase ASR Sensitivity to catch more words
asr.setParameter("Sensitivity", 0.9)

# Resume ASR so it can listen
asr.pause(False)

# Start listening
asr.subscribe("Test_ASR")

print("Listening... Say a word from:", vocabulary)

try:
    while True:
        word_data = memory.getData("WordRecognized")  # Get recognized words
        if word_data and len(word_data) >= 2:
            recognized_word = word_data[0].strip("<...>").strip()
            confidence = word_data[1]

            # Ignore low-confidence detections
            if confidence < 0.6:
                continue

            print("Recognized:", recognized_word, "(Confidence: {})".format(confidence))

            # Send recognized word to ChatGPT API
            response = requests.post(WEBHOOK_URL, json={"word": recognized_word})
            if response.status_code == 200:
                story = response.json().get("story", "I don't know what to say.")
                print("Generated Story:", story)

                # Have NAO read the story aloud
                # Convert the story to a plain string, remove newlines
		story_clean = story.encode('utf-8').replace("\n", " ")

		print("NAO Speaking Story...")
		tts.say(story_clean)


        # Sleep briefly to prevent excessive processing
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nStopping ASR...")
    asr.unsubscribe("Test_ASR")  # Stop listening
