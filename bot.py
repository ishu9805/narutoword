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

app = Client("my_bot", api_id=api_id, api_hash=api_hash, session_string=session_string)


@app.on_message(filters.command("stoped", HANDLER) & filters.user(6257270528))
async def stop_message( client, message):
    global stop_scraping
    stop_scraping = True
    await message.reply("stoping the bot...")

@app.on_message(filters.command("scrap", HANDLER) & filters.user(6257270528))
async def scrap_handler(client, message):
    global stop_scraping
    global processed_results

    try:
        if len(message.command) < 3:
            await message.reply("Usage: .scrap [botusername] [anime_name]")
            return

        bot_username = message.command[1]
        character_name = message.command[2]
        chat_id = message.chat.id

        stop_scraping = False
        query_text = character_name
        await client.send_message(chat_id, f"Querying {query_text}...")
        try:
            results = await client.get_inline_bot_results(bot=bot_username, query=query_text)

            if results.results:
                new_redults_found = False
                for result in results.results:
                    if stop_scraping:
                        await client.send_message(chat_id, "scrapping stoped")
                        return
                    result_id = result.id
                    if result_id in processed_results:
                        continue
                    await client.send_inline_bot_result(chat_id, results.query_id, result_id)
                    processed_results.add(result_id)
                    new_results_found = True
                    await asyncio.sleep(2)  # Delay between sending results

                if new_results_found:
                    await client.send_message(chat_id, f"result")
                else:
                    await client.send_message(chat_id, f"no new result")
            else:
                await client.send_message(chat_id, f"no result")

        except RPCError as e:
                await client.send_message(chat_id, f"Error occurred while querying {query_text}: {e}")
                await asyncio.sleep(10)  # Delay before retrying

    except Exception as e:
        await message.reply(f"Unexpected error: {e}")

app.run()
