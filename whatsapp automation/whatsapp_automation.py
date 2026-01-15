import pywhatkit as kit
import pyautogui
import time
from datetime import datetime

class WhatsAppAutomator:
    """
    A utility class to automate sending WhatsApp messages.
    Note: Requires a logged-in WhatsApp Web account in your default browser.
    """
    
    @staticmethod
    def send_direct_message(phone_no: str, message: str, wait_time: int = 15, tab_close: bool = True):
        """
        Sends a WhatsApp message to a specific phone number instantly (or at scheduled time).
        
        Args:
            phone_no: Target phone number with country code (e.g., '+923001234567').
            message: The message content.
            wait_time: Seconds to wait for WhatsApp Web to load.
            tab_close: Whether to automatically close the browser tab after sending.
        """
        print(f"Scheduling message to {phone_no}...")
        now = datetime.now()
        
        # pywhatkit.sendwhatmsg sends at a specific time. 
        # For 'instant' we use current time + 1 or 2 minutes (minimum required by kit)
        # However, pywhatkit.sendwhatmsg_instantly exists in newer versions.
        # Following notebook logic:
        hour = now.hour
        minute = now.minute + 2 # Schedule 2 mins from now
        
        if minute >= 60:
            minute -= 60
            hour = (hour + 1) % 24

        kit.sendwhatmsg(phone_no, message, hour, minute, wait_time)
        
        # Ensure the message is actually sent by pressing Enter
        time.sleep(10)
        pyautogui.press("enter")
        
        if tab_close:
            time.sleep(3)
            pyautogui.hotkey("ctrl", "w")
            print("Tab closed.")

    @staticmethod
    def send_group_message(group_id: str, message: str, wait_time: int = 15, tab_close: bool = True):
        """
        Sends a WhatsApp message to a specific group.
        
        Args:
            group_id: Unique identifier for the group (found in invite link).
            message: The message content.
            wait_time: Seconds to wait for WhatsApp Web to load.
            tab_close: Whether to automatically close the browser tab after sending.
        """
        print(f"Scheduling message to group {group_id}...")
        now = datetime.now()
        hour = now.hour
        minute = now.minute + 2
        
        if minute >= 60:
            minute -= 60
            hour = (hour + 1) % 24

        kit.sendwhatmsg_to_group(group_id, message, hour, minute, wait_time)
        
        time.sleep(10)
        pyautogui.press("enter")
        
        if tab_close:
            time.sleep(3)
            pyautogui.hotkey("ctrl", "w")
            print("Tab closed.")

def main():
    print("--- WhatsApp Automation Tool ---")
    print("WARNING: This script uses pyautogui to control your keyboard. Do not interact with your PC while it runs.")
    
    automator = WhatsAppAutomator()
    
    # Example Usage (Commented to prevent accidental execution):
    automator.send_direct_message('+923004848190', "Hello from automation script!")
    # automator.send_group_message('DkFLHZpmfnH2MI3xgJBaV', "Group reminder!")

if __name__ == "__main__":
    main()
