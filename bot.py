import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import RPCError

# API credentials
api_id = 26692918
api_hash = '2b239375e141e882a33b59820ce827be'
bot_token = 'BQGXTTYAl9LCKhnR2dnseiZaRRkahybYgs7SSlHm9T2SBK4L_nvI_AmP1dcKvTAeMknsAVR5z7SuIooP3u5soXzTqkQS17eCm40GWorCjg8r2Sp1Lb3lWGBTNBdkVJgsezH2kUpSBdeKrU6moVUNYE-7G8RRxPiEKNenhYKq4ap9iIFpeSyt-0HXGLiWmo8KRTw7FNuLGKNiv4T6nOIUpyxUZzj2eLtoRnU-ynjylRQ7-bb75Kt8fH4o3lhq5wBtp513EKt6ZvwB5akKKW7tKlr3X0BU1DSHDiuk0MeXB4BToN-6UD278XUGuFzfbvXuNOKGUwai9N3yDCsj4CHN-b2iXZmUFgAAAAF09l8AAA'
bot_token2 = 'BQFRgCwAJjP_Bvo9srkCxtBaXeiDfaQPGjdsjBl321WXSwm6ixT2LiAlualCOFMpS4VYN-Ibb2foJhsckyTE0HE0q-R95km4dzT6qysStD35dNMxhYrE416LlhW4NW...'

import logging
import os
from pyrogram import Client, filters
from pymongo import MongoClient
import re
import time

# Environment variables
from collections import defaultdict
app = Client("my_bot", api_id=api_id, api_hash=api_hash, session_string=bot_token)

# Initialize Pyrogram Client

# Environment variables
MONGO_URI = 'mongodb+srv://naruto:hinatababy@cluster0.rqyiyzx.mongodb.net/'
GROUP_ID = -1002040871088  # Target group ID
DOWNLOAD_DIR = "downloads"
GROUP_ID2 = [-1002243288784, -1002029788751]
HEXAMON = [-1002212863321, -4213090659, -4286902153, -4227676670]
HEXAMONS = -1001854906826
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


import schedule
import threading

def send_guess_message():
    for chat_id in HEXAMON:
        app.send_message(chat_id, "/guess")

@app.on_message(filters.chat(HEXAMON) & filters.user([572621020]))
def get_image_details(client, message):
    if message.photo and "Who's that pokemon?" in message.caption:
        file_unique_id = message.photo.file_unique_id
        image_data = images_collection.find_one({"file_unique_id": file_unique_id})
        if not image_data:
            logging.info("Image data not found in the database.")
            chat_id = message.chat.id
            client.send_message(chat_id, "Waiting for the pokemon name...")
            @app.on_message(filters.chat(chat_id) & filters.user([572621020]))
            def wait_for_pokemon_name(client, message):
                if message.text and "The pokemon was" in message.text:
                    pokemon_name = message.text.split("The pokemon was")[1]
                    chat_id = -1002048925723
                    client.send_photo(chat_id, message.photo.file_id, caption=f"Character Name: {pokemon_name}\nAnime Name: Pokemon")
        else:
            character_name = image_data.get("character_name")
            response_text = f"c{character_name}c"
            time.sleep(5)
            client.send_message(chat_id=message.chat.id, text=response_text)


def schedule_guess_message():
    schedule.every(10).minutes.do(send_guess_message)  # Send /guess message every 1 hour
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=schedule_guess_message).start()

app.run()
