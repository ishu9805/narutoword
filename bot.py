import asyncio
from pyrogram import Client, filters

# Replace with your bot token, API ID, and API hash
API_ID = 26692918
API_HASH = '2b239375e141e882a33b59820ce827be'
BOT_TOKEN = 'BQGXTTYArKeeIvZRF9K8uhIx93UpYwdAXoeHCFo1QA5LX5g6uKkHBSfRKRTv7Jem1QQ_W4Y7Cvn_nS39VOitcHw1S09ZosZ0Hno4ilnQO-Z0AHkjlfC1pFRdIOHmJdjXvar5uqG9Y85C8BPB7ZAnhOD8DppaZJbcjKwfzqb-_CmW580NueH1YrVHOMuXpH3XWjx1lG5cd12d70fA6M_Mit2wJHVMaiLtvv4-DI3mJxbSsVedWN_WzfzCzj9wkxPFKGV3oHTLdoGGz4dQBusMcTQxFbBRDvSqeeQ50nS-POuXFr94xAGK8z3qj0OA9ciCIlyQvRMNIvJzMVlFJnKFaTlAjFyU-QAAAAFdFunlAA'

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, session_string=BOT_TOKEN)

spamming = False

@app.on_message(filters.command("start") & filters.group)
async def start(client, message):
    if message.from_user.id in [2079602485, 6257270528]:
        await message.reply("Welcome! I'm a spam bot. Use `/spam <number> <message>` to spam a message.")


@app.on_message(filters.text & filters.group)
async def respond_hi(client, message):
    if message.text.startswith("Naruto spam time "):
        count = int(message.text.split()[-1])
        for _ in range(count):
            await message.reply(".")
    else:
        await message.reply("hi")


app.run()
