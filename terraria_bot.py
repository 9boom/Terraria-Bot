#!/usr/bin/env python3

###################################
# Developed By Pongsakorn Sriwichai
# Github:
# Donate:

#Do not edit the value in this file if you don't understand how it works.

import socket #We import this to Receive and send data between servers
import time #We import this to Slows some speed a bit.
import struct #We import this to Decode and create packets between servers.
from colorama import Fore, Style, init #We import this to Make the console text colored
import threading #We import this to Make some processes work in the background.
import asyncio #We import this to Make receiving and sending data works faster.
import item_id_dictionary #We import this to Used to manage identity items in the game
import npc_id_dictionary #We import this to Used to manage the identity of the NPC in the game.

#Always reset the color after running the Colorama command.
init(autoreset=True)

#Used for managing the display on the console.
class Logger:
    def __init__(self):
        self.colors = {
            "info": Fore.GREEN + Style.BRIGHT,
            "warn": Fore.YELLOW + Style.BRIGHT,
            "error": Fore.RED + Style.BRIGHT,
            "default": Fore.BLUE + Style.BRIGHT
        }

    def log(self, message, level="default"):
        print(f"{self.colors[level]}[*] {message}")
        time.sleep(0.1)

#Used for creating and sending packets.
class PacketManager:
    def __init__(self):
        self.packets_queue = asyncio.Queue(maxsize=1000)
    #Add packets to wait for delivery by queue.
    async def add_packet(self, packet):
        await self.packets_queue.put(packet)
    #Pull the packets from the queue to send.
    async def get_packet(self):
        return await self.packets_queue.get()
    #Used to create a payload or packet to send to the server.
    #get_payload(self, for_connect_packet=False, msg_type=None, data=None, use_length_string=False,
    #                have_raw_packet_to_send=False, raw_packet_to_send=0, use_new_structured_data=False,
    #                structure_type=None, structure_data=None):
    # for_connect_packet : Activate if the payload you create is partially and want to connect to other payloads.
    # msg_type : If for_connect_packet is true, just enter number 0, but if not, you need to specify this (msgType is used to define the type or function of the packet you created, such as killing a player, summon an item. You can learn more in the readme.md file).
    # data : Payload data to create (return as byte)
    # use_length_string : Activate if the payload is used to create a String.
    # have_raw_packet_to_send : Activate if all payload parts are successfully created. and ready for attaching MsgType
    # raw_packet_to_send : If have_raw_packet_to_send is true, you need to specify that payload variable.
    # use_new_structured_data : Activated If you want to create a custom payload part
    # structure_type : If use_new_structured_data is true, you must specify the type of packet you will create. The identification will be the same as the struct module in Python.
    # steucture_data : Payload data to create (return as your structure_type)
    def get_payload(self, for_connect_packet=False, msg_type=None, data=None, use_length_string=False,
                    have_raw_packet_to_send=False, raw_packet_to_send=0, use_new_structured_data=False,
                    structure_type=None, structure_data=None):
        data_bytes = bytearray()
        if use_new_structured_data:
            temp = struct.pack(structure_type, structure_data)
            data_bytes.extend(temp)
            return data_bytes
        else:
            if use_length_string:
                if not have_raw_packet_to_send:
                    length = len(data)
                    data = bytes(data, 'utf-8')
                    data_bytes = struct.pack('<b', length)
                    data_bytes += data
            else:
                if not have_raw_packet_to_send:
                    data_bytes += bytes([data])
            if not for_connect_packet:
                if not raw_packet_to_send == 0:
                    packet = struct.pack("<h", len(raw_packet_to_send) + 3)
                    packet += struct.pack('b', msg_type)
                    packet += raw_packet_to_send
                    return packet
                else:
                    packet = struct.pack("<h", len(data_bytes) + 3)
                    packet += struct.pack('b', msg_type)
                    packet += data_bytes
                    return packet
            else:
                if not have_raw_packet_to_send:
                    return data_bytes
# used to collect world data
class World:
    def __init__(self):
        self.time = 0
        self.daynight = 0
        self.moonphase = 0
        self.maxX = 0
        self.maxY = 0
        self.spawnX = 0
        self.spawnY = 0

