import discord
import dbconn
import config
from discord.ext.commands import Bot

bot = Bot(command_prefix='>')
db = dbconn.DataBase()


def get_link(s): #---------------------------------- complete
	links = []

	i = s.find('https://')
	while i != -1 and i<len(s):
		link = 'https://'

		for j in range(i+8,len(s)):
			if s[j]==' ' or s[j]=='\n' or s[j]=='/':
				break
			link += s[j]

		links.append(link)

		i += len(link)
		i = s.find('https://',i)

	return links

def is_admin(member, guild):

	if member.id == guild.owner_id:
		return True

	for role in member.roles:
		if role.name == 'Anti-Spammer-Mod':
			return True
		if role.permissions == discord.Permissions.administrator:
			return True 
		if role.permissions == discord.Permissions.ban_members:
			return True 
		if role.permissions == discord.Permissions.kick_members:
			return True

	return False


@bot.event
async def on_ready():
	print(f'{bot.user} is online')


@bot.event
async def on_message(msz):
	if msz.author.bot:
		return 

	links = get_link(msz.content)

	if links==[] or is_admin(msz.author, msz.guild):
		await bot.process_commands(msz)
		return

	for link in links:
		if db.is_valid(link):
			return
		elif db.is_spam(link):
			await msz.author.add_roles( msz.guild.get_role(config.muted_role_id) )
			await msz.channel.send(f'{msz.author} was muted for spamming')
			return
		else:
			if db.is_unverified(link):
				db.update_warning(msz.author.id)
				await msz.reply(f"You sent an unverified link\n\n<{link}>")
			else:
				db.set_unverified(link, msz.author.id)
				db.update_warning(msz.author.id)

				await msz.guild.get_channel(config.mod_channel).send(f'Here is an unverified link, plz verify it\n<{link}>')
				await msz.reply(f"You sent an unverified link\n\n<{link}>")

	if db.check_warning(msz.author.id)>=5:

		role = msz.guild.get_role(config.muted_role_id)

		await msz.author.add_roles( role )
		await msz.channel.send(f'{msz.author.mention} was muted for spamming')

	await bot.process_commands(msz)


@bot.command()
async def show_valids(ctx):
	info = db.show_valid()
	s = ''
	for x in info:
		s += str(x)[2:-3] + '\n'	

	s = '```\n' + s + '```'

	await ctx.send(s)

@bot.command()
async def show_spams(ctx):
	info = db.show_spam()
	s = ''
	for x in info:
		s += str(x)[2:-3] + '\n'	

	s = '```\n' + s + '```'

	await ctx.send(s)

@bot.command()
async def show_unverifieds(ctx):
	info = db.show_unverified()
	s = ''
	for x in info:
		s += str(x)[2:-3] + '\n'	

	s = '```\n' + s + '```'

	await ctx.send(s)

@bot.command()
async def verify(ctx, link=''):

	if not is_admin(ctx.author , ctx.guild):
		await ctx.send("You are not allowed to verify links");
		return

	q = get_link(link)
	if q==[]: 
		await ctx.send("That wasn't a link")
		return
	link = q[0]

	if db.is_valid(link):
		await ctx.send('Link is already verified')
		return

	if db.is_spam(link):
		await ctx.send('Link is already in spammed list...\nPlease remove it from from spammed list and verify again')
		return

	if db.is_unverified(link):
		ids = db.get_unverified_link_sender(link)
		for id in ids:
			db.del_warning(int(id))

	db.set_valid(link)
	await ctx.send('link verified')


@bot.command()
async def add_spam(ctx, link=''):
	
	if not is_admin(ctx.author , ctx.guild):
		await ctx.send("You are not allowed to verify links");
		return

	q = get_link(link)
	if q==[]: 
		await ctx.send("That wasn't a link")
		return
	link = q[0]

	if db.is_spam(link):
		await ctx.send('Link is already in spam links')
		return

	if db.is_valid(link):
		await ctx.send('Link is already in verified list...\nPlease remove it from from verified list and verify again')
		return

	if db.is_unverified(link):
		ids = db.get_unverified_link_sender(link)
		for id in ids:
			db.del_warning(int(id))	

	db.set_spam(link)
	await ctx.send('link added to spammed list')


@bot.command()
async def pop_verified(ctx, link=''):
	
	if not is_admin(ctx.author , ctx.guild):
		await ctx.send("You are not allowed to remove verify links");
		return

	q = get_link(link)
	if q==[]: 
		await ctx.send("That wasn't a link")
		return
	link = q[0]

	if db.del_valid(link):
		await ctx.send("Removed from verified list")
	else:
		await ctx.send("It's not in the list")


@bot.command()
async def pop_spammed(ctx, link=''):

	if not is_admin(ctx.author , ctx.guild):
		await ctx.send("You are not allowed to remove spammed links");
		return

	q = get_link(link)
	if q==[]: 
		await ctx.send("That wasn't a link")
		return
	link = q[0]

	if db.del_spam(link):
		await ctx.send("Removed from spammed list")
	else:
		await ctx.send("It's not in the list")


@bot.command()
async def warning_status(ctx):

	if not is_admin(ctx.author , ctx.guild):
		return

	info = db.show_member()

	s = '```\n'
	for id, warning in info:
		name = str(await bot.fetch_user(id))
		s += name + '\t' + str(warning) + '\n'

	s += '```'

	await ctx.send(s)

@bot.command()
async def check_warning(ctx, user : discord.Member = None ):
	if not user:
		user = ctx.author

	if not is_admin(ctx.author, ctx.guild):
		user = ctx.author

	w = db.check_warning(user.id)
	await ctx.send(f"{str(user)} has a warning of level {w}")


bot.run(config.token)
