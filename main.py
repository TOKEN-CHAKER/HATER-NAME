import requests
import time
import os

# ------------------ CONFIGURATION ------------------

ACCESS_TOKEN = 'EAABXXXXXXXXXXXX'     # <-- Your Facebook EAAB token
CONVO_ID = 't_1234567890123456'       # <-- Conversation ID (with 't_' prefix)
HATER_UID = '1000XXXXXXXXXXX'         # <-- UID of the person to mention
DELAY_SECONDS = 3                     # <-- Delay between messages

MESSAGES_FILE = 'messages.txt'        # <-- File containing messages (one per line)

# ------------------ MESSAGE SENDING FUNCTION ------------------

def load_messages(file_path):
    if not os.path.exists(file_path):
        print(f"[ERROR] Message file not found: {file_path}")
        return []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()]
    return lines

def send_mention_message(hater_uid, convo_id, messages, token, delay):
    url = f'https://graph.facebook.com/v20.0/{convo_id}/messages'
    
    for idx, msg in enumerate(messages, 1):
        full_message = f"{msg} @{hater_uid}"
        data = {
            'recipient': f'{{"thread_key":"{convo_id}"}}',
            'message': full_message,
            'tagged_message_metadata': f'[{{"id":"{hater_uid}","offset":{len(msg)+1},"length":{len(hater_uid)+1}}}]',
            'access_token': token
        }

        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"[{idx}] Sent: '{msg}' with mention")
        else:
            print(f"[{idx}] Failed: {response.text}")
        time.sleep(delay)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ------------------ MAIN PROGRAM ------------------

if __name__ == '__main__':
    clear()
    print("========================================")
    print("  Facebook Mention Spammer with File")
    print("           by Broken Nadeem")
    print("========================================\n")

    messages = load_messages(MESSAGES_FILE)
    if not messages:
        print("[!] No messages loaded. Exiting.")
        exit()

    print(f"Total Messages Loaded : {len(messages)}")
    print(f"Target UID            : {HATER_UID}")
    print(f"Conversation ID       : {CONVO_ID}")
    print(f"Delay per message     : {DELAY_SECONDS} sec\n")

    proceed = input("Start Spamming? (y/n): ").lower()
    if proceed == 'y':
        send_mention_message(HATER_UID, CONVO_ID, messages, ACCESS_TOKEN, DELAY_SECONDS)
    else:
        print("Aborted.")
