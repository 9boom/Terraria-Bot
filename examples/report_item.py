#!/usr/bin/env python3

# Simple Report Items Bot
# This script creates a bot that monitors item data in a Terraria game server and interacts with the game through messages.

import sys
try:
    # Import the Terraria bot framework.
    import terraria_bot
except ModuleNotFoundError:
    # If the module isn't found, prompt the user to run the script from the correct directory.
    print("Please run this file in terraria-bot directory, not terraria-bot/examples.")
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
                await bot.sendMsg("Hello")

            # Continuous processing: Monitor item slots.
            items = bot.entity_manager.return_all_item_slots()  # Retrieve all item slots from the game.

            for item in items:
                # Retrieve detailed data about each item.
                item = bot.entity_manager.get_data_from_item_slot(item)
                # If an item is a "Torch" and the stack amount exceeds 200, send a message.
                if item.name == "Torch" and item.stack_amount > 200:
                    await bot.sendMsg("Do you want to summon torch god event?")

        # Wait before the next iteration to control processing speed.
        await asyncio.sleep(processing_speed_limit)

# Run the main async function.
asyncio.run(main())
