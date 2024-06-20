import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import RPCError

# API credentials
api_id = 26692918
api_hash = '2b239375e141e882a33b59820ce827be'
session_string = 'BQGg49sAjWbjcPwVZUcFUiqBTq7SrusShC_RojE3mFKlFc-6KgVTWVaVneXNvB_fVxonph_jG8YxiVaP62w6KF64gqzCo2HlnFnF8a1zxfkoogwzcJ25sqKgrv5RFLiqkfrXuF-bG-QGzRkfRpKLJKPB48FMS2_B9srFWL-Pl672_edHtiGi2oK_bXJhAcJ7e80XdIQnpFgAbZTozftqTZW0kq7ulE_H1sqsxGCHcqrsYAAqpefogsMhcgsZ5_PUG3CZnuYqsvXii4EN9MqOC1KAHXU0rW14VlEPECiVa1zJHZtQgJXONFDjwrHJaL1wxoL1R4t8DgGekM0mpScW7FKQbHGQBAAAAAGTKcSMAA'
bot_token2 = 'BQFRgCwAJjP_Bvo9srkCxtBaXeiDfaQPGjdsjBl321WXSwm6ixT2LiAlualCOFMpS4VYN-Ibb2foJhsckyTE0HE0q-R95km4dzT6qysStD35dNMxhYrE416LlhW4NW...'

HANDLER = "."
processed_results = set()
stop_scraping = False  # Initialize stop_scraping globally

app = Client("my_bot", api_id=api_id, api_hash=api_hash, session_string=session_string)

@app.on_message(filters.command("stoped", HANDLER) & filters.user(6257270528))
async def stop_message(client, message):
    global stop_scraping
    stop_scraping = True
    await message.reply("Stopping the bot...")

@app.on_message(filters.command("scrap", HANDLER) & filters.user(6257270528))
async def scrap_handler_self(client, message):
    global stop_scraping
    try:
        if len(message.command) < 2:
            await message.reply("Usage: .scrap [botusername]")
            return

        bot_username = message.command[1]
        chat_id = message.chat.id

        offset = ""
        while not stop_scraping:
            try:
                results = await client.get_inline_bot_results(bot=bot_username, query="", offset=offset)

                if results.results:
                    sorted_results = sorted(results.results, key=lambda x: x.id)  # Sort results by ID
                    for result in sorted_results:
                        result_id = result.id
                        if result_id in processed_results:
                            continue  # Skip sending if result is already processed

                        await client.send_inline_bot_result(chat_id, results.query_id, result_id)
                        processed_results.add(result_id)
                        await asyncio.sleep(2)  # Adjust delay as needed

                    # Check if there are more results
                    if results.next_offset:
                        offset = results.next_offset
                    else:
                        break  # No more results to fetch

                else:
                    await client.send_message(chat_id, "No results found.")
                    break

            except RPCError as e:
                await client.send_message(chat_id, f"Error occurred while querying: {e}")
                await asyncio.sleep(10)  # Delay before retrying in case of RPC errors

            except Exception as e:
                await client.send_message(chat_id, f"Unexpected error: {e}")
                break

    finally:
        stop_scraping = False  # Reset stop flag after scraping ends

@app.on_message(filters.command("scrap2", HANDLER) & filters.user(6257270528))
async def scrap2_handler_self(client, message):
    global stop_scraping
    try:
        if len(message.command) < 3:
            await message.reply("Usage: .scrap2 [botusername] [query]")
            return

        bot_username = message.command[1]
        query = message.command[2]
        chat_id = message.chat.id

        offset = ""
        while not stop_scraping:
            try:
                results = await client.get_inline_bot_results(bot=bot_username, query=query, offset=offset)

                if results.results:
                    sorted_results = sorted(results.results, key=lambda x: x.id)  # Sort results by ID
                    for result in sorted_results:
                        result_id = result.id
                        if result_id in processed_results:
                            continue  # Skip sending if result is already processed

                        await client.send_inline_bot_result(chat_id, results.query_id, result_id)
                        processed_results.add(result_id)
                        await asyncio.sleep(2)  # Adjust delay as needed

                    # Check if there are more results
                    if results.next_offset:
                        offset = results.next_offset
                    else:
                        break  # No more results to fetch

                else:
                    await client.send_message(chat_id, "No results found.")
                    break

            except RPCError as e:
                await client.send_message(chat_id, f"Error occurred while querying: {e}")
                await asyncio.sleep(10)  # Delay before retrying in case of RPC errors

            except Exception as e:
                await client.send_message(chat_id, f"Unexpected error: {e}")
                break

    finally:
        stop_scraping = False  # Reset stop flag after scraping ends

if __name__ == "__main__":
    app.run()
