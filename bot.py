import os
from pyrogram import Client, filters
from pymongo import MongoClient

# Environment variables
MONGO_URI = os.getenv("MONGO_URI")
GROUP_ID = -1002212863321  # Target group ID
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

# Function to extract character name from message text
def extract_character_name(text):
    if "The pokemon was" in text:
        return text.split("The pokemon was")[1].strip()
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

        # Update awaited_message with the received message
        awaited_message = message

# Event handler to process awaited message reply in groups
@app.on_message(filters.group & filters.user(572621020) & filters.reply)
async def process_awaited_message(client, message):
    global awaited_message
    if awaited_message and awaited_message.message_id == message.reply_to_message.message_id:
        file_unique_id = awaited_message.photo.file_unique_id
        chat_id = awaited_message.chat.id

        # Extract character name from the awaited message reply
        character_name = extract_character_name(message.text) if message.text else "Unknown"

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

        # Reset awaited_message
        awaited_message = None

# Start the bot
app.run()
