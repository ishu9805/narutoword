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
@app.on_message(filters.photo & filters.user()
def get_image_details(client, message: Message):
    """Handle replies to image messages with the 'name' command to fetch details."""
    
    replied_message = message.reply_to_message

    if not replied_message or not replied_message.photo:
        return

    file_unique_id = replied_message.photo.file_unique_id

    image_data = images_collection.find_one({"file_unique_id": file_unique_id})

    if not image_data:
        pass
        except Exception as e:
            logging.error(f"Failed to send photo to group: {e}")
        return 

    character_name = image_data.get("character_name")
    anime_name = image_data.get("anime_name")

    if replied_message.caption:
        command = extract_special_command_from_caption(replied_message.caption)
    else:
        command = None

    if command:
        response_text = (
            f"{command} {character_name}"
        )
     else: 
         pass message.reply_text(response_text)

app.run()
