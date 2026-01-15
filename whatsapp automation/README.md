# WhatsApp Automation

This project provides a script to automate sending WhatsApp messages to individual numbers or groups using `pywhatkit` and `pyautogui`.

## Prerequisites
You must have the following installed:
- Python 3.x
- `pywhatkit` library: `pip install pywhatkit`
- `pyautogui` library: `pip install pyautogui`
- **WhatsApp Web**: You must be logged into WhatsApp Web in your default browser.

## Features
- **Individual Messaging**: Send scheduled messages to any phone number (with country code).
- **Group Messaging**: Send messages to any group using its unique ID.
- **Auto-Send**: Uses `pyautogui` to simulate the "Enter" key press to ensure the message is dispatched.
- **Tab Management**: Automatically closes the WhatsApp Web tab after sending to keep your browser tidy.

## ⚠️ Important Warning
This script uses **GUII automation (`pyautogui`)**. Once the script opens your browser:
1. **Do not move your mouse** or use your keyboard until the message is sent.
2. The script will take control of your keyboard to press "Enter" and "Ctrl+W".
3. Ensure your browser is the active window when the payload is ready.

## Usage
Edit the `main()` block in `whatsapp_automation.py` with your target details and run:

```bash
python whatsapp_automation.py
```
