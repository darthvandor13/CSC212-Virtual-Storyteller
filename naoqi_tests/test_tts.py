##! @file test_tts.py
##! @brief  Quick NAO TTS sanity-check (speaks one line).
##! @author Calvin Vandor

from naoqi import ALProxy

# Replace with your NAO's IP address
nao_ip = "192.168.1.120"

# Connect to NAO's Text-to-Speech (TTS) system
tts = ALProxy("ALTextToSpeech", nao_ip, 9559)

# Make NAO speak
tts.say("Hello! I am ready to tell a story.")

