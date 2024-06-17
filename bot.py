import asyncio
import os
import zipfile
from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultPhoto

# Set up your Telegram API credentials
api_id = 26692918
api_hash = "2b239375e141e882a33b59820ce827be"
bot_token = "7461505284:AAFsqEwWww1GZakSa9oLyalchIY03PTLQu8"

# Create a Pyrogram Client
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


@app.on_message(filters.command("start"))
def start_message(client, message):
    client.send_message(message.chat.id, "Bot is started")
    
# Define a handler for inline queries
@app.on_inline_query()
async def inline_query_handler(client, inline_query):
    query = inline_query.query
    if not query:
        await inline_query.answer(results=[], cache_time=1)
        return

    # Example of querying another bot's inline results
    # Replace "OTHER_BOT_USERNAME" with the username of the bot you want to query
    other_bot_username = "Catch_Your_WH_Group"
    results = await client.get_inline_bot_results(other_bot_username, query)

    # Filter out image results and collect their metadata
    image_results = []
    for result in results.results:
        if isinstance(result, InlineQueryResultPhoto):
            image_results.append(result)

    # Prepare a zip file to store image metadata
    zip_file = 'bot.zip'
    with zipfile.ZipFile(zip_file, 'w') as zip_ref:
        for image in image_results:
            metadata_text = f"Image URL: {image.photo.url}\n"
            metadata_text += f"Thumb URL: {image.thumb_url}\n"
            metadata_text += f"Description: {image.description}\n"
            metadata_text += f"Title: {image.title}\n\n"

            # Write metadata to a temporary text file
            temp_file = f"{image.photo.file_id}.txt"
            with open(temp_file, 'w', encoding='utf-8') as temp:
                temp.write(metadata_text)

            # Add the temporary text file to the zip archive
            zip_ref.write(temp_file)
            
            # Remove the temporary text file after adding it to zip
            os.remove(temp_file)

    # Respond to the inline query with the zip file containing metadata files
    await inline_query.answer(
        results=[],
        cache_time=1,
        is_personal=True,
        switch_pm_text="Check your zip file",
        switch_pm_parameter="inline_query"
    )

# Start the bot
app.run()
