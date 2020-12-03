import discord
import datetime
import json
from discord.ext import commands
from asyncio import sleep

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
client.remove_command('help')

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='>modmail'))
	print("\033[92mReady\033[0m")

@client.event
async def on_command_error(ctx, error):
	await ctx.send(f"ERROR: `{error}` Ask Exploded Birdo for help")

@client.command()
async def help(ctx):
	e = discord.Embed(title="Help for Shane ModMail", description="**<>** Fields are optional, **{}** Fields are manditory")
	e.add_field(name=">modmail", value="Open a new modmail ticket")
	await ctx.send(embed=e)

@client.command()
async def modmail(ctx, member: discord.Member=None):
	await ctx.message.delete()
	if member is None: member = ctx.author
	msg = await ctx.send("Creating ModMail Channel..")
	for channel in ctx.guild.text_channels:
		if channel.name == f'modmail-{member.id}':
			await msg.delete()
			await ctx.send(f"ModMail channel already exists! Please contact `Exploded Birdo` for help if you cannot see <#{channel.id}>")
			return
	x = store('tickets.json', None, True)
	if str(member.id) in x:
		await msg.edit(content="Error creating Modmail ticket: Ticket already exists. Please contact `Exploded Birdo` for help.")
		return
	cat = discord.utils.get(ctx.guild.categories, name='modmail')
	chn = await ctx.guild.create_text_channel(f"modmail-{member.id}", category=cat, topic=f"Modmail for user {member}", reason="Modmail created")
	x[str(member.id)] = str(chn.id)
	with open('tickets.json', 'w') as v:
		json.dump(x, v, indent=4)
	await chn.set_permissions(member, read_messages=True, send_messages=True)
	e = discord.Embed(title="ModMail Channel Opened!", color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
	e.set_footer(text="Created")
	e.add_field(name="ModMail opened by:", value=ctx.author)
	if member != ctx.author:
		e.add_field(name="ModMail opened for:", value=member)
	role = discord.utils.get(ctx.guild.roles, name='Pingable Staff')
	msga = await chn.send(f"<@!{ctx.author.id}>")
	await msga.delete()
	await chn.send(f"<@&{role.id}>", embed=e)
	await msg.edit(content=f"Created <#{chn.id}>!")
	await sleep(5)
	await msg.delete()

# add a modmailclose command later (maybe group too idk)
@client.command()
async def close(ctx):
	auth = False
	usar = None
	chan = None
	x = store('tickets.json', None, True)
	for usr, chn in x.items():
		if chn == str(ctx.channel.id):
			if str(ctx.author.id) == usr:
				auth = True
				usar = usr
				chan = chn
				break
			else:
				chan = chn
				try:
					new = ctx.channel.name.replace('modmail-', '')
				except:
					await ctx.send("Erorr!")
					return
				usar = new
				break
				
	role = discord.utils.get(ctx.guild.roles, name='Trainee Mod')
	if role not in ctx.author.roles:
		if str(ctx.author.id) != usar:
			await ctx.send("Cannot execute this command! (Do you have the \"Trainee Mod\" role?)")
			return
	else:
		auth = True
	if auth == False:
		await ctx.send("You are not authorized to close this ticket! (Or the ticket was not found!)")
		return
	# maybe change to embed and add chn.created_at
	e = discord.Embed(title="Delteing Chaannel in 3 seconds!", timestamp=ctx.channel.created_at, color=discord.Color.red())
	e.set_footer(text="ModMail opened")
	await ctx.send(embed=e)
	await sleep(3)
	chn = client.get_channel(int(chan))
	await chn.delete(reason="Modmail ticket closed")
	x.pop(usar)
	with open('tickets.json', 'w') as v:
		json.dump(x, v, indent=4)

# @_kick.error
# async def kick_error(error, ctx):

try:
	client.run(store('config.json', 'token', True))
except:
	print("\033[91mrun error\033[0m")
