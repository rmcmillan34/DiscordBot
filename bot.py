# Import statements
import os
import discord
import random
import time
import requests
import json
import html2text
import string
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
from dotenv import load_dotenv

# Load .env file for secret key
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GENERAL = int(os.getenv('GENERAL_CHANNEL'))
VERBOSE = os.getenv('DISCORD_VERBOSE')


intents = discord.Intents.default()
intents.members = True

description = ''' A discord chat bot written in python by Rizz for the Circle Jerk Server
README can be found here: https://github.com/rmcmillan34/DiscordBot/blob/main/README.md
'''

bot = commands.Bot(command_prefix='!', description=description, intents=intents)
bot.can_talk = VERBOSE


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

	#await bot.get_channel(GENERAL).send('Im online! Looking good ' + str(random.choice([member.name for member in guild.members][1:]) + '!'))


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Wassup {member.name}, ya fuck. Welcome to the Circle Jerk discord server.'
    )


@bot.event
async def on_message(ctx):
	'''
	What the bot should do on receipt of a message.
	'''
	if ctx == '!verbose':
		verbose(ctx)
	print('message received')
	if bot.can_talk == True:
		print('RESPONDING')


@bot.command(name='hello', category='Useless')
async def hello(ctx):
	'''
	Return a personalised greeting.
	'''
	await ctx.send('Hello {0.author.mention}'.format(ctx))


@bot.command(name='roll_dice')
async def roll_dice(ctx):
	'''
	Return integer between 1 and 6.
	'''
	await ctx.send("Rolling Dice..")
	response = random.randint(1, 6)
	await ctx.send(str(response))


@bot.command(name='SPR')
async def scissors_paper_rock(ctx):
	'''
	Return a random scissors, paper or rock emoji
	'''
	await ctx.send('Alright {0.author.mention}, lets go..'.format(ctx))
	await asyncio.sleep(1)
	await ctx.send("Scissors..")
	await asyncio.sleep(1)
	await ctx.send("Paper..")
	await asyncio.sleep(1)
	await ctx.send("Rock!")
	choices = [':scissors:', ':roll_of_paper:', ':rock:']
	await ctx.send(random.choice(choices))


@bot.command(name='trivia')
async def trivia_question(ctx):
	'''
	Return a random trivia question from https://www.opentdb.com
	'''
	alphabet = string.ascii_lowercase
	# Request new trivia question from opentdb.com and convert response to JSON -- probably should be a try statement
	resp = requests.get('https://opentdb.com/api.php?amount=1').json()

	# Parse the JSON response
	correct_answer = resp['results'][0]['correct_answer']
	answer_list = [x for x in resp['results'][0]['incorrect_answers']]
	answer_list.append(resp['results'][0]['correct_answer'])

	await ctx.send("Okay {0.author.mention}, here's your trivia question: ".format(ctx))
	time.sleep(1)


	if resp['results'][0]['type'] == 'boolean':
		await ctx.send("True/False\n" +  html2text.html2text(resp['results'][0]['question']))
		answer_list = ['True', 'False']
	else:
		await ctx.send("Multiple Choice!\n" + html2text.html2text(resp['results'][0]['question']))
		random.shuffle(answer_list)

	answers = ''
	for i in range(len(answer_list)):
		answers = answers + alphabet[i] + '). ' + answer_list[i] + '\n'

	await ctx.send(answers)
	await asyncio.sleep(10)
	await ctx.send("The correct answer was " + alphabet[answer_list.index(correct_answer)] + '). ' + correct_answer)


@bot.command(name='verbose')
async def verbose(ctx):
	'''
	Toggle if the bot can respond to messages from members on the server
	'''
	await ctx.send(bot.can_talk)
	bot.can_talk = not bot.can_talk
	if bot.can_talk == False:
		await ctx.send('https://tenor.com/view/matrix-mouth-neo-mr-anderson-melted-gif-7848092')
	else:
		await ctx.send('https://tenor.com/view/finally-about-time-damn-gif-15605541')
	await ctx.send(bot.can_talk)


bot.run(TOKEN)
