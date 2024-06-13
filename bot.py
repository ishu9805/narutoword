import re
import random
from telethon import events
from . import Blade_cmd, Blade_bot

# Define regex patterns
starting_letter_pattern = r"start with ([A-Z])"
min_length_pattern = r"include at least (\d+) letters"
trigger_pattern = r"Turn: 〨 Nᴀʀᴜᴛᴏ ؜Ꮶɪɴɢ ⌯؜ Ꮓx..*"
accepted_pattern = r"(\w+) is accepted"
not_in_list_pattern = r"(\w+) is not in my list of words"

# Dictionary to keep track of used words per group
used_words_dict = {}
# Set to keep track of blacklisted words
blacklist = set()

def fetch_words():
    """Fetch words from a local wordlist.txt file and filter them."""
    with open("wordlist.txt", "r") as file:
        words_alpha = set(file.read().splitlines())
    
    # Include words containing only alphabetic characters
    pattern = re.compile(r"^[a-zA-Z]+$")
    words_alpha_filtered = {re.sub(r"[-',]", "", word) for word in words_alpha if pattern.match(re.sub(r"[-',]", "", word))}
    
    return words_alpha_filtered

@Blade_cmd(pattern="ping")
async def ping(event):
    """Reply to a ping command with pong."""
    await event.reply("pong!")

@Blade_cmd(pattern="resetwords")
async def reset_used_words(event):
    """Reset the used words list for the current chat."""
    global used_words_dict
    chat_id = event.chat_id
    used_words_dict[chat_id] = set()
    await event.reply("Used words list has been reset for this chat.")

@Blade_cmd(pattern="resetallwords")
async def reset_all_used_words(event):
    """Reset the used words list for all chats."""
    global used_words_dict
    used_words_dict.clear()
    await event.reply("Used words list has been reset for all chats.")

@Blade_cmd(pattern="generatewordlist")
async def generate_wordlist(event):
    """Generate a filtered wordlist and send it as a file."""
    words = fetch_words()
    
    # Filter out words containing non-alphabetic characters
    pattern = re.compile(r"^[a-zA-Z]+$")
    filtered_words = {word for word in words if pattern.match(word)}
    
    with open("wordlist_filtered.txt", "w") as file:
        for word in filtered_words:
            file.write(word + "\n")
    
    await event.client.send_file(event.chat_id, "wordlist_filtered.txt")

@Blade_bot.on(events.NewMessage(pattern=trigger_pattern))
async def handle_incoming_message(event):
    """Handle incoming messages matching the trigger pattern."""
    puzzle_text = event.raw_text
    chat_id = event.chat_id

    # Initialize used words set for the chat if it doesn't exist
    if chat_id not in used_words_dict:
        used_words_dict[chat_id] = set()

    # Fetch words
    words = fetch_words()
    
    # Check if the message matches the accepted pattern
    accepted_match = re.search(accepted_pattern, puzzle_text)
    if accepted_match:
        accepted_word = re.sub(r"[-',]", "", accepted_match.group(1).lower())
        used_words_dict[chat_id].add(accepted_word)
        await Blade_bot.send_message("On9cheatbot", accepted_word)
        return
    
    # Check if the message matches the not in list pattern
    not_in_list_match = re.search(not_in_list_pattern, puzzle_text)
    if not_in_list_match:
        blacklisted_word = re.sub(r"[-',]", "", not_in_list_match.group(1).lower())
        blacklist.add(blacklisted_word)
        await event.reply(f"{blacklisted_word} has been added to the blacklist.")
        return

    # Extract criteria for word generation
    starting_letter_match = re.search(starting_letter_pattern, puzzle_text)
    min_length_match = re.search(min_length_pattern, puzzle_text)

    if starting_letter_match and min_length_match:
        starting_letter = starting_letter_match.group(1).lower()
        min_length = int(min_length_match.group(1))

        # Filter valid words based on criteria and excluding blacklisted words
        valid_words = [word for word in words if word.startswith(starting_letter) and len(word) >= min_length and word not in used_words_dict[chat_id] and word not in blacklist]

        if valid_words:
            # Randomly choose one word
            selected_word = random.choice(valid_words)
            
            # Add selected word to the set of used words
            used_words_dict[chat_id].add(selected_word)
            
            await event.reply(f"{selected_word}")
        else:
            await event.reply("No valid words found.")
    else:
        await event.reply("Invalid puzzle format.")
