import logging
import os
from pyrogram import Client, filters
from pymongo import MongoClient
import re
import time
# Environment variables
from collections import defaultdict

# Initialize Pyrogram Client
api_id = 26692918
api_hash = '2b239375e141e882a33b59820ce827be'
bot_token = 'BQE--bQAjqHoV0hhvb27cizIgWfl0kHrwKwmGGHyZCP8D65FYLSLm993AOCg5G-xuoCHWPv32qaZfndeeKKo62IpOQc1Wv7Xj7ga2DAYq94D05JdL5pwk5plwdCXQdcBIFFlPIIigEN3ky57nJq_8k6d9qWQSC0m5NqX5gIEbMUfKzspp27zqdXy1WAr_D-Ykxi27CEWAEI9YHqWQe9Ox2OLIbuIzAM6Gzampsub4JisFCxewwE1BUA7COgc4Vvf6zV98AYKd167UPqVhwZEuAF2DJUbNDTw_NFEksUh5Y5oCdRtv4axpdJFpdZ0cocfl-zNkKLDt9oVfQA1Brh9oIzZhBgIkAAAAAF09l8AAA'
bot_token2 = 'BQFRgCwAJjP_Bvo9srkCxtBaXeiDfaQPGjdsjBl321WXSwm6ixT2LiAlualCOFMpS4VYN-Ibb2foJhsckyTE0HE0q-R95km4dzT6qysStD35dNMxhYrE416LlhW4NWrpohqRRyYR9XkZGd2445ocaw-ybUusLoaMdMfj01uNZSA0DlnBgb9vyiX_sh6zbZPvlznnJkDT4EhyTwfyLx7Kg4_c2d5WOe7f_JXkazqaamPUmq8E7RoU4U2pe0SwsfLZCkf9qf497pdfuhLqrE_WEk3YsyB7SEca6laku5wpcOo63BcAclnpWGd5t-Kt8-pZTXG5wzQt3UFJ32pqkZmOmYZGg_mVEgAAAAGnyL7yAA'
app = Client("my_bot", api_id=api_id, api_hash=api_hash, session_string=bot_token)




# Group chat ID
group_chat_id = -1002048925723

# Initialize the Client


@app.on_message(filters.command("waifu"))
async def get_bot_results(client, message):
    # Get inline bot results
    results = await client.get_inline_bot_results("@Hunt_Your_Waifu_Bot", query="waifu")
    
    # Limit to 5 results and send them to the group
    for result in results.results[:5]:
        if result.type == "photo":
            photo = result.photo
            if photo:
                message_text = f"File Unique ID: {photo.file_unique_id}, File Name: {photo.file_name}"
                await client.send_message(group_chat_id, message_text)

# Run the app
app.run()
