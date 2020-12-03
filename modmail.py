import discord
from discord.ext import commands
import json

def store(file, key=None, read=False, val=None):
	with open(file, 'r') as v:
		x = json.load(v)
	if read is not False:
		if key is None:
			return x
		else:
			return x[key]
	else:
		x[key] = val
		with open(file, 'w') as v:
			json.dump(x, v, indent=4)

client = commands.Bot(command_prefix='>')

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='>modmail'))
	print("\033[92mready\033[0m")

try:
	client.run(store('config.json', 'token', True))
except:
	print("\033[91mrun error\033[0m")
