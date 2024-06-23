import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import RPCError

# API credentials
api_id = 26692918
api_hash = '2b239375e141e882a33b59820ce827be'
bot_token = 'BQGXTTYAl9LCKhnR2dnseiZaRRkahybYgs7SSlHm9T2SBK4L_nvI_AmP1dcKvTAeMknsAVR5z7SuIooP3u5soXzTqkQS17eCm40GWorCjg8r2Sp1Lb3lWGBTNBdkVJgsezH2kUpSBdeKrU6moVUNYE-7G8RRxPiEKNenhYKq4ap9iIFpeSyt-0HXGLiWmo8KRTw7FNuLGKNiv4T6nOIUpyxUZzj2eLtoRnU-ynjylRQ7-bb75Kt8fH4o3lhq5wBtp513EKt6ZvwB5akKKW7tKlr3X0BU1DSHDiuk0MeXB4BToN-6UD278XUGuFzfbvXuNOKGUwai9N3yDCsj4CHN-b2iXZmUFgAAAAF09l8AAA'
bot_token2 = 'BQGXTTYAFI81Eo8Ig6Td_69GZM23ttzftPtc9SLRyPBaA626sCmkyQN0-L2PBgD235-bYVAxTtjAz2g2rDyg0iT2M0JAtvHUF3IYzTWbkIMpJf4gWAQnG-jHVVxBsijZcaIYULNLHenvn5WmqVmkfzEUeH5O4JxrY-Gz9K5CPVy3WKk9HjwDK0wO0lhldX1QOGqLkMKzcm4eiv_x9_eB3QnbtI_Ff7vD-2utNVVRHszp4nXBkLFMryqh7r8CvSeFPULW1IrpB5nNNkNxfQwp3YwIGecY3yjQkuhOGrpTI1kSrMmBtOCr9qlm9D2iSFNqkQuLl2_-g2J9D2j_k5SrvA--IV8NygAAAAFdFunlAA'

import logging
import os
from pyrogram import Client, filters
from pymongo import MongoClient
import re
import time

# Environment variables
from collections import defaultdict
app = Client("my_bot", api_id=api_id, api_hash=api_hash, session_string=bot_token)
app2 =Client("my_boot", api_id=api_id, api_hash=api_hash, session_string=bot_token2)
# Initialize Pyrogram Client

# Environment variables
MONGO_URI = 'mongodb+srv://naruto:hinatababy@cluster0.rqyiyzx.mongodb.net/'
GROUP_ID = -1002040871088  # Target group ID
DOWNLOAD_DIR = "downloads"
GROUP_ID2 = [-1002243288784, -1002029788751]
HEXAMON = [-1002212863321, -4213090659, -4286902153, -1002237969026, -1002189762536]
HEXAMONS = -1002048925723
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
        app2.send_message(chat_id, "/guess@HeXamonbot")

@app.on_message(filters.chat(HEXAMON) & filters.user([572621020]))
def get_image_details(client, message):
    """Handle replies to image messages with the specific caption to fetch details."""
    chat_id = message.chat.id
    if message.caption and "Who's that pokemon?" in message.caption:
        file_unique_id = message.photo.file_unique_id
        image_data = images_collection.find_one({"file_unique_id": file_unique_id})
        chat_id = message.chat.id
        if not image_data:
            chat_id = message.chat.id
            logging.info("Image data not found in the database.")
            forward_caption = f"Chat ID: {chat_id}\n\n{message.caption}"
            client.send_photo(chat_id, message.photo.file_id, caption=forward_caption)
            return

        character_name = image_data.get("character_name")

        response_text = f"{character_name}"
        time.sleep(2)
        client.send_message(chat_id=message.chat.id, text=response_text)
    else:
        logging.info("Caption does not contain the required text.")

    chat_id = message.chat.id
    if message.text and "The pokemon was" in message.text:
       
        forward_text = f"/guess"
        time.sleep(1)
        client.send_message(chat_id, forward_text)
        
def schedule_guess_message():
    schedule.every(2).minutes.do(send_guess_message)  # Send /guess message every 3 minutes
    while True:
        schedule.run_pending()
        time.sleep(1)


threading.Thread(target=schedule_guess_message).start()


app.run()
app2.run()
