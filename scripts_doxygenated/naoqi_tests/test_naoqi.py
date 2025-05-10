##! @file test_naoqi.py
##! @brief Quick connectivity check to NAOqi by attempting to connect to ALTextToSpeech.
##! @details
##! This script attempts to establish a connection with a NAO robot's ALTextToSpeech
##! module using a specified IP address and port. It then reports whether the
##! connection was successful or provides the specific error message if it failed.
##! This is useful as a first-step diagnostic tool for NAOqi connectivity.
##!
##! @author Calvin Vandor (Enhanced by AI)
##! @date   2025-05-10
##! @version 1.1
##! @copyright MIT License

from naoqi import ALProxy
from typing import Tuple, Optional

# --- Configuration ---
## @var DEFAULT_NAO_IP
# @brief Default IP address of the NAO robot. **Modify this to your NAO's actual IP.**
DEFAULT_NAO_IP: str = "192.168.1.120"

## @var DEFAULT_NAO_PORT
# @brief Default port for NAOqi services, ALTextToSpeech typically uses 9559.
DEFAULT_NAO_PORT: int = 9559


def connect_to_tts(ip_address: str, port: int) -> Tuple[bool, Optional[str]]:
    """
    Attempts to create an ALProxy connection to NAO's ALTextToSpeech module.

    @param ip_address The IPv4 address of the NAO robot.
    @param port The TCP port for NAOqi services (typically 9559 for ALTextToSpeech).
    @return A tuple containing:
            - bool: True if the connection was successful, False otherwise.
            - Optional[str]: The error message if the connection failed, otherwise None.
    """
    try:
        ALProxy("ALTextToSpeech", ip_address, port)
        # If the line above doesn't raise an exception, connection is considered successful.
        return True, None
    except Exception as e:
        return False, str(e)


def main():
    """
    Main entry point for the NAOqi connectivity test script.
    It attempts to connect to the NAO robot using the configured IP and port,
    and prints the result of the connection attempt.
    """
    print(f"Attempting to connect to NAO at IP: {DEFAULT_NAO_IP}, Port: {DEFAULT_NAO_PORT}...")

    success, error_message = connect_to_tts(DEFAULT_NAO_IP, DEFAULT_NAO_PORT)

    if success:
        print("✅ Connected to NAO (ALTextToSpeech module) successfully!")
    else:
        print(f"❌ Failed to connect to NAO at {DEFAULT_NAO_IP}:{DEFAULT_NAO_PORT}.")
        if error_message:
            print(f"   Error details: {error_message}")
        else: # Should not happen if success is False based on connect_to_tts logic
            print("   An unknown error occurred.")


if __name__ == "__main__":
    main()
