#!/usr/bin/env python3

# Simple Bot
# This script initializes a basic bot for Terraria that can send messages and perform looping tasks.

import sys
try:
    # Import the Terraria bot framework.
    import terraria_bot
except ModuleNotFoundError:
    # If the module isn't found, prompt the user to run the script from the correct directory.
    print("Please run this file in Terraria-Bot directory, not Terraria-Bot/examples.")
    sys.exit()

import asyncio  # For handling asynchronous tasks.

# Main asynchronous function for the bot.
async def main(onetime=True, processing_speed_limit=1):
    # Initialize the bot with default settings.
    bot = terraria_bot.Bot()
    await bot.connect()  # Connect the bot to the Terraria server.

    # Main control loop that runs while the bot is active.
    while bot.running:
        if bot.logged_in:
            if onetime:
                # One-time initialization task: Send a "Hello" message.
                onetime = False
                await bot.sendMsg("Hello")  # Sends a message to the server.

            # Looping logic (empty in this example, can be customized for additional features).

        # Wait before the next iteration to control processing speed.
        await asyncio.sleep(processing_speed_limit)

# Run the main async function.
asyncio.run(main())
