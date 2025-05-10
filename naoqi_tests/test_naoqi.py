##! @file test_naoqi.py
##! @brief  One-shot ping: verifies NAO-qi connection via ALTextToSpeech.
##! @author Calvin Vandor

from naoqi import ALProxy

# Replace with your NAO's IP address
nao_ip = "192.168.1.120"

try:
    tts = ALProxy("ALTextToSpeech", nao_ip, 9559)
    print("Connected to NAO successfully!")
except Exception as e:
    print("Failed to connect to NAO:", e)

