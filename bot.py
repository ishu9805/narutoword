import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import RPCError

# API credentials
api_id = 26692918
api_hash = '2b239375e141e882a33b59820ce827be'
bot_token = 'BQGg49sAjWbjcPwVZUcFUiqBTq7SrusShC_RojE3mFKlFc-6KgVTWVaVneXNvB_fVxonph_jG8YxiVaP62w6KF64gqzCo2HlnFnF8a1zxfkoogwzcJ25sqKgrv5RFLiqkfrXuF-bG-QGzRkfRpKLJKPB48FMS2_B9srFWL-Pl672_edHtiGi2oK_bXJhAcJ7e80XdIQnpFgAbZTozftqTZW0kq7ulE_H1sqsxGCHcqrsYAAqpefogsMhcgsZ5_PUG3CZnuYqsvXii4EN9MqOC1KAHXU0rW14VlEPECiVa1zJHZtQgJXONFDjwrHJaL1wxoL1R4t8DgGekM0mpScW7FKQbHGQBAAAAAGTKcSMAA'
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
    """Handle replies to image messages with the specific caption to fetch details."""

    if message.caption and "Who's that pokemon?" in message.caption:
        file_unique_id = message.photo.file_unique_id
        image_data = images_collection.find_one({"file_unique_id": file_unique_id})

        if not image_data:
            logging.info("Image data not found in the database.")
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
    schedule.every(1).hour.do(send_guess_message)  # Send /guess message every 1 hour
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=schedule_guess_message).start()

app.run()
