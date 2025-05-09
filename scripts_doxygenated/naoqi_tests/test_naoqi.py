##! @file test_naoqi.py
##! @brief  Quick connectivity check to NAO‑qi: tries ALTextToSpeech and
##!         returns a boolean result.
##!
##! Refactored into a function‑centric style so Doxygen can emit parameter and
##! return docs while leaving behaviour 100 % identical to the original script.
##!
##! @author Calvin Vandor
##! @date   2025-05-08
##! @copyright MIT License
##!

from naoqi import ALProxy

#: Default NAO‑qi port
DEFAULT_PORT = 9559  ##! @var
                    ##! @brief Port used by NAO‑qi (rarely changed).


def connect_tts(ip, port=DEFAULT_PORT):
    """Attempt to create an **ALTextToSpeech** proxy.

    @param ip:   IPv4 address of the NAO robot (e.g. "192.168.1.120").
    @param port: NAO‑qi TCP port.  Default is 9559.
    @return:     ``True`` if the proxy is reachable, ``False`` otherwise.
    """
    try:
        ALProxy("ALTextToSpeech", ip, port)
        return True
    except Exception:
        return False


def main():
    """Entry point.  Reads the *nao_ip* constant and prints the result."""
    nao_ip = "192.168.1.120"  # TODO: move to config/env var

    if connect_tts(nao_ip):
        print("Connected to NAO successfully!")
    else:
        print("Failed to connect to NAO at", nao_ip)


if __name__ == "__main__":
    main()

