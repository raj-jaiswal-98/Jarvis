import os
import discord
from dotenv import load_dotenv
from alive import keep_alive
# from discord.ext import commands
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
intents = discord.Intents.default()
intents.members=True
client = discord.Client(intents=intents)
# bot = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    guild = discord.utils.get(client.guilds,name=GUILD)
    print(f'{client.user} has been connected to {guild.name} id:{guild.id}')
    # members = '\n - '.join([member.name for member in guild.members])
    # print(f'Guild Members:\n - {members}')
@client.event
async def on_member_join(member):
  # await client.get_channel().send(f"{member.name} has joined") yh pta nhi kaam krta h ki nhi lal..
  channel = client.get_channel(788505937693900823)
  embed=discord.Embed(title=f"Welcome {member.name}", description=f"Namastey!! {member.guild.name} Ji!!") # F-Strings!
  embed.set_thumbnail(url=member.avatar_url) # Set the embed's thumbnail to the member's avatar image!
  await channel.send(embed=embed)



# bot.run(TOKEN)
client.run(TOKEN)
keep_alive()
