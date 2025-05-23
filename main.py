import requests
import time
import os

# ------------------ CONFIG ------------------

CONVO_ID = 't_1234567890123456'      # <-- Conversation ID
HATER_UID = '1000XXXXXXXXXXX'        # <-- Hater UID
DELAY_SECONDS = 3                    # <-- Delay between each message

TOKENS_FILE = 'tokens.txt'           # <-- File with one token per line
MESSAGES_FILE = 'messages.txt'       # <-- File with one message per line

# ------------------ FUNCTIONS ------------------

def load_file_lines(file_path):
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return []
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

def send_message(token, convo_id, hater_uid, message):
    url = f'https://graph.facebook.com/v20.0/{convo_id}/messages'
    data = {
        'recipient': f'{{"thread_key":"{convo_id}"}}',
        'message': f"{message} @{hater_uid}",
        'tagged_message_metadata': f'[{{"id":"{hater_uid}","offset":{len(message)+1},"length":{len(hater_uid)+1}}}]',
        'access_token': token
    }
    try:
        res = requests.post(url, data=data)
        if res.status_code == 200:
            return True
        else:
            print(f"  [Token Error] {res.json().get('error', {}).get('message', 'Unknown')}")
            return False
    except Exception as e:
        print(f"  [Request Failed] {str(e)}")
        return False

def start_spamming(tokens, messages, convo_id, hater_uid, delay):
    msg_index = 0
    token_index = 0

    while msg_index < len(messages):
        token = tokens[token_index]
        message = messages[msg_index]

        print(f"[{msg_index+1}] Trying token {token_index+1}/{len(tokens)}... ", end='')

        success = send_message(token, convo_id, hater_uid, message)

        if success:
            print("Sent successfully!")
            msg_index += 1
            time.sleep(delay)
        else:
            token_index += 1
            if token_index >= len(tokens):
                print("[!] All tokens failed. Exiting.")
                break

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ------------------ MAIN ------------------

if __name__ == '__main__':
    clear()
    print("==============================================")
    print(" Multi-Token Facebook Mention Spammer Tool")
    print("               by Broken Nadeem")
    print("==============================================\n")

    tokens = load_file_lines(TOKENS_FILE)
    messages = load_file_lines(MESSAGES_FILE)

    if not tokens:
        print("[!] No tokens found in tokens.txt")
        exit()
    if not messages:
        print("[!] No messages found in messages.txt")
        exit()

    print(f"Total Tokens Loaded   : {len(tokens)}")
    print(f"Total Messages Loaded : {len(messages)}")
    print(f"Target UID            : {HATER_UID}")
    print(f"Conversation ID       : {CONVO_ID}")
    print(f"Delay per message     : {DELAY_SECONDS} sec\n")

    proceed = input("Start Spamming? (y/n): ").lower()
    if proceed == 'y':
        start_spamming(tokens, messages, CONVO_ID, HATER_UID, DELAY_SECONDS)
    else:
        print("Aborted.")
