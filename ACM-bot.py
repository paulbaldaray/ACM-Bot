import os, discord, dotenv, asyncio

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

INTENTS=discord.Intents.default()
INTENTS.members = True
CLIENT = discord.Client(intents=INTENTS)

JOIN_VC = 'join-to-create-new-vc'
NEW_VC = '-'*25
assert(JOIN_VC != NEW_VC and NEW_VC != '')

@CLIENT.event
async def on_ready():
	active_channels = []

	print(f'{CLIENT.user} is connected to the following guild(s):')
	for guild in CLIENT.guilds:
		print(f'{guild.name}(id: {guild.id})')
		for vc in list(guild.voice_channels):
			if vc.name == JOIN_VC and len(vc.members) > 0:
				active_channels.append(vc)
			elif vc.name != JOIN_VC and len(vc.members) == 0:
				await vc.delete()

	for vc in active_channels:
		print(f'Creating new channel: {vc.name}')
		new_channel = await vc.clone(name=NEW_VC)
		print(f'Moving users:')
		for member in vc.members:
			print(member.name)
			await member.move_to(new_channel)

@CLIENT.event
async def on_voice_state_update(member, before, after):

	if before.channel\
			and before.channel.name != JOIN_VC\
			and len(before.channel.voice_states) == 0:
		await before.channel.delete()

	if after.channel and after.channel.name == JOIN_VC:
		new_channel = await after.channel.clone(name=NEW_VC)
		await member.move_to(new_channel)

CLIENT.run(TOKEN)
