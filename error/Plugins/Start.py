from .. import bot
from telethon import events
import asyncio
#import openai

#openai.my_api_key = openai_key
@bot.on(events.NewMessage(incoming=True,pattern="/start"))
async def start(event):
  await event.reply("Hello This is coding Bot")
  
  
@bot.on(events.NewMessage(incoming=True,pattern="/get"))
async def start(event):
  a=await event.reply("Hello This is get cammand")
  await asyncio.sleep(3)
  await a.edit("this is an edit messages")
  
  
@bot.on(events.NewMessage(incoming=True,pattern="/eval"))
async def start(event):
  await event.reply("Hello This is eval cammand")