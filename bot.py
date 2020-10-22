# Import statements
import os
import discord
import random
from discord.ext.commands import Bot
from discord.ext import commands
from dotenv import load_dotenv

# Load .env file for secret key
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True

description = ''' A discord chat bot written in python by Rizz for the Circle Jerk Server

'''

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

@bot.event
async def on_ready():

	for guild in bot.guilds:
		if guild.name == GUILD:
			break

	print(
		f'{bot.user} is connected to the following guild:\n'
		f'{guild.name}(id: {guild.id})'
		)

	print(f'{bot.user} has entered the circle jerk!')

	members = '\n - '.join([member.name for member in guild.members])
	print(f'Guild Members:\n - {members}')

	# Send a broadcast notifying of bot online status
#	for channel in bot.get_all_channels():
#		if channel.permissions_for(bot):
#			await bot.Messageable(channel, "Yoooooooo, Im back online")


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Wassup {member.name}, ya fuck. Welcome to the Circle Jerk discord server.'
    )

@bot.command(name='hello', category='Useless')
async def hello(ctx):
	await ctx.send('Hello {0.author.mention}'.format(ctx))

@bot.command(name='roll_dice')
async def roll_dice(ctx):
	response = random.randint(1, 6)
	await ctx.send(str(response) + ':scissors:')

@bot.command(name='SPR')
async def scissors_paper_rock(ctx):
	'''Return a random scissors, paper or rock emoji'''
	choices = [':scissors:', ':roll_of_paper:', ':rock:']
	await ctx.send(random.choice(choices))

bot.run(TOKEN)
