

# Initialize Pyrogram Client
api_id = 26692918
api_hash = '2b239375e141e882a33b59820ce827be'
string = 'BQE--bQAjqHoV0hhvb27cizIgWfl0kHrwKwmGGHyZCP8D65FYLSLm993AOCg5G-xuoCHWPv32qaZfndeeKKo62IpOQc1Wv7Xj7ga2DAYq94D05JdL5pwk5plwdCXQdcBIFFlPIIigEN3ky57nJq_8k6d9qWQSC0m5NqX5gIEbMUfKzspp27zqdXy1WAr_D-Ykxi27CEWAEI9YHqWQe9Ox2OLIbuIzAM6Gzampsub4JisFCxewwE1BUA7COgc4Vvf6zV98AYKd167UPqVhwZEuAF2DJUbNDTw_NFEksUh5Y5oCdRtv4axpdJFpdZ0cocfl-zNkKLDt9oVfQA1Brh9oIzZhBgIkAAAAAF09l8AAA'
bot_token2 = 'BQFRgCwAJjP_Bvo9srkCxtBaXeiDfaQPGjdsjBl321WXSwm6ixT2LiAlualCOFMpS4VYN-Ibb2foJhsckyTE0HE0q-R95km4dzT6qysStD35dNMxhYrE416LlhW4NWrpohqRRyYR9XkZGd2445ocaw-ybUusLoaMdMfj01uNZSA0DlnBgb9vyiX_sh6zbZPvlznnJkDT4EhyTwfyLx7Kg4_c2d5WOe7f_JXkazqaamPUmq8E7RoU4U2pe0SwsfLZCkf9qf497pdfuhLqrE_WEk3YsyB7SEca6laku5wpcOo63BcAclnpWGd5t-Kt8-pZTXG5wzQt3UFJ32pqkZmOmYZGg_mVEgAAAAGnyL7yAA'




import os
import nest_asyncio
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors.rpcerrorlist import BotResponseTimeoutError, FloodWaitError
from telethon.tl.functions.messages import GetInlineBotResultsRequest
from telethon.tl.types import InputBotInlineMessageID

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Credentials

# Directory to save images and captions
save_dir = './waifu_images'
os.makedirs(save_dir, exist_ok=True)

# Set to keep track of processed result IDs
processed_ids = set()

async def main():
    # Create and start the client
    client = TelegramClient(StringSession(string), api_id, api_hash)
    await client.start()

    # Send a message to the bot to trigger inline results
    bot_username = 'Waifu_Grabber_Bot'
    query = ''  # Empty query to get default inline results

    downloaded_count = 0
    max_downloads = 3300
    offset = ''  # Initial offset is empty

    while downloaded_count < max_downloads:
        # Retry mechanism
        max_retries = 50000
        for attempt in range(max_retries):
            try:
                results = await client(GetInlineBotResultsRequest(
                    bot=bot_username,
                    peer='me',
                    query=query,
                    offset=offset
                ))
                break
            except BotResponseTimeoutError:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed, retrying...")
                    await asyncio.sleep(2)  # Wait before retrying
                else:
                    print("Max retries reached. The bot did not respond in time.")
                    return
            except FloodWaitError as e:
                print(f"Rate limit hit. Waiting for {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)

        # Process the inline results
        if not results.results:
            print("No more results in the current offset.")
            break

        for result in results.results:
            if result.type == 'photo' and result.id not in processed_ids:
                # Save the caption
                caption = result.send_message.message
                caption_file = os.path.join(save_dir, f"{result.id}.txt")
                with open(caption_file, 'w') as f:
                    f.write(caption)

                # Save the image
                photo = result.photo
                photo_file = os.path.join(save_dir, f"{result.id}.jpg")
                await client.download_media(photo, photo_file)

                # Mark this result as processed
                processed_ids.add(result.id)

                # Increment the downloaded count
                downloaded_count += 1

                # Add a delay between downloads to avoid rate limiting
                await asyncio.sleep(2)  # Adjust the delay as needed

                # Break if the maximum download count is reached
                if downloaded_count >= max_downloads:
                    break

        # Update the offset to get the next set of results only if there are no more results in the current offset
        if not results.results:
            offset = results.next_offset

        # Wait for a while before checking for new results
        await asyncio.sleep(60)  # Check every 60 seconds

    await client.disconnect()

# Run the main function
asyncio.run(main())p
