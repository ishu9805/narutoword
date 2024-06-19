import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import RPCError

# API credentials
api_id = 26692918
api_hash = '2b239375e141e882a33b59820ce827be'
session_string = 'BQEyNt4Alzxv5dWKPocOGEM5WDU4-sQwZwYiQIHT_qgcMHdYolcGJjfTVKov_6Fi5dmmdAvLh8UDQDXqCkWSeAjYvEYUjot2guNF-DtCXIMWKNQ85j3mRZ8kzkYBEhmDFnt0kOcmkAxI-h89JC0Uswh6frn7HfvWOn0nQhokeH1zCI9LdtxX0v_DSX3nD7-RoozDAKQ-XCrP345HUaM_x2NxUOERBqfwgFuK5TF50sTYxCdgUYPPepCJexgDPKXYLXFF6N6OVDL49hpt-aMD7_OBYVVUWr0RIVUfi2BEA1RNsiI_pNF0-WZkpFPlE_buoWBY-BOn9t4lH2-jntM8ZWJdbsn73QAAAAGYzZixAA'
bot_token2 = 'BQFRgCwAJjP_Bvo9srkCxtBaXeiDfaQPGjdsjBl321WXSwm6ixT2LiAlualCOFMpS4VYN-Ibb2foJhsckyTE0HE0q-R95km4dzT6qysStD35dNMxhYrE416LlhW4NW...'

HANDLER = "."
processed_results = set()
stop_scraping = False

app = Client("my_bot", api_id=api_id, api_hash=api_hash, session_string=session_string)


@app.on_message(filters.command("stoped", HANDLER) & filters.user(6257270528))
async def stop_message( client, message):
    global stop_scraping
    stop_scraping = True
    await message.reply("stoping the bot...")

@app.on_message(filters.command("scrap", HANDLER) & filters.user(6257270528))
@app.on_message(filters.command("scrap", HANDLER) & filters.me)
async def scrap_handler_self(client, message):
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
                    for result in results.results:
                        result_id = result.id
                        if result_id in processed_results:
                            continue  # Skip sending if result is already processed

                        await client.send_inline_bot_result(chat_id, results.query_id, result_id)
                        processed_results.add(result_id)
                        await asyncio.sleep(2)

                    # Check if there are more results
                    if results.next_offset:
                        offset = results.next_offset
                    else:
                        break  # No more results to fetch

                else:
                    await client.send_message(chat_id, f"No results found.")

            except RPCError as e:
                await client.send_message(chat_id, f"Error occurred while querying: {e}")
                await asyncio.sleep(10)

    except Exception as e:
        await message.reply(f"Unexpected error: {e}")

    finally:
        stop_scraping = False  # Reset stop flag after scraping ends

app.run()
