##! @file test_tts.py
##! @brief  Minimal NAO‑qi Text‑to‑Speech smoke‑test.
##!
##! Given a robot IP address, this utility connects to the **ALTextToSpeech**
##! proxy and makes NAO say a short greeting.  It is deliberately tiny — meant
##! as the first test after configuring NAO‑qi on a new workstation.
##!
##! @author Calvin Vandor
##! @date   2025‑05‑08
##! @copyright MIT License
##!

from naoqi import ALProxy

#: Default NAO IPv4 address — override on the CLI or by editing this constant.
DEFAULT_NAO_IP = "192.168.1.120"


def get_tts_proxy(ip: str = DEFAULT_NAO_IP):
    """Return an :pyclass:`ALTextToSpeech` proxy.

    @param ip  NAO’s IPv4 address.
    @return    An initialised **ALTextToSpeech** proxy.
    """
    return ALProxy("ALTextToSpeech", ip, 9559)


def speak_greeting(tts, text: str = "Hello! I am ready to tell a story."):
    """Play a single line via NAO’s speakers.

    @param tts   The **ALTextToSpeech** proxy returned by :pyfunc:`get_tts_proxy`.
    @param text  The sentence to speak (UTF‑8).
    """
    tts.say(text)


def main():
    """Entry point — connects and speaks the default greeting. """
    tts = get_tts_proxy()
    speak_greeting(tts)


if __name__ == "__main__":
    main()

