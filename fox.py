import discord
import json
from os import system
import asyncio
import datetime
from discord.ext import commands

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

client = commands.Bot(command_prefix='./')
client.remove_command('help')

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='./help | Stable v0.2'))
	print(f"Ready")

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.NotOwner) or isinstance(error, commands.CheckFailure):
		await ctx.send("No Permission!")
	elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
		await ctx.send("Arg error")
	else:
		await ctx.send(f"{error}")

@client.command()
async def help(ctx, comma=None):
	x = store('config.json', 'help', read=True)
	e = discord.Embed(title='Help for NotFox', description="**<>** Fields are optional. **{}** Fields are manditory.", color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
	nu = 0
	for help in x:
		nu += 1
		e.add_field(name=x[str(nu)]["com"], value=x[str(nu)]["desc"], inline=False)
	await ctx.send(embed=e)

@client.command()
@commands.has_permissions(manage_roles=True)
async def purge(ctx, purgeme):
	await ctx.message.delete()
	await ctx.channel.purge(limit=int(purgeme))

@client.command()
@commands.is_owner()
async def check(ctx):
	async for member in ctx.guild.fetch_members(limit=None):
		e = discord.Embed(title=f"Member info for {member}:")
		e.set_thumbnail(url=member.avatar_url)
		e.add_field(name="Join Date:", value=member.joined_at)
		e.add_field(name="Account creation date:", value=member.created_at)
		e.add_field(name="Tag:", value=member.discriminator)
		e.add_field(name="Animated avatar:", value=f"{member.is_avatar_animated()}")
		await ctx.send(embed=e)

@client.command()
@commands.has_permissions(manage_roles=True)
async def purgeuser(ctx, member: discord.Member, amnt):
	await ctx.message.delete()
	def purgec(m):
		return m.author == member
	await ctx.channel.purge(limit=(int(amnt) + 1), check=purgec)

@client.command()
async def clearme(ctx):
	await ctx.message.delete()
	def purgeme(m):
		return m.author == ctx.author
	await ctx.channel.purge(limit=50, check=purgeme)

@client.command()
@commands.has_permissions(manage_roles=True)
async def softban(ctx, member: discord.Member, reason="Softban"):
	def purgec(m):
		return m.author == member
	for channel in ctx.guild.text_channels:
		await channel.purge(limit=None, check=purgec)
	await member.kick(reason=reason)

# @client.command()
# @commands.cooldown(1, 60, commands.BucketType.member)
# async def report(ctx, member: discord.Member, *, reason="Bad Behavior"):
	# channel = client.get_channel(int(store('config.json', 'rch', read=True)))
	# e = discord.Embed(title=f"{ctx.author} reported {member} for ", description=reason, color=discord.Color.red())
	# await channel.send(embed=e)

@client.command()
@commands.is_owner()
async def edit(ctx, mid, new):
	msg = await ctx.channel.fetch_message(int(mid))
	new = discord.Embed(title=new)
	await msg.edit(embed=new)

@client.command()
@commands.is_owner()
async def input(ctx, file, key, val):
	await ctx.message.delete()
	store(file, key, False, val)
	await ctx.send("done")

client.run(store('config.json', 'token', True))
