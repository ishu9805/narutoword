import os
from pyrogram import Client, filters
from pymongo import MongoClient
import re
# Environment variables
MONGO_URI = os.getenv("MONGO_URI")
GROUP_ID = -1002038805604  # Target group ID
DOWNLOAD_DIR = "downloads"

# Initialize Pyrogram Client
api_id = 26692918
api_hash = '2b239375e141e882a33b59820ce827be'
bot_token = 'BQGXTTYAJErYsrHBBpFttTJAVUOk3MTIdmL7o_gawxZakXe_oD3qKx5IPStZKAck7XMtpIZRDy22YrPSx7arEuzH1-9xl-rY5MQrby-FQwNPflh1JaxYX0XxA76TJx7aurpnQZL2es5t_qATD32RRYzc2vlprSXEC_kK9EDp5oeZbzmSccuXIbvAQXwOUbRv8eG8t-i4wshg8MmRMgRwu1qv2gsW8nivu_8JUEkkHrXFWYFVGizk-LpKOHa6TOG266tkLUopTGLSM8pZoYc013q1iYcYvNGUxFN5_73K00Z9-TjNwbmYQgR_TIUfBjudyj3kCDlGU8aylgCj8Sbj7QBCRiw_KQAAAAFdFunlAAXy1WAr_D-Ykxi27CEWAEI9YHqWQe9Ox2OLIbuIzAM6Gzampsub4JisFCxewwE1BUA7COgc4Vvf6zV98AYKd167UPqVhwZEuAF2DJUbNDTw_NFEksUh5Y5oCdRtv4axpdJFpdZ0cocfl-zNkKLDt9oVfQA1Brh9oIzZhBgIkAAAAAF09l8AAA'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, session_string=bot_token)

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['image_search_db']
images_collection = db['images']
pokemon_collection = db['poki']

# Create download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Dictionary to store photo_path temporarily
awaited_messages = {}


# Function to extract character name from message text
def extract_character_name(text):
    # Regex pattern to match the desired format
    pattern = r'The pokemon was ([\w\s]+)\.'
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    else:
        return "Unknown"

@app.on_message(filters.text)
async def handle_text_message(client, message):
    global awaited_messages

    # Check if the message text contains the specific pattern
    match = re.search(r'The pokemon was ([\w\s]+)\.', message.text)
    if match:
        character_name = match.group(1).strip()
        print(f"Extracted character name: {character_name}")  # Print for debugging

        # Check if there's an awaited message for this chat
        if message.chat.id in awaited_messages:
            awaited_message = awaited_messages[message.chat.id]
            file_unique_id = awaited_message.photo.file_unique_id
            photo_path = awaited_message.download(file_name=os.path.join(DOWNLOAD_DIR, f"{file_unique_id}.jpg"))

            # Save the extracted data to the database
            pokemon_collection.insert_one({
                "file_unique_id": file_unique_id,
                "chat_id": message.chat.id,
                "character_name": character_name
            })

            # Construct the caption
            caption = f"Character Name: {character_name}\nAnime Name: Pokemon"

            # Send the photo to the specified group with the caption
            await client.send_photo(GROUP_ID, photo=photo_path, caption=caption)

            # Clean up the downloaded photo
            os.remove(photo_path)

            # Remove awaited message from dictionary
            del awaited_messages[message.chat.id]
        else:
            print("No awaited message found for this chat.")  # Optionally log the event


# Event handler for messages containing photo
@app.on_message(filters.photo)
async def handle_photo_message(client, message):
    global awaited_messages

    # Store the message in awaited_messages
    awaited_messages[message.chat.id] = message

app.run()
