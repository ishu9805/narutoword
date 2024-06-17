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
bot_token = 'BQE--bQAjqHoV0hhvb27cizIgWfl0kHrwKwmGGHyZCP8D65FYLSLm993AOCg5G-xuoCHWPv32qaZfndeeKKo62IpOQc1Wv7Xj7ga2DAYq94D05JdL5pwk5plwdCXQdcBIFFlPIIigEN3ky57nJq_8k6d9qWQSC0m5NqX5gIEbMUfKzspp27zqdXy1WAr_D-Ykxi27CEWAEI9YHqWQe9Ox2OLIbuIzAM6Gzampsub4JisFCxewwE1BUA7COgc4Vvf6zV98AYKd167UPqVhwZEuAF2DJUbNDTw_NFEksUh5Y5oCdRtv4axpdJFpdZ0cocfl-zNkKLDt9oVfQA1Brh9oIzZhBgIkAAAAAF09l8AAA'

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
shared_data = {}

def extract_character_name(text):
    if "The pokemon was" in text:
        # Split by "The pokemon was" and take the second part
        character_name_part = text.split("The pokemon was")[1].strip()
        
        # Remove any additional characters that are not part of the name
        # Specifically, remove any characters after the first dot or other non-alphabetical character.
        cleaned_character_name = re.sub(r'[^\w\s]', '', character_name_part)
        
        return cleaned_character_name.strip()  # Return the cleaned character name

    return None  


# Shared variable to store the awaited message
awaited_message = None

# Event handler for messages from specific user containing photo in groups
@app.on_message(filters.group & filters.user(572621020) & filters.photo)
async def handle_photo_message(client, message):
    global awaited_message
    file_unique_id = message.photo.file_unique_id
    chat_id = message.chat.id
    
    # Check if the photo's details are in the database
    image_data = images_collection.find_one({"file_unique_id": file_unique_id})

    if image_data:
        character_name = image_data.get("character_name")
        response_text = f"{character_name}"
        await message.reply_text(response_text)
    else:
        # Download the photo
        photo_path = await message.download(file_name=os.path.join(DOWNLOAD_DIR, f"{file_unique_id}.jpg"))

        # Store photo_path in shared_data
        shared_data[file_unique_id] = photo_path

        # Update awaited_message with the received message
        awaited_message = message

# Event handler to process awaited message reply in groups
# Event handler to process awaited message reply in groups
@app.on_message(filters.group & filters.user(572621020) & filters.reply)
async def process_awaited_message(client, message):
    global awaited_message
    if awaited_message and awaited_message.id == message.reply_to_message.id:
        file_unique_id = awaited_message.photo.file_unique_id
        chat_id = awaited_message.chat.id

        # Extract character name from the awaited message reply
        character_name = extract_character_name(message.text) if message.text else "Unknown"

        print(f"Extracted character name: {character_name}")  # Print for debugging

        # Get photo_path from shared_data
        photo_path = shared_data.get(file_unique_id)

        if photo_path:
            # Save the extracted data to the database
            pokemon_collection.insert_one({
                "file_unique_id": file_unique_id,
                "chat_id": chat_id,
                "character_name": character_name
            })

            # Construct the caption
            caption = f"Character Name: {character_name}\nAnime Name: Pokemon"

            # Send the photo to the specified group with the caption
            await client.send_photo(GROUP_ID, photo=photo_path, caption=caption)

            # Clean up the downloaded photo
            os.remove(photo_path)

            # Reset awaited_message and remove photo_path from shared_data
            awaited_message = None
            del shared_data[file_unique_id]
        else:
            print(f"Error: photo_path not found for file_unique_id {file_unique_id}")

app.run()
