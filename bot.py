import asyncio
from pyrogram import Client, filters

# Replace with your bot token, API ID, and API hash
API_ID = 26692918
API_HASH = "2b239375e141e882a33b59820ce827be"
BOT_TOKEN = "7252582504:AAGWmkVkD-mAc6zhw87ZyRa9e2GWHIbNvzk"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Welcome! I'm a spam bot. Use `/spam <number> <message>` to spam a message.")

@app.on_message(filters.command("spam"))
async def spam(client, message):
    if len(message.command) < 3:
        await message.reply("Usage: /spam <number> <message>")
        return
    num = int(message.command[1])
    text = " ".join(message.command[2:])
    for _ in range(num):
        await message.reply(text)

async def main():
    await app.start()
    print("Bot started. Press Ctrl+C to stop.")
    await app.idle()

if __name__ == "__main__":
    asyncio.run(main())
