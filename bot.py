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
HEXAMON = -1002212863321
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



import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

@app.on_message(filters.group & filters.user(572621020))
async def forward_message(client, message):
    chat_id = message.chat.id

    if message.text and "The pokemon was" in message.text:
        forward_text = f"Chat ID: {chat_id}\n\n{message.text}"
        await client.send_message(HEXAMONS, forward_text)

    if message.photo:
        
        if message.caption and "Who's that pokemon?" in message.caption:
            file_unique_id = message.photo.file_unique_id
            image_data = images_collection.find_one({"file_unique_id": file_unique_id})
            if not image_data:
                forward_caption = f"Chat ID: {chat_id}\n\n{message.caption}"
                await client.send_photo(HEXAMONS, message.photo.file_id, caption=forward_caption)
            else:
                pass 
          
        elif not message.caption:
            return




app.run()
