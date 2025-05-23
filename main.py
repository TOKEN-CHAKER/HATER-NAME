import requests
import time
import os
import json

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_file_lines(file_path):
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def send_message(token, convo_id, hater_uid, message):
    mention_text = f"{message} @{hater_uid}"
    url = f"https://graph.facebook.com/v20.0/{convo_id}/messages"

    # Tag metadata for mention (best-effort)
    tag_data = [{
        "id": hater_uid,
        "offset": len(message) + 1,
        "length": len(hater_uid) + 1
    }]

    payload = {
        "message": mention_text,
        "tagged_message_metadata": json.dumps(tag_data),
        "access_token": token
    }

    try:
        res = requests.post(url, data=payload)
        if res.status_code == 200:
            return True
        else:
            print(f"[x] Error: {res.json().get('error', {}).get('message')}")
            return False
    except Exception as e:
        print(f"[x] Request Failed: {str(e)}")
        return False

def start_spamming(tokens, messages, convo_id, hater_uid, delay):
    msg_index = 0
    token_index = 0

    while msg_index < len(messages):
        if token_index >= len(tokens):
            print("[!] All tokens failed. Stopping.")
            break

        current_token = tokens[token_index]
        current_message = messages[msg_index]

        print(f"[{msg_index+1}] Sending with token {token_index+1}: ", end='')
        success = send_message(current_token, convo_id, hater_uid, current_message)

        if success:
            print("Success")
            msg_index += 1
            time.sleep(delay)
        else:
            print("Failed. Trying next token...")
            token_index += 1

# ======================== MAIN ========================

if __name__ == "__main__":
    clear()
    print("=============================================")
    print("      Facebook Mention Spammer Tool")
    print("           Coded by Broken Nadeem")
    print("=============================================\n")

    token_file = input("Enter path to token file      : ").strip()
    convo_id = input("Enter conversation ID         : ").strip()
    hater_uid = input("Enter hater's Facebook UID    : ").strip()
    message_file = input("Enter path to message file    : ").strip()
    try:
        delay = float(input("Enter delay in seconds        : ").strip())
    except:
        delay = 2
        print("[!] Invalid delay. Defaulting to 2 seconds.")

    tokens = load_file_lines(token_file)
    messages = load_file_lines(message_file)

    if not tokens:
        print("[!] No tokens loaded.")
        exit()
    if not messages:
        print("[!] No messages loaded.")
        exit()

    print(f"\n[✓] Loaded {len(tokens)} tokens and {len(messages)} messages.")
    print("[✓] Starting spam...\n")

    start_spamming(tokens, messages, convo_id, hater_uid, delay)
