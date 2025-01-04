# Terraria Bot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

Terraria Bot is an advanced automation tool designed to empower your Terraria experience by automating in-game actions and interactions. It offers a flexible and customizable solution for streamlining tasks, enhancing gameplay mechanics, and unlocking creative possibilities.

**Table of Contents**

* [About the Project](#AboutTheProject)
* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Possible Errors and Limitations](#PossibleErrorsAndLimitations)
* [License](#license)
* [Contributing](#contributing)
* [Acknowledgments](#acknowledgments)
* [Support Me](#Donate)

## AboutTheProject

Terraria Bot streamlines various in-game tasks, from dealing damage to NPCs to interacting with players and modifying events with convenient commands. Whether you seek efficiency in resource farming, strategic gameplay enhancement, or simply want to explore more creatively, Terraria Bot is your companion.

**Why Choose Terraria Bot?**

* **Enhanced Gameplay:** Unlock new possibilities and manipulate the game world in innovative ways.
* **Highly Customizable:** Tailor the bot's functionality to your specific preferences and needs.
* **Community-Driven:** Open-source and welcomes contributions for continuous improvement.

## Features

* **NPC Automation:** Deal damage to NPCs for effortless farming or combat scenarios.
* **Coding:** Write your own programs to control your bot to behave as you want.
* **Character Customization:** Assign a unique name to your bot and customize its appearance.
* **Chest & Key Management:** Leverage the bot to unlock various game objects.
* **Chat Interaction:** Listen to in-game chat messages and send your own.
* **Event Reporting:** Receive detailed reports on:
    * NPC Information
    * Player Information
    * Item Information
    * World Information
* **Player Teleportation:** Warp instantly to other players for quicker collaboration and exploration.
* **Item Spawning:** Summon any item into the game world regardless of inventory limitations.
* **Item Ownership Control:** Change the ownership of dropped items.
* **Password Login:** Connect to password-protected servers seamlessly.
* **PvP Mode:** Train your combat skills or engage in friendly duels with the bot.
* **Player Healing:** Restore health for other players within your world or server.
* **Celestial Pillars Control:** Adjust the Strength bar in each Celestial Pillar during events to influence battle dynamics.
* **Error Handling:** The bot automatically stops operations and reports the issue when kicked from the server (Error 2).

## PossibleErrorsAndLimitations
The bot is still somewhat unstable. If anyone submits a help pull request, I would really appreciate it.
1. On certain devices, the game crashes when the bot reaches the stage where it sends packet number 12 (0xC Player Spawn) to the server. I’ve tried to find the cause, but I haven’t been able to and the tools aren’t ready.
2. The NPC_ID in Journey mode is an unknown value. This may be due to the game or my packet decoding system not working properly.
3. The bot cannot communicate with public servers.
4. The bot may will be unstable or stop working when connected to a game server that is not localhost.
5. The x, y coordinates can only be used separately, specific to the type of entity. That means I can’t teleport the bot to the position of an item or to another type of entity.
6. I haven’t tested whether the bot works properly on PC yet (This project made in Phone) If it doesn't work, try using a version similar to or close to 1.4.4.9.6.


## Installation

**Prerequisites**

* Python: Version 3.8 or later

**Dependencies**

Install the required libraries listed in `requirements.txt`.

**Steps**

1. Clone this repository to your local machine.
2. Navigate to the project directory and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Configure the bot by editing the necessary configuration files.

4. Run the bot using:
```bash
python bot.py
```

## Usage

After you have installed That means it's ready to use. Let you write a program to control your bot. or use our example in the project folder and then you can run that python file like this
```bash
python3 yourfilename.py
```

### basic programming
Let's explain the basic programming of bot controls. In the future, we will create a separate website for using the API in detail. If I have been supported and inspired.

In this section, we will help you understand the structure of the program that you will need to write in order to use the basic bot. It is a simple script that can be connected and texted in the game in TerraRia via API. Your program has the following key components:

### Introduction to Basic Programming for Users
1. Module Importing and Setup
```python
import sys
try:
    import terraria_bot
except ModuleNotFoundError:
    print("Please run this file in Terraria-Bot directory")
    sys.exit()
import asyncio  # For handling asynchronous tasks.
from dictionary import npc_id_dictionary
from dictionary import item_id_dictionary
```
**Explanation:**
* **import sys:** Used for system-level operations, such as stopping the program if an error occurs.

* **import terraria_bot:** The main module for working with the Terraria Bot.

* **Using try and except:** Captures errors if the terraria_bot module cannot be imported and displays a user-friendly error message.

* **import asyncio:** Used for handling asynchronous tasks, such as waiting or managing server connections.

* **import npc_id_dictionary:** Used to retrieve NPC names based on their IDs.

* ** import item_id_dictionary:** Used to retrieve item names based on their IDs.


2. Main Function
```python
async def main(onetime=True, processing_speed_limit=1):
    bot = terraria_bot.Bot()
    await bot.connect()  # Connect the bot to the Terraria server.
```
**Explanation:**

* **The `main` function**  
  An asynchronous function designed to initialize and start the bot's operations.

* **Variable `onetime=True`:**  
  Controls one-time execution logic within the bot's functionality.

* **`processing_speed_limit=1`:**  
  Regulates the bot's execution frequency in seconds.

* **`bot = terraria_bot.Bot()`:**  
  Instantiates a bot object using the Terraria bot framework.

* **`await bot.connect()`:**  
  Commands the bot to connect to the Terraria server for further interactions.

Below are the default values for the bot's configuration, which you can customize as needed.
```python
bot = terraria_bot.Bot(terraria_server_ip="127.0.0.1", terraria_server_port=7777,terraria_protocol_version_name="Terraria279",player_slot=0, skin_variant=4, hair=0, name="The_Ironman",mana_level=20,mana_max=20,health_amount=400,health_max=400,hair_dye=0, hide_visible_accessory=0,hide_visible_accessory_v2=0, hide_misc=0, hair_color_R=255, hair_color_G=0, hair_color_B=255,skin_color_R=255, skin_color_G=255,skin_color_B=255, eye_color_R=0, eye_color_G=0, eye_color_B=255,shirt_color_R=255, shirt_color_G=255, shirt_color_B=0, under_shirt_color_R=0, under_shirt_color_G=255,
under_shirt_color_B=255, pants_color_R=0, pants_color_G=255, pants_color_B=0,shoe_color_R=255,shoe_color_G=255, shoe_color_B=255, difficult=0, password="123456")
```
 * If you want to join journey world just set difficult to 14

1. Loop process of Bot
```python
while bot.running:
        if bot.logged_in:
            if onetime:
                onetime = False
                await bot.sendMsg("Hello")  # Sends a message to the server.
        await asyncio.sleep(processing_speed_limit)
```
**Explanation:**

* **`while bot.running:`**  
  Executes the loop as long as the bot is active and running.

* **`if bot.logged_in:`**  
  Checks if the bot has successfully logged into the server.

* **If `onetime` is `True`:**  
  The bot sends the message `"Hello"` to the server. Afterward, the `onetime` variable is set to `False` to prevent repeated messages.

* **`await asyncio.sleep(processing_speed_limit):`**  
  Pauses the loop for the specified duration (`processing_speed_limit`) before starting the next iteration.

4. **Calling the Main Function**
```python
asyncio.run(main())
```
**Explanation:**

* **`asyncio.run(main()):`**  
  Invokes the asynchronous `main()` function to start the program's execution.

### Step-by-Step Guide to Writing a Program

1. **Install and Set Up the Terraria Bot API**  
   Ensure the `terraria_bot` file is in the same directory as your script.

2. **Modify the Loop Functionality**  
   Customize the bot's loop to perform tasks such as detecting players, spawning items, or sending conditional messages.

3. **Adjust Processing Speed**  
   Modify the `processing_speed_limit` variable to control how frequently the bot performs its tasks.

4. **Run the Script**  
   Execute your file with the command:  
   `python3 your_script_name.py`.

### Example: Expanding Your Program  

You can add new functionality to the bot within the loop section:
``` python
if bot.logged_in:
    if onetime:
        onetime = False
        bot.sendMsg("Bot started successfully!")

    # Check the number of players
    players = bot.entity_manager.return_all_player_slots()
    if players:
        for player_slot in players:
            player_data = bot.entity_manager.get_data_from_player_slot(player_slot)
            bot.sendMsg(f"Hello {player_data.name}!")
```
**Explanation:**

* Retrieves data for all players on the server.
* Sends personalized messages when the bot detects a player on the server.

**Summary:**

This program structure serves as the foundation for creating bots in Terraria. You can customize it to suit your needs, such as responding to items, activities, or notifications.

### Using `bot.entity_manager`

`bot.entity_manager` is a key tool for managing entities in the Terraria game, such as Players, NPCs, and Items. It allows you to retrieve data or search for various entities in the game world conveniently.

Before using it, it's essential to understand the difference between a **slot** and an **ID**:

* **Slot:** This is a temporary identifier or "fingerprint" for an entity within the game. It is assigned when the entity is created and serves as the unique reference to identify and access specific data about that entity, such as name, ID, position, etc.
* **ID:** This refers to the permanent identifier for an entity. However, unlike slots, IDs are not used for managing entities directly. Instead, you typically use the slot to fetch the ID, allowing you to learn more about the entity, such as its name.

### Structure of `bot.entity_manager`

1. **Players:**
   - Used to access player data. Once you can access a specific player, you can retrieve the following information:
     - `player_slot`: The unique slot identifier for the player.
     - `chat`: The chat data of the player.
     - `pos_x`: The player's x-coordinate position.
     - `pos_y`: The player's y-coordinate position.
     - `vel_x`: The player's velocity along the x-axis.
     - `vel_y`: The player's velocity along the y-axis.

2. **NPCs:**
   - Used to access NPC (non-player character) data. Once you can access a specific NPC, you can retrieve the following:
     - `npc_slot`: The unique slot identifier for the NPC.
     - `npc_id`: The permanent ID of the NPC.
     - `name`: The NPC's name.
     - `life`: The NPC's health points.
     - `pos_x`: The NPC's x-coordinate position.
     - `pos_y`: The NPC's y-coordinate position.
     - `vel_x`: The NPC's velocity along the x-axis.
     - `vel_y`: The NPC's velocity along the y-axis.

3. **Items:**
   - Used to access item data. Once you can access a specific item, you can retrieve the following:
     - `item_slot`: The unique slot identifier for the item.
     - `item_id`: The permanent ID of the item.
     - `stack_amount`: The number of stacked items.
     - `prefix_id`: The prefix ID for the item.
     - `own_ignore`: Used for the item's ownership status or certain flags.
     - `pos_x`: The item's x-coordinate position.
     - `pos_y`: The item's y-coordinate position.
     - `vel_x`: The item's velocity along the x-axis.
     - `vel_y`: The item's velocity along the y-axis.

### Example Commands and Usage

1. Retrieving all slots for Players, NPCs, and Items:
```python
# Pull all player slots of a players
player_slots = bot.entity_manager.return_all_player_slots()
for player_slot in player_slots:
    print(player_slot)

# Pull all npc slots of a npcs
npc_slots = bot.entity_manager.return_all_npc_slots()
for npc_slot in npc_slots:
    print(npc_slot)

# Pull all item slots of an items
item_slots = bot.entity_manager.return_all_item_slots()
for item_slot in item_slots:
    print(item_slot)
```
### Explanation:

- **`return_all_player_slots`:** Returns all the player slots available in the game world.
- **`return_all_npc_slots`:** Returns all the NPC slots available in the game world.
- **`return_all_item_slots`:** Returns all the item slots available in the game world.
- **`for slot in slots`:** Loops through each slot in the given list of slots, allowing you to process or analyze the entities based on their slot information.

### 2. Retrieving Data from a Specific Slot
You can retrieve data for a specific entity by passing its slot number to the corresponding method. This will fetch the entity details from that slot.
```python
# Retrieve player information from player slot
player_data = bot.entity_manager.get_data_from_player_slot(player_slot)

# Retrieve npc information from npc slot
npc_data = bot.entity_manager.get_data_from_npc_slot(npc_slot)

# Retrieve item information from item slot
item_data = bot.entity_manager.get_data_from_item_slot(item_slot)
```
### Explanation:

- **`get_data_from_player_slot(player_slot):`** Fetches the player's data, such as name, position (`pos_x`, `pos_y`), and velocity (`vel_x`, `vel_y`).
- **`get_data_from_npc_slot(npc_slot):`** Retrieves data about the NPC, such as name, health (`life`), and position (`pos_x`, `pos_y`).
- **`get_data_from_item_slot(item_slot):`** Fetches item data, such as name, quantity (`stack_amount`), and item ID (`item_id`).

### 4. Searching for Slot by Name
If you want to find the slot corresponding to a specific entity by its name, you can use the following methods:
```python
# find player slots with a name of that player
player_slots = bot.entity_manager.name_to_player_slot(player_name)
for player_slot in player_slots:
    print(player_slot)

# find npc slots with a name of that npc
npc_slots = bot.entity_manager.name_to_npc_slot(npc_name)
for npc_slot in npc_slots:
    print(npc_slot)

# find item slots with a name of that item
item_slots = bot.entity_manager.name_to_item_slot(item_name)
for item_slot in item_slots:
    print(item_slots)
```
### Explanation:

You can use these commands to search for slots of Player, NPC, or Item by referencing their names.

### 5. Real-World Usage Example

Let's say you want the bot to find if there is anyone in the game named "Player1" and send a message to them.

Here’s how you can implement this:
```python
player_name = "Player1"
player_slots = bot.entity_manager.name_to_player_slot(player_name)

if player_slots is not None:
    player_slot = player_slots[0]
    player_data = bot.entity_manager.get_data_from_player_slot(player_slot)
    bot.sendMsg(f"Hello, {player_data.name}!")
else:
    bot.sendMsg("Player1 is not found.")
```
### Explanation:
- **Search for the Player slot by name**: This method helps you find a player's slot based on their name.
- **If the player is found**: The bot will send a message to the player.
- **If the player is not found**: It will send a message informing that the player is not found.

### 1. Search for ID from Name

Sometimes, you may want to find a specific ID for an entity (Player, NPC, or Item) from its name. Here’s how you can do it:
```python
item_name = "Torch"
item_id = bot.entity_manager.find_id_by_name(item_name, item_id_dictionary.item_constants)
print(f"The item with name {item_name} is {item_id}.")
```
### Explanation:
- **find_id_by_name(item_name, item_id_dictionary.item_constants)**: This method allows you to search for an item ID using the item name, by referencing the dictionary that maps item names to their IDs.
- **The same can be done for NPCs**: Similarly, you can use the **`npc_id_dictionary`** to search NPC IDs by name.

### Summary
The **`bot.entity_manager`** module is an essential tool for managing players, NPCs, and items in the Terraria game. It provides easy access to various commands within **`entity_manager`**, allowing you to retrieve information as needed. For example, you can check the player's position or the quantity of a specific item in the game world.

### The Features Functions
**You should know:** You should call these functions. within the terms of logged_in

```python
# Teleport the bot to the server at a specified location and velocity.
# pos_x, pos_y, vel_x, and vel_y must be properly set; they can't be random.
# To get the correct values, fetch the position and velocity from a some players in the game, then use them to teleport the bot to at that location.
await bot.warpBotToPosition(pos_x, pos_y, vel_x, vel_y)

# Summons an item to the server at a specified location and velocity.
# pos_x, pos_y, vel_x, and vel_y must be properly set; they can't be random.
# To get the correct values, fetch the position and velocity from an some items in the game, then use them to summon the item at that location.
await bot.summonItems(item_slot, pos_x, pos_y, vel_x, vel_y, stack_amount, item_id)

# Sets the owner of the item to a specified player.
await bot.playerItemOwner(target_item_slot, target_player_slot)

# Sends a chat message to the server.
await bot.sendMsg(text)

# Inflicts damage to all NPCs in the game, excluding players.
await bot.damageNpc(target_npc_slot, damage)

# Toggles PVP mode. Set to 1 to enable, 0 to disable.
await bot.togglePvpMode(self, switch)

# Heals the specified player or the bot itself by a certain amount of health.
await bot.healPlayer(target_player_slot, heal_amount)

# Unlocks chests or doors at the specified tile coordinates.
await bot.unlockChestsOrDoors(tileX, tileY)

# Sets the shield strength of each Celestial Pillar in the event.
await bot.setLifeTower(ShieldStrengthTowerSolar, ShieldStrengthTowerVortex, ShieldStrengthTowerNebula, ShieldStrengthTowerStardust)
```

This is a simple code example. to summon items
```python
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
```


[![Watch Video](https://raw.githubusercontent.com/9boom/Terraria-Bot/main/screenshots/thumbnail.png)](https://raw.githubusercontent.com/9boom/Terraria-Bot/main/screenshots/example_chat_cnc.mp4)


## License

This project is licensed under the **MIT License.** See the LICENSE file for details.

## Contributing

We welcome contributions from the community! To contribute, fork the repository, make your changes, and submit a pull request. Please follow the established coding guidelines.

## Acknowledgments

Thanks to these learning resources that helped me complete this project.
 **Terraria Network Protocol**: [link here](https://seancode.com/terrafirma/net.html)
 **Terraria Game Source Code**: [link here](https://github.com/MikeyIsBaeYT/Terraria-Source-Code)
 **ChatGPT**: [link here](https://chatgpt.com)

## Donate
I developed this project over a poor phone because I don't have a computer. If you find this project useful and want to support development. consider donating Your support helps this project persist and grow. 💖
### Donation Methods:
- **Bye Me A Coffee**: [Support Me](https://buymeacoffee.com/9boom)
### Thank You!
