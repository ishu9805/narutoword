import logging
import os
from pyrogram import Client, filters
from pymongo import MongoClient
import re
# Environment variables


# Initialize Pyrogram Client
api_id = 26692918
api_hash = '2b239375e141e882a33b59820ce827be'
bot_token = 'BQE--bQAjqHoV0hhvb27cizIgWfl0kHrwKwmGGHyZCP8D65FYLSLm993AOCg5G-xuoCHWPv32qaZfndeeKKo62IpOQc1Wv7Xj7ga2DAYq94D05JdL5pwk5plwdCXQdcBIFFlPIIigEN3ky57nJq_8k6d9qWQSC0m5NqX5gIEbMUfKzspp27zqdXy1WAr_D-Ykxi27CEWAEI9YHqWQe9Ox2OLIbuIzAM6Gzampsub4JisFCxewwE1BUA7COgc4Vvf6zV98AYKd167UPqVhwZEuAF2DJUbNDTw_NFEksUh5Y5oCdRtv4axpdJFpdZ0cocfl-zNkKLDt9oVfQA1Brh9oIzZhBgIkAAAAAF09l8AAA'
bot_token2 = 'BQFRgCwAJjP_Bvo9srkCxtBaXeiDfaQPGjdsjBl321WXSwm6ixT2LiAlualCOFMpS4VYN-Ibb2foJhsckyTE0HE0q-R95km4dzT6qysStD35dNMxhYrE416LlhW4NWrpohqRRyYR9XkZGd2445ocaw-ybUusLoaMdMfj01uNZSA0DlnBgb9vyiX_sh6zbZPvlznnJkDT4EhyTwfyLx7Kg4_c2d5WOe7f_JXkazqaamPUmq8E7RoU4U2pe0SwsfLZCkf9qf497pdfuhLqrE_WEk3YsyB7SEca6laku5wpcOo63BcAclnpWGd5t-Kt8-pZTXG5wzQt3UFJ32pqkZmOmYZGg_mVEgAAAAGnyL7yAA'
app = Client("my_bot", api_id=api_id, api_hash=api_hash, session_string=bot_token)


# Environment variables
MONGO_URI = os.getenv("MONGO_URI")
GROUP_ID = -1002040871088 # Target group ID
DOWNLOAD_DIR = "downloads"
GROUP_ID2 = [-1002243288784, -1002029788751]
# Initialize Pyrogram Client
HEXAMON = -1002189762536
# Connect to MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['image_search_db']
images_collection = db['images']
pokemon_collection = db['poki']

# Create download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Initialize logging
logging.basicConfig(level=logging.INFO)

def extract_special_command_from_caption(caption):
    """Extract special command starting with / from the caption."""
    if not caption:
        return None
    
    words = caption.split()
    for word in words:
        if word.startswith('/'):
            return word.lower()  # Return the command in lowercase
    
    return None


@app.on_message(filters.photo & filters.private & filters.user([6763528462, 6883098627, 6501935889, 7107840748, 6670446530, 6942284208, 6501935889]))
def get_image_details(client, message):
    """Handle replies to image messages with the 'name' command to fetch details."""
    
    file_unique_id = message.photo.file_unique_id
    image_data = images_collection.find_one({"file_unique_id": file_unique_id})

    if not image_data:
        logging.info("Image data not found in the database.")
        return

    character_name = image_data.get("character_name")
    anime_name = image_data.get("anime_name")

    command = extract_special_command_from_caption(message.caption) if message.caption else None

    if command:
        response_text = f"{command} {character_name}"
        message.reply_text(response_text)
    else:
        pass


@app.on_message(filters.photo & filters.chat(HEXAMON) & filters.user([572621020]))
def get_image_details(client, message):
    """Handle replies to image messages with the 'name' command to fetch details."""
    
    file_unique_id = message.photo.file_unique_id
    image_data = images_collection.find_one({"file_unique_id": file_unique_id})

    caption = f"Character Name: \nAnime Name: Pokemon"
    if not image_data:
        # If no details found, send the photo to the specified group
        client.send_photo(chat_id=GROUP_ID, photo=replied_message.photo.file_id, caption=caption
        return                  
    character_name = image_data.get("character_name")
    anime_name = image_data.get("anime_name")

    
        response_text = f"{character_name}"
        message.reply_text(response_text)


app.run()
