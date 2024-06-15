import asyncio
import re
import os
from pyrogram import Client, filters
from threading import Thread
from flask import Flask

# Retrieve API credentials from environment variables
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("BOT_TOKEN")  # Using session string for userbot

# Initialize the Pyrogram client as a user bot
app = Client("word9", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
server = Flask(__name__)

@server.route("/")
def home():
    return "Bot is running"

# Define regex patterns
starting_letter_pattern = r"start with ([A-Z])"
min_length_pattern = r"include at least (\d+) letters"
trigger_pattern = r"Turn: 量­­‌؜「 Bʟᴀᴅᴇ 」؜⦁­­­឵ Nᴀʀᴜᴛᴏ.*"
accepted_pattern = r"(\w+) is accepted"
not_in_list_pattern = r"(\w+) is not in my list of words"
used_word_pattern = r"(\w+) has been used"
specific_bot_id = 7090700350  # Bot user ID to track accepted words

# Dictionary to keep track of used words per group
used_words_dict = {}
# Set to keep track of blacklisted words
blacklist = set()

# Define the user ID and the message patterns to trigger specific actions
user_id_to_watch = 6257270528
join_message_trigger = "Naruto join the game"
reset_message_trigger = "Naruto reset the used words"
command_to_send = "/join@on9wordchainbot"

@app.on_message(filters.group & filters.user(user_id_to_watch) & filters.regex(re.escape(join_message_trigger)))
async def handle_join_game_message(client, message):
    """Handle incoming messages from a specific user to trigger a join command in a group."""
    await client.send_message(message.chat.id, command_to_send)

@app.on_message(filters.group & filters.user(user_id_to_watch) & filters.regex(re.escape(reset_message_trigger)))
async def handle_reset_used_words_message(client, message):
    """Handle incoming messages from a specific user to reset the used words list for all chats."""
    global used_words_dict
    used_words_dict.clear()
    await message.reply_text("ho gya ab fir se khelein.")

def fetch_words():
    """Fetch words from the wordlist.txt file and filter them."""
    with open("wordlist.txt", "r") as file:
        words = set(word.strip().lower() for word in file if word.strip().isalpha())
    return words

@app.on_message(filters.me & filters.command("ping"))
async def ping(client, message):
    """Reply to a ping command with pong."""
    await message.reply_text("pong!")

@app.on_message(filters.me & filters.command("resetwords"))
async def reset_used_words(client, message):
    """Reset the used words list for the current chat."""
    global used_words_dict
    chat_id = message.chat.id
    used_words_dict[chat_id] = set()
    await message.reply_text("ye bhi ho gya.")

@app.on_message(filters.me & filters.command("resetallwords"))
async def reset_all_used_words(client, message):
    """Reset the used words list for all chats."""
    global used_words_dict
    used_words_dict.clear()
    await message.reply_text("ho gya ab khelein.")

@app.on_message(filters.me & filters.command("generatewordlist"))
async def generate_wordlist(client, message):
    """Generate a filtered wordlist and send it as a file."""
    words = fetch_words()
    
    # Save to a file
    with open("wordlist_filtered.txt", "w") as file:
        for word in words:
            file.write(word + "\n")
    
    await client.send_document(message.chat.id, "wordlist_filtered.txt")

@app.on_message(filters.regex(trigger_pattern))
async def handle_incoming_message(client, message):
    """Handle incoming messages matching the trigger pattern."""
    puzzle_text = message.text
    chat_id = message.chat.id

    # Initialize used words set for the chat if it doesn't exist
    if chat_id not in used_words_dict:
        used_words_dict[chat_id] = set()

    # Fetch words
    words = fetch_words()
    
    # Extract criteria for word generation
    starting_letter_match = re.search(starting_letter_pattern, puzzle_text)
    min_length_match = re.search(min_length_pattern, puzzle_text)

    if starting_letter_match and min_length_match:
        starting_letter = starting_letter_match.group(1).lower()
        min_length = int(min_length_match.group(1))

        while True:
            # Filter valid words based on criteria and excluding blacklisted and used words
            valid_words = [word for word in words if word.startswith(starting_letter) and len(word) >= min_length and word not in blacklist and word not in used_words_dict[chat_id]]

            if valid_words:
                # Find the smallest word
                selected_word = min(valid_words, key=len)
                
                # Check if the selected word has already been used
                if selected_word in used_words_dict[chat_id]:
                    continue
                else:
                    # Send the selected word
                    await asyncio.sleep(3)
                    await message.reply_text(f"{selected_word}")

                    # Add the selected word to the used words list
                    used_words_dict[chat_id].add(selected_word)

                    break
            else:
                await message.reply_text("No valid words found.")
                break
    else:
        await message.reply_text("Invalid puzzle format.")

@app.on_message(filters.user(specific_bot_id) & filters.regex(accepted_pattern))
async def track_accepted_words(client, message):
    """Track accepted words from the specific bot and add to the used words list."""
    chat_id = message.chat.id
    message_text = message.text

    if chat_id not in used_words_dict:
        used_words_dict[chat_id] = set()

    accepted_match = re.search(accepted_pattern, message_text)
    if accepted_match:
        accepted_word = re.sub(r"[-',]", "", accepted_match.group(1).lower())
        used_words_dict[chat_id].add(accepted_word)

def run():
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    app.run()
