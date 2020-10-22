# Import statements
import os
import discord
import random
import time
from discord.ext.commands import Bot
from discord.ext import commands
from dotenv import load_dotenv

# Load .env file for secret key
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GENERAL = int(os.getenv('GENERAL_CHANNEL'))

intents = discord.Intents.default()
intents.members = True

description = ''' A discord chat bot written in python by Rizz for the Circle Jerk Server
README can be found here: https://github.com/rmcmillan34/DiscordBot/blob/main/README.md
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


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Wassup {member.name}, ya fuck. Welcome to the Circle Jerk discord server.'
    )


@bot.command(name='hello', category='Useless')
async def hello(ctx):
	'''Return a personalised greeting.'''
	await ctx.send('Hello {0.author.mention}'.format(ctx))


@bot.command(name='roll_dice')
async def roll_dice(ctx):
	'''Return integer between 1 and 6.'''
	await ctx.send("Rolling Dice..")
	response = random.randint(1, 6)
	await ctx.send(str(response))


@bot.command(name='SPR')
async def scissors_paper_rock(ctx):
	'''Return a random scissors, paper or rock emoji'''
	await ctx.send('Alright {0.author.mention}, lets go..'.format(ctx))
	time.sleep(1)
	await ctx.send("Scissors..")
	time.sleep(1)
	await ctx.send("Paper..")
	time.sleep(1)
	await ctx.send("Rock!")
	choices = [':scissors:', ':roll_of_paper:', ':rock:']
	await ctx.send(random.choice(choices))


bot.run(TOKEN)
