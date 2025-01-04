# Simple Command & Control Server Chat Bot
# This script runs a chat bot for the Terraria game using the `terraria_bot` library.

import sys
try:
   import terraria_bot  # Imports the Terraria bot framework for communication with the game server.
except ModuleNotFoundError:
   # If the module isn't found, prompts the user to run the script from the correct directory.
   print("Please run this file in Terraria-Bot directory, not Terraria-Bot/examples.")
   sys.exit()
import asyncio # For handling asynchronous tasks.
from dictionary import item_id_dictionary  # Dictionary for mapping item names to their corresponding IDs.

# Main async function that initializes and controls the bot.
async def main():
    # Create a bot instance with default settings for the Terraria server.
    bot = terraria_bot.Bot(terraria_server_port=7777, difficult=0)
    await bot.connect()  # Connect to the Terraria server.
    if bot.logged_in:
        print("Logged in successfully!")

    # Main control loop that runs while the bot is active.
    while bot.running:
        if bot.logged_in:
            # If players exist in the game, find and interact with a specific player named "Pongsakorn".
            if bot.entity_manager.players:
                player1 = bot.entity_manager.name_to_player_slot("Pongsakorn")
                print(player1)
                player1 = bot.entity_manager.get_data_from_player_slot(player1[0]) # If players have same name this will get player index 0

                if player1.chat:
                    # Display the chat message from "Pongsakorn" in the console.
                    print("Pongsakorn Chat: " + player1.chat)

                    # Handle chat commands based on the message content.
                    if bot.entity_manager.items:
                        own_item_slot = bot.entity_manager.get_new_slot_of_item()  # Find a new slot for items.

                    if bot.entity_manager.npcs:
                        # Locate NPCs mentioned in the chat message.
                        npc1 = bot.entity_manager.name_to_npc_slot(player1.chat)
                        for slot in npc1:
                            await bot.damageNpc(slot, 32000)  # Inflict high damage to the NPC(s).

                    # Summon an item if the chat message is "Spell".
                    if player1.chat == "Spell":
                        torchs = bot.entity_manager.name_to_item_slot("Torch")
                        print("Trying...")
                        for torch in torchs:
                            torch = bot.entity_manager.get_data_from_item_slot(torch)
                            if torch.stack_amount > 500:  # Check if the player has enough torches.
                                zenith_id = bot.entity_manager.find_id_by_name("Zenith", item_id_dictionary.item_constants)
                                await bot.summonItems(
                                    own_item_slot, torch.pos_x, torch.pos_y, torch.vel_x, torch.vel_y, 1, zenith_id
                                )
                                await bot.sendMsg("Summon Item Success...")

                    # Warp the bot to the player's position if the chat message is "Wrap".
                    elif player1.chat == "Wrap":
                        await bot.warpBotToPosition(player1.pos_x, player1.pos_y, player1.vel_x, player1.vel_y)

                    # Shut down the bot if the chat message is "Gone".
                    elif player1.chat == "Gone":
                        bot.running = False
            else:
                print("No players available.")  # Notify if no players are connected.

            await asyncio.sleep(1)  # Add a delay to reduce server load.

# Run the main async function.
asyncio.run(main())
