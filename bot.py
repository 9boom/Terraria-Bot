import terraria_bot
import asyncio

async def main():
    bot = terraria_bot.Bot(terraria_server_port = 7777,difficult=0)
    # เริ่มการเชื่อมต่อ
    await bot.connect()
    # ตรวจสอบสถานะล็อกอิน
    if bot.logged_in:
        print("Logged in successfully!")
    #try:
    while bot.running:
          if bot.logged_in:
                if bot.entity_manager.players:
                   player1 = bot.entity_manager.name_to_player_slot("Pongsakorn")
                   player1 = bot.entity_manager.get_data_from_player_slot(player1)
                   if player1.chat:
                      print(player1.chat)
                      if bot.entity_manager.items:
                         all_item_slots = list(bot.entity_manager.items.keys())
                         #max_slot = max(all_item_slots) if all_item_slots else 0
                         #print(max_slot + 1)
                         #item1=bot.entity_manager.name_to_item_slot["Zenith"]
                         #item1 = bot.entity_manager.items[item1[0]]
                      if bot.entity_manager.npcs:
                         npc1 = bot.entity_manager.name_to_npc_slot(player1.chat)
                         print(npc1)
                         for slot in npc1:
                             print(slot)
                             await bot.damageNpc(slot,32000)
                      if player1.chat == "spell":
                         pass
                         #await bot.updateItems(max_slot+1,item1[0].pos_x,item1[0].pos_y,item1[0].vel_x,item1[0].vel_y,1,4695)
                      elif player1.chat == "wraptoguide":
                         await bot.warpBotToPosition(player1.pos_x,player1.pos_y,player1.vel_x,player1.vel_y)
                      elif player1.chat == "Gone":
                         bot.running = False
                else:
                   print("No players available.")
                   # หยุดเล็กน้อยเพื่อไม่ให้ loop ค้าง
                await asyncio.sleep(1)
    #except Exception as e:
    #    print(f"Error occurred: {e}")

# เรียกใช้งาน
asyncio.run(main())
