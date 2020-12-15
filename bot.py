# Import statements
import os
import discord
import random
import time
import requests
import json
import html2text
import string
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

	#await bot.get_channel(GENERAL).send('Im online! Looking good ' + str(random.choice([member.name for member in guild.members][1:]) + '!'))


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Wassup {member.name}, ya fuck. Welcome to the Circle Jerk discord server.'
    )


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
	time.sleep(1)
	await ctx.send("Scissors..")
	time.sleep(1)
	await ctx.send("Paper..")
	time.sleep(1)
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
	time.sleep(60)
	await ctx.send("The correct answer was " + alphabet[answer_list.index(correct_answer)] + '). ' + correct_answer)

bot.run(TOKEN)
