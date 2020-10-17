import os
import discord

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

clent = discord.Client()

@client.event
async def on_ready():
    prnt(f'{client.user} has entered the circle jerk!')
  
client.run(TOKEN)