# Used to read packets sent from the server. (little endian)
class Streamer(object):
    def __init__(self, data):
        self.data = data
        self.index = 0

    def next_short(self):
        result = struct.unpack("<h", self.data[self.index: self.index + 2])[0]
        self.index += 2
        return result

    def next_u_short(self):
        result = struct.unpack("<H", self.data[self.index: self.index + 2])[0]
        self.index += 2
        return result

    def next_int32(self):
        result = struct.unpack("<i", self.data[self.index: self.index + 4])[0]
        self.index += 4
        return result

    def next_byte(self):
        result = self.data[self.index]
        self.index += 1
        return result

    def next_float(self):
        result = struct.unpack("<f", self.data[self.index: self.index + 4])[0]
        self.index += 4
        return result

    def back_int16(self):
        last_two_bytes = self.data[-2:]
        result = struct.unpack('<h', bytes(last_two_bytes))[0]
        return result

    def next_string(self,length):
        result = self.data[self.index: self.index + length]
        self.index += length
        return result

    def return_all_from_back_index(self):
        result = self.data[self.index:]
        return result

    def remainder(self):
        return self.data[self.index:]

# Used to collect Entity data
class PlayerEntity:
    def __init__(self, player_slot=0,name="Unknown Entity",chat=None,pos_x=0,pos_y=0,vel_x=0,vel_y=0):
        self.player_slot = player_slot
        self.name = name
        self.chat = chat
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y

class NpcEntity:
    def __init__(self, npc_slot=0,name="Unknown Entity", npc_id=0, life=0, pos_x=0, pos_y=0, vel_x=0, vel_y=0):
        self.npc_slot = npc_slot
        self.name = name
        self.npc_id = npc_id
        self.life = life
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y

class ItemEntity:
    def __init__(self, item_slot=0,name="Unknown Entitt",item_id=0,stack_amount=0,prefix_id=0,own_ignore=0, pos_x=0, pos_y=0, vel_x=0, vel_y=0):
        self.item_slot = item_slot
        self.name = name
        self.item_id = item_id
        self.stack_amount = stack_amount
        self.prefix_id = prefix_id
        self.own_ignore = own_ignore
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y

class EntityManager:
    def __init__(self):
        self.players = {}
        self.npcs = {}
        self.items = {}
        self.players_name = {}
        self.logger = Logger()


    def update_player(self, player):
        self.players[player.player_slot] = player
        self.players_name[player.name] = player.player_slot

    def update_npc(self, npc):
        self.npcs[npc.npc_slot] = npc

    def update_item(self, item):
        self.items[item.item_slot] = item

    def get_new_slot_of_item(self):
        all_item_slots = list(self.items.keys())
        max_slot = max(all_item_slots) if all_item_slots else 0
        return (max_slot + 1)

    def get_data_from_player_slot(self,player_slot):
        try:
            data = self.players[player_slot]
            return data
        except:
            self.logger.log(f"[!] Failed to get player data from {player_slot}",level="warn")

    def get_data_from_npc_slot(self,npc_slot):
        try:
            data = self.npcs[npc_slot]
            return data
        except:
            self.logger.log(f"[!] Failed to get npc data from {npc_slot}",level="warn")

    def get_data_from_item_slot(self,item_slot):
        try:
            data = self.items[item_slot]
            return data
        except:
            self.logger.log(f"[!] Failed to get item data from {item_slot}",level="warn")

    def name_to_player_slot(self, _name):
        try:
            slot = self.players_name[_name]
            return slot
        except:
            self.logger.log(f"[!] Failed to get player slot from name {_name}",level="warn")

    def name_to_npc_slot(self, _name):
        try:
            slots = [slot for slot, npc in self.npcs.items() if npc.name == _name]
            return slots
        except:
            self.logger.log(f"[!] Failed to get npc slot from name {_name}",level="warn")

    def name_to_item_slot(self, _name):
        try:
            slots = [slot for slot, item in self.items.items() if item.name == _name]
            return slots
        except:
            self.logger.log(f"[!] Failed to get item slot from name {_name}",level="warn")

    def return_all_players(self):
       try:
           slots = [slot for slot, item in self.players.items()]
           return slots
       except:
           self.logger.log(f"[!] Failed to get all player slots",level="warn")

    def return_all_npcs(self):
       try:
           slots = [slot for slot, npc in self.npcs.items()]
           return slots
       except:
           self.logger.log(f"[!] Failed to get all npc slots",level="warn")

    def return_all_items(self):
       try:
           slots = [slot for slot, item in self.items.items()]
           return slots
       except:
           self.logger.log(f"[!] Failed to get all item slots",level="warn")

    def find_name_by_id(self,item_id, constants_dict):
        id_to_name = {v: k for k, v in constants_dict.items()}

        name = id_to_name.get(item_id, None)

        if name:
               return name
        else:
               return "Unknown Entity"

