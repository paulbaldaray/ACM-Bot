import os, discord, dotenv, asyncio

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CLIENT = discord.Client()

@CLIENT.event
async def on_ready():
	print(f'{CLIENT.user} is connected to the following guild(s):')
	for guild in CLIENT.guilds:
		print(f'{guild.name}(id: {guild.id})')

@CLIENT.event
async def on_voice_state_update(member, before, after):
	join_vc = 'join-to-create-new-vc'

	if before.channel\
			and before.channel.name != join_vc\
			and len(before.channel.members) == 0:
		await before.channel.delete()

	if after.channel and after.channel.name == join_vc:
		new_channel = await after.channel.clone(name='-'*25)
		await member.move_to(new_channel)

CLIENT.run(TOKEN)
