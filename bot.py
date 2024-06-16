from pyrogram import Client, filters
from pymongo import MongoClient

# Environment variables
MONGO_URI = "mongodb+srv://naruto:hinatababy@cluster0.rqyiyzx.mongodb.net/"
GROUP_ID = -1002212863321  # Target group ID

# Initialize Pyrogram Client
api_id = 26692918
api_hash = '2b239375e141e882a33b59820ce827be'
bot_token = 'BQE--bQAjqHoV0hhvb27cizIgWfl0kHrwKwmGGHyZCP8D65FYLSLm993AOCg5G-xuoCHWPv32qaZfndeeKKo62IpOQc1Wv7Xj7ga2DAYq94D05JdL5pwk5plwdCXQdcBIFFlPIIigEN3ky57nJq_8k6d9qWQSC0m5NqX5gIEbMUfKzspp27zqdXy1WAr_D-Ykxi27CEWAEI9YHqWQe9Ox2OLIbuIzAM6Gzampsub4JisFCxewwE1BUA7COgc4Vvf6zV98AYKd167UPqVhwZEuAF2DJUbNDTw_NFEksUh5Y5oCdRtv4axpdJFpdZ0cocfl-zNkKLDt9oVfQA1Brh9oIzZhBgIkAAAAAF09l8AAA'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, session_string=bot_token)

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['image_search_db']
images_collection = db['images']

async def from_specific_user_and_photo(_, __, message):
    return message.from_user.id == 6670446530 and message.photo

# Event handler for handling messages from specific user containing photo
@app.on_message(filters.create(from_specific_user_and_photo))
async def handle_photo_message(client, message):
    file_unique_id = message.photo.file_unique_id

    # Check if the photo's details are in the database
    image_data = images_collection.find_one({"file_unique_id": file_unique_id})

    if image_data:
        character_name = image_data.get("character_name")
        response_text = f"/catch {character_name}"
        await message.reply_text(response_text)
    else:
        pass

        



# Start the bot
app.run()