class Bot:
    def __init__(self, terraria_server_ip="127.0.0.1", terraria_server_port=7777, terraria_protocol_version_name="Terraria279",
                 player_slot=0, skin_variant=4, hair=0, name="The_Ironman",mana_level=20,mana_max=20,health_amount=400,health_max=400, hair_dye=0, hide_visible_accessory=0,
                 hide_visible_accessory_v2=0, hide_misc=0, hair_color_R=255, hair_color_G=0, hair_color_B=255,
                 skin_color_R=255, skin_color_G=255, skin_color_B=255, eye_color_R=0, eye_color_G=0, eye_color_B=255,
                 shirt_color_R=255, shirt_color_G=255, shirt_color_B=0, under_shirt_color_R=0, under_shirt_color_G=255,
                 under_shirt_color_B=255, pants_color_R=0, pants_color_G=255, pants_color_B=0, shoe_color_R=255,
                 shoe_color_G=255, shoe_color_B=255, difficult=0, password="123456"):
        self.terraria_server_ip = terraria_server_ip
        self.terraria_server_port = terraria_server_port
        self.terraria_protocol_version_name = terraria_protocol_version_name
        self.player_slot = player_slot
        self.skin_variant = skin_variant
        self.hair = hair
        self.name = name
        self.hair_dye = hair_dye
        self.hide_visible_accessory = hide_visible_accessory
        self.hide_visible_accessory_v2 = hide_visible_accessory_v2
        self.hide_misc = hide_misc
        self.hair_color_R = hair_color_R
        self.hair_color_G = hair_color_G
        self.hair_color_B = hair_color_B
        self.skin_color_R = skin_color_R
        self.skin_color_G = skin_color_G
        self.skin_color_B = skin_color_B
        self.eye_color_R = eye_color_R
        self.eye_color_G = eye_color_G
        self.eye_color_B = eye_color_B
        self.shirt_color_R = shirt_color_R
        self.shirt_color_G = shirt_color_G
        self.shirt_color_B = shirt_color_B
        self.under_shirt_color_R = under_shirt_color_R
        self.under_shirt_color_G = under_shirt_color_G
        self.under_shirt_color_B = under_shirt_color_B
        self.pants_color_R = pants_color_R
        self.pants_color_G = pants_color_G
        self.pants_color_B = pants_color_B
        self.shoe_color_R = shoe_color_R
        self.shoe_color_G = shoe_color_G
        self.shoe_color_B = shoe_color_B
        self.difficult = difficult
        self.running = False
        self.world = World()
        self.logger = Logger()
        self.packet_manager = PacketManager()
        self.initialized = False
        self.logged_in = False
        self.npc_data = {}
        self.pre_player_vel_x = 0
        self.pre_player_vel_y = 0
        self.queue = asyncio.Queue(maxsize=1000)
        self.player_slot = 0
        self.entity_manager = EntityManager()
        self.mana_level = mana_level
        self.mana_max = mana_max
        self.health_amount = health_amount
        self.health_max = health_max
        self.password = password
    def start_background_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(asyncio.gather(
            self.send_from_queue(),
            self.producer(),
            self.consumer(),
        ))

    def start(self):
        t = threading.Thread(target=self.start_background_loop)
        t.start()
    async def connect(self):
              try:
                     self.running = True
                     self.logger.log(f"[*] The process of sending bots is starting...")
                     self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                     self.client.setblocking(False)  # Non-blocking
                     await asyncio.get_event_loop().sock_connect(self.client, (self.terraria_server_ip, self.terraria_server_port))
                     self.logger.log(f"[*] Packet 1 Sending. Connection Request... (Using Protocol Version : {self.terraria_protocol_version_name})")
                     # Add initial packet to queue
                     await self.packet_manager.add_packet(
                     self.packet_manager.get_payload(False, 1, self.terraria_protocol_version_name, True)
                     )
                     # Start asynchronous tasks
                     self.start()
              except socket.error as e:
                     self.logger.log(f"[!] Connection Error: {e}", level="warn")

    async def send_from_queue(self):
        while self.running:
            try:
                packet = await self.packet_manager.get_packet()
                try:
                    await self.packet_manager.packets_queue.task_done()
                except:
                    pass
                await asyncio.get_event_loop().sock_sendall(self.client, packet)
            except Exception as e:
                self.logger.log(f"[!] Error sending packet: {e}", level="error")

    async def producer(self):
        while self.running:
            try:
                header = await asyncio.get_event_loop().sock_recv(self.client, 2)
                if len(header) < 2:
                    self.running = False
                    continue
                packet_length = struct.unpack("<h", header)[0] - 2
                data = await asyncio.get_event_loop().sock_recv(self.client, packet_length)
                await self.queue.put(data)
            except Exception as e:
                self.logger.log(f"[!] Error receiving packet: {e}", level="error")

    async def consumer(self):
        while self.running:
            try:
                data = await self.queue.get()
                await self.process_packet(data)
                self.queue.task_done()
            except Exception as e:
                self.logger.log(f"[!] Error processing packet: {e}", level="error")
    async def process_packet(self, data):
        # Store the packetType sent from the server.
        packetType = data[0]
        # Process packets based on packetType
        # PacketType is the key to identifying the functions of the packet or payload.
        if packetType == 37:
            await self.sendPacket26()
        if packetType == 2:
            streamer = Streamer(data)
            streamer.next_byte()
            kick = streamer.return_all_from_back_index()
            kick = kick.decode()
            self.logger.log("[!] Kicked from server", level="error")
            self.logger.log(kick, level="error")
            self.running = False
        if packetType == 3:
             streamer = Streamer(data)
             streamer.next_byte()
             player_slot = streamer.next_byte()
             if player_slot > 8:
                self.logger.log("[!] Can't join the server because there are too many players.", level="error")
                self.running = False
             self.logger.log(f"[+] The connection request is approved.",level="info")
             self.player_slot = player_slot
             self.logger.log(f"[*] Packet 4 Sending. Player Appearance...")
             await self.sendPacket4()
             self.logger.log(f"[*] Packet 10 Sending. Set Player Life...")
             await self.sendPacket10()
             self.logger.log(f"[*] Packet 2A Sending. Set Player Mana...")
             await self.sendPacket2A()
             self.logger.log(f"[*] Packet 32 Sending. Set Player Buffs...")
             await self.sendPacket32()
             self.logger.log(f"[*] Packet 5 Sending. Set Inventory...")
             for i in range(0,58):
                     await self.sendPacket5(i)
             self.logger.log(f"[*] Packet 6 Sending. Request World Infomation...")
             await self.sendPacket6()
        if packetType == 82:
             streamer = Streamer(data)
             streamer.next_byte()
             net_module_type = streamer.next_byte()
             if net_module_type == 1:
                streamer.next_byte()
                player_slot = streamer.next_byte()
                streamer.next_byte()
                length = streamer.next_byte()
                chat = streamer.next_string(length)
                chat = chat.decode()
                try:
                    self.entity_manager.players[player_slot].chat = chat
                except Exception as e:
                    self.logger.log(f"[!] Player slot : {player_slot} not found, Can't process this player slot chat", level="warn")
        if packetType == 4:
             streamer = Streamer(data)
             streamer.next_byte()
             player_slot = streamer.next_byte()
             skin_variant = streamer.next_byte()
             hair = streamer.next_byte()
             string_length = streamer.next_byte()
             name = streamer.next_string(string_length)
             name = name.decode()
             hair_dye = streamer.next_byte()
             hide_visible_accessory = streamer.next_byte()
             hide_visible_accessory_v2 = streamer.next_byte()
             hide_misc = streamer.next_byte()
             hair_color_R = streamer.next_byte()
             hair_color_G = streamer.next_byte()
             hair_color_B = streamer.next_byte()
             skin_color_R = streamer.next_byte()
             skin_color_G = streamer.next_byte()
             skin_color_B = streamer.next_byte()
             eye_color_R = streamer.next_byte()
             eye_color_G = streamer.next_byte()
             eye_color_B = streamer.next_byte()
             shirt_color_R = streamer.next_byte()
             shirt_color_G = streamer.next_byte()
             shirt_color_B = streamer.next_byte()
             under_shirt_color_R = streamer.next_byte()
             under_shirt_color_G = streamer.next_byte()
             under_shirt_color_B = streamer.next_byte()
             pants_color_R = streamer.next_byte()
             pants_color_G = streamer.next_byte()
             pants_color_B = streamer.next_byte()
             shoe_color_R = streamer.next_byte()
             shoe_color_G = streamer.next_byte()
             shoe_color_B = streamer.next_byte()
             difficult = streamer.next_byte()
             self.entity_manager.update_player(PlayerEntity(player_slot=player_slot,name=name))
        if packetType == 13:
             streamer = Streamer(data)
             streamer.next_byte()
             player_slot = streamer.next_byte()
             flags = streamer.next_byte()
             selected_item_slot = streamer.next_byte()
             pos_x = streamer.next_float()
             pos_y = streamer.next_float()
             try:
                   self.pre_player_vel_x = streamer.next_float()
                   self.pre_player_vel_y = streamer.next_float()
                   vel_x = self.pre_player_vel_x
                   vel_y = self.pre_player_vel_y
             except:
                   vel_x = self.pre_player_vel_x
                   vel_y = self.pre_player_vel_y
             self.entity_manager.players[player_slot].pos_x = pos_x
             self.entity_manager.players[player_slot].pos_y = pos_y
             self.entity_manager.players[player_slot].vel_x = vel_x
             self.entity_manager.players[player_slot].vel_y = vel_y
        if packetType == 7:
                  self.logger.log(f"[+] Getting World Information",level="info")
                  streamer = Streamer(data)
                  streamer.next_byte()  # Ignore packet ID byte
                  self.world.time = streamer.next_int32()
                  self.world.daynight = streamer.next_byte()
                  self.world.moonphase = streamer.next_byte()
                  self.world.maxX = streamer.next_short()
                  self.world.maxY = streamer.next_short()
                  self.world.spawnX = streamer.next_short()
                  self.world.spawnY = streamer.next_short()
                  if not self.initialized:
                         self.initialized = True
                         self.logger.log(f"[*] Packet 8 Sending. Request initial tile data...")
                         await self.sendPacket8()
        if packetType == 49:
                  self.logger.log(f"[+] Request to Spawn",level="info")
                  self.logger.log(f"[+] Packet C Sending. Spawning....",level="info")
                  await self.sendPacketC()
        if packetType == 129:
                  self.logger.log(f"[*] Logged in")
                  self.logged_in = True
        if packetType == 21:
                  streamer = Streamer(data)
                  streamer.next_byte()
                  item_slot = streamer.next_short()
                  pos_x = streamer.next_float()
                  pos_y = streamer.next_float()
                  vel_x = streamer.next_float()
                  vel_y = streamer.next_float()
                  stack_amount = streamer.next_short()
                  prefix_id = streamer.next_byte()
                  own_ignore = streamer.next_byte()
                  item_id = streamer.next_short()
                  name = self.entity_manager.find_name_by_id(item_id,item_id_dictionary.item_constants)
                  self.entity_manager.update_item(ItemEntity(item_slot,name,item_id,stack_amount,prefix_id,own_ignore,pos_x,pos_y,vel_x,vel_y))
        if packetType == 23:
                  streamer = Streamer(data)
                  streamer.next_byte()
                  npc_slot = streamer.next_short()
                  pos_x = streamer.next_float()
                  pos_y = streamer.next_float()
                  vel_x = streamer.next_float()
                  vel_y = streamer.next_float()
                  target = streamer.next_byte()
                  flags = streamer.next_byte()
                  life = streamer.next_int32()
                  npc_id = streamer.back_int16()
                  name = self.entity_manager.find_name_by_id(npc_id,npc_id_dictionary.npc_constants)
                  self.entity_manager.update_npc(NpcEntity(npc_slot,name,npc_id,life,pos_x,pos_y,vel_x,vel_y))
    # The functions below is the ability of bots when calling any function It will create a payload or packet and specify MsgType what it will do and send it to the game server.
    async def setLifeTower(self,ShieldStrengthTowerSolar,ShieldStrengthTowerVortex,ShieldStrengthTowerNebula,ShieldStrengthTowerStardust):
        packet = self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",ShieldStrengthTowerSolar)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",ShieldStrengthTowerVortex)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",ShieldStrengthTowerNebula)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",ShieldStrengthTowerStardust)
        packet = self.packet_manager.get_payload(False,101,packet,False,True,packet,False,None,None)
        await self.packet_manager.add_packet(packet)
    async def unlockChestsOrDoors(self,tileX,tileY):
        packet = self.packet_manager.get_payload(True,0,1,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",tileX)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",tileY)
        packet = self.packet_manager.get_payload(False,52,packet,False,True,packet,False,None,None)
        await self.packet_manager.add_packet(packet)
    async def healPlayer(self,target_player_slot,heal_amount):
        packet = self.packet_manager.get_payload(True,0,target_player_slot,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",heal_amount)
        packet = self.packet_manager.get_payload(False,66,packet,False,True,packet,False,None,None)
        await self.packet_manager.add_packet(packet)
    async def damageNpc(self,target_npc_slot,damage):
        packet = self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",target_npc_slot)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",damage)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<f",4.657323415813153e-10)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,False,None,None)
        packet = self.packet_manager.get_payload(False,28,packet,False,True,packet,False,None,None)
        await self.packet_manager.add_packet(packet)
    async def sendMsg(self,text):
        packet = self.packet_manager.get_payload(True,0,1,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,self.player_slot,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,text,True,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,255,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,255,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,255,False,False,0,False,None,None)
        packet = self.packet_manager.get_payload(False,82,packet,False,True,packet,False,None,None)
        await self.packet_manager.add_packet(packet)
    async def updateItems(self,item_slot,pos_x,pos_y,vel_x,vel_y,stack_amount,item_id):
        packet = self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",item_slot)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<f",pos_x)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<f",pos_y)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<f",vel_x)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<f",vel_y)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",stack_amount)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",item_id)
        packet = self.packet_manager.get_payload(False,21,packet,False,True,packet,False,None,None)
        await self.packet_manager.add_packet(packet)
    async def playerItemOwner(self,target_item_slot,target_player_slot):
        packet = self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",target_item_slot)
        packet += self.packet_manager.get_payload(True,0,target_player_slot,False,False,0,False,None,None)
        packet = self.packet_manager.get_payload(False,22,packet,False,True,packet,False,None,None)
        await self.packet_manager.add_packet(packet)
    async def warpBotToPosition(self,pos_x,pos_y,vel_x,vel_y):
        packet = self.packet_manager.get_payload(True,0,self.player_slot,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,0b00000000,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,1,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<f",pos_x)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<f",pos_y)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<f",vel_x)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<f",vel_y)
        packet += self.packet_manager.get_payload(True,0,255,False,False,0,False,None,None)
        packet = self.packet_manager.get_payload(False,13,packet,False,True,packet,False,None,None)
        await self.packet_manager.add_packet(packet)
    async def togglePvpMode(self,switch):
        packet = self.packet_manager.get_payload(True,0,self.player_slot,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,switch,False,False,0,False,None,None)
        packet = self.packet_manager.get_payload(False,30,packet,False,True,packet,False,None,None)
        await self.packet_manager.add_packet(packet)
    async def sendPacket26(self):
        packet = self.packet_manager.get_payload(True, 0, self.password, True, False, 0, False, None, None)
        packet = self.packet_manager.get_payload(False,0x26,packet,False,True,packet,False,None,None)
        await self.packet_manager.add_packet(packet)
    async def sendPacketC(self): #Spawn Player
        #The client sends this at the end of the login process to spawn the player. The server enforces the player slot so attempts to spawn another player will instead respawn the client's player.
        packet = self.packet_manager.get_payload(True,0,self.player_slot,False,False,0,False,None,None)
        packet = self.packet_manager.get_payload(False,0xC,bytes.fromhex(str(0)+str(self.player_slot)+"ffffffff000000000500000001"),False,True,bytes.fromhex(str(0)+str(self.player_slot)+"ffffffff000000000500000001"),False,None,None)
        await self.packet_manager.add_packet(packet)
    async def sendPacket8(self): #Request Initial Tile Data #<i
        #The client sends this message to the server to request initial tile data. The client specifies the player's spawn X,Y. This may or may not be the same as the server spawn. The server sends a lot of messages in response to this. See the Login process below for more detail.
        packet = self.packet_manager.get_payload(False,0x8,bytes.fromhex("ffffffffffffffff"),False,True,bytes.fromhex("ffffffffffffffff"),False,None,None)
        await self.packet_manager.add_packet(packet)
    async def sendPacket6(self): #Request World Information
        #Asks the server for world info. This is done as part of the login process.
        await self.packet_manager.add_packet(self.packet_manager.get_payload(False,0x6,"",True,False,0))
    async def sendPacket5(self,slot): #Set Inventory
        #This specifies what item is in a specific inventory slot. Slots 0 to 58 are inventory slots, Slots 59 to 69 are armor/accessory slots. Slots 70 to 72 are dye slots. A stack of 0 means the slot is empty.
        packet = self.packet_manager.get_payload(True,0,self.player_slot,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,slot,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",1)
        packet += self.packet_manager.get_payload(True,0,1,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",1)
        packet = self.packet_manager.get_payload(False,0x5,packet,False,True,packet,False,None,None)
        await self.packet_manager.add_packet(packet)
    async def sendPacket32(self): #Set Player Buffs
        #Client sends this during initialization, or when the player activates multiple buffs. The server enforces the player slot, so you cannot change the buffs of another player.
        packet = self.packet_manager.get_payload(True,0,self.player_slot,False,False,0,False,None,None)
        for i in range(0,22):
                packet += self.packet_manager.get_payload(True,0,0,False,False,0,False,None,None)
        packet = self.packet_manager.get_payload(False,0x32,packet,False,True,packet,False,None,None)
        await self.packet_manager.add_packet(packet)
    async def sendPacket2A(self): #Set Player Mana
        #Client sends this as part of the login to specify the mana levels. The server enforces the player slot, so you may not set mana for another player.
        packet = self.packet_manager.get_payload(True,0,self.player_slot,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",self.mana_level)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",self.mana_max)
        packet = self.packet_manager.get_payload(False,0x2a,packet,False,True,packet,False,None,None)
        await self.packet_manager.add_packet(packet)
    async def sendPacket10(self): #Set Player Life
        #The client sends this as part of the login process. The server enforces the player slot, so attempts to modify another person's health will only modify your own.
        packet = self.packet_manager.get_payload(True,0,self.player_slot,False,False,0,False,None,None)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",self.health_amount)
        packet += self.packet_manager.get_payload(True,0,0,False,False,0,True,"<h",self.health_max)
        packet = self.packet_manager.get_payload(False,0x10,packet,False,True,packet,False,None,None)
        await self.packet_manager.add_packet(packet)
    async def sendPacket4(self): #Player Appearance
        #The client sends this as part of the login process to notify the server of the player's appearance. There is nothing preventing the client from sending this after the login process, however. The server will enforce the player slot, so any attempts to change the appearance of other players will just change your own.
        packet = self.packet_manager.get_payload(True, 0, self.player_slot, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.skin_variant, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.hair, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.name, True, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.hair_dye, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.hide_visible_accessory, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.hide_visible_accessory_v2, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.hide_misc, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.hair_color_R, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.hair_color_G, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.hair_color_B, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.skin_color_R, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.skin_color_G, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.skin_color_B, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.eye_color_R, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.eye_color_G, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.eye_color_B, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.shirt_color_R, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.shirt_color_G, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.shirt_color_B, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.under_shirt_color_R, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.under_shirt_color_G, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.under_shirt_color_B, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.pants_color_R, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.pants_color_G, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.pants_color_B, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.shoe_color_R, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.shoe_color_G, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.shoe_color_B, False, False, 0, False, None, None)
        packet += self.packet_manager.get_payload(True, 0, self.difficult, False, False, 0, False, None, None)  # changed to 14 for journey mode
        packet = self.packet_manager.get_payload(False, 0x4, packet, False, True, packet, False, None, None)
        await self.packet_manager.add_packet(packet)
