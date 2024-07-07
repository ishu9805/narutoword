import asyncio
from pyrogram import Client, filters

# Replace with your bot token, API ID, and API hash
API_ID = 26692918
API_HASH = '2b239375e141e882a33b59820ce827be'
BOT_TOKEN = '7252582504:AAGWmkVkD-mAc6zhw87ZyRa9e2GWHIbNvzk'

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

spamming = False

@app.on_message(filters.command("start") & filters.group)
async def start(client, message):
    if message.from_user.id in [2079602485, 6257270528]:
        await message.reply("Welcome! I'm a spam bot. Use `/spam <number> <message>` to spam a message.")


@app.on_message(filters.text & filters.group)
async def respond_hi(client, message):
    await message.reply("hi")


@app.on_message(filters.command("spam") & filters.group)
async def spam(client, message):
    if message.from_user.id in [2079602485, 6257270528]:
        global spamming
        if spamming:
            await message.reply("Spamming is already in progress. Use `/stop` to stop spamming.")
            return
        if len(message.command) < 3:
            await message.reply("Usage: /spam <number> <message>")
            return
        try:
            num = int(message.command[1])
            if num <= 0:
                await message.reply("Number must be greater than 0.")
                return
            text = " ".join(message.command[2:])
            spamming = True
            for _ in range(num):
                await message.reply(text)
            spamming = False
        except ValueError:
            await message.reply("Invalid number. Please enter a valid integer.")

@app.on_message(filters.command("stop") & filters.group)
async def stop(client, message):
    if message.from_user.id in [2079602485, 6257270528]:
        global spamming
        spamming = False
        await message.reply("Spamming stopped.")

app.run()
