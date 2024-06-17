import os
import re
from pyrogram import Client, filters
from pymongo import MongoClient

# Environment variables
MONGO_URI = "mongodb+srv://naruto:hinatababy@cluster0.rqyiyzx.mongodb.net/"
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
pokemon = db['poki']

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def extract_character_name(text):
    if "The pokemon was" in text:
        return text.split("The pokemon was")[1].strip()
    return None

async def from_specific_user_and_photo(_, __, message):
    return message.from_user.id == 572621020 and message.photo

# Event handler for handling messages from specific user containing photo
@app.on_message(filters.create(from_specific_user_and_photo))
async def handle_photo_message(client, message):
    file_unique_id = message.photo.file_unique_id
    chat_id = message.chat.id
    # Check if the photo's details are in the database
    image_data = images_collection.find_one({"file_unique_id": file_unique_id})

    if image_data:
        character_name = image_data.get("character_name")
        response_text = f"{character_name}"
        await message.reply_text(response_text)
    else:
        photo_path = await message.download(file_name=os.path.join(DOWNLOAD_DIR, f"{file_unique_id}.jpg"))

        # Extract character name from the latest messages containing the specific format
        character_name = None
        
        async def wait_for_message():
            while True:
                msg = await app.listen(filters.user(572621020) & filters.text)
                if msg.text and "The pokemon was" in msg.text:
                    return msg
        
        msg = await wait_for_message()
        
        character_name = extract_character_name(msg.text) if msg else None


        # If character name was not found, use a default value
        if not character_name:
            character_name = "Unknown"

        # Save the extracted data to the database
        pokemon.insert_one({
            "file_unique_id": file_unique_id,
            "chat_id": chat_id,
            "character_name": character_name
        })

        # Construct the caption
        caption = f"Character Name: {character_name}\nAnime Name: Pokemon"


        # Send the photo to the specified group with the caption
        await client.send_photo(chat_id, photo_path, caption=caption)

        # Clean up the downloaded photo
        os.remove(photo_path)

        
async def from_specific_user_and_photos(_, __, message):
    return message.from_user.id == 6501935889 and message.photo

@app.on_message(filters.create(from_specific_user_and_photos))
async def handle_photo_message(client, message):
    file_unique_id = message.photo.file_unique_id

    # Check if the photo's details are in the database
    image_data = images_collection.find_one({"file_unique_id": file_unique_id})

    if image_data:
        character_name = image_data.get("character_name")
        response_text = f"/slave {character_name}"
        await message.reply_text(response_text)
    else:
        pass
# Start the bot
app.run()
