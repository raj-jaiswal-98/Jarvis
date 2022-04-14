import os
# import random
from bs4 import BeautifulSoup
import discord
import requests
from dotenv import load_dotenv
from alive import keep_alive
from discord.ext import commands
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
api_dev_key=os.getenv('api_dev_key')
api_user_key=os.getenv('api_user_key')
intents = discord.Intents.default()
api_paste_key = os.getenv('API_PASTE_KEY')
intents.members=True
# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)



def pull_paste_backfunc():
  url="https://pastebin.com/api/api_raw.php"
  api_option='show_paste'
  data={
    'api_dev_key':api_dev_key,
    'api_user_key':api_user_key,
    'api_paste_key':api_paste_key,
    'api_option':api_option
  }
  r=requests.post(url,data=data)
  return r.text
  
def list_pastes_backend():
  url="https://pastebin.com/api/api_post.php"
  api_option='list'
  data={
    'api_dev_key':api_dev_key,
    'api_user_key':api_user_key,
    'api_option':api_option
  }
  r=requests.post(url,data=data)
  # res=r.text
  return r.text


#--------------------------------------------------
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(bot.guilds)
    print('------')
    await bot.change_presence(status=discord.Status.idle,activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))
    # chal=discord.utils.get(server.channels,name='general')
    # chal=bot.get_channel(788505937693900823)
    # await chal.send("Hello!!")
    
    # await chal.send("Hydra chutiyo ki nhi sunta!! Ashvin")
    # await bot.change_presence(status=discord.Status.idle, activity=activity)

#--------------------------------------------------
@bot.command()
async def repeat(ctx, times: int, content,category='General'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)
@bot.command(name='hello',help="Just informal Hello!!")
async def hello_func(ctx):
  await ctx.send("Ram Ram vhiya!!")

# @bot.command(name='stp',help='Stone Paper Scissor classic game.')
# async def stone_paper(ctx):
#   options_stone_paper=["stone","paper","scissor"]
#   await ctx.send("Let's Start the Game!! Enter your move.")
#   arg = await bot.wait_for('message')

#   bot_chance=random.choice(options_stone_paper)
#   if arg==bot_chance:
#     await ctx.send("I also said "+bot_chance+"!!")
#   else:
#     if arg==options_stone_paper[0] and bot_chance==options_stone_paper[1]:
#       await ctx.send("Bot Wins")
#     elif arg==options_stone_paper[0] and bot_chance==options_stone_paper[2]:
#       await ctx.send("User Wins!!")
#     elif arg==options_stone_paper[1] and bot_chance==options_stone_paper[0]:
#       await ctx.send("User Wins!!")
#     elif arg==options_stone_paper[1] and bot_chance==options_stone_paper[2]:
#       await ctx.send("Bot Wins!!")
#     elif arg==options_stone_paper[2] and bot_chance==options_stone_paper[0]:
#       await ctx.send("Bot Wins!!")
#     elif arg==options_stone_paper[2] and bot_chance==options_stone_paper[1]:
#       await ctx.send("User Wins!!")
#     else:
#       await ctx.send(arg.text)


#--------------------------------------------------
@bot.event
async def on_member_join(member):
  # chal=bot.get_channel(788505937693900823)
  chal=discord.utils.get(member.guilds.channel,name='general').id
  embed=discord.Embed(title=f"Welcome {member.name}",description=f"Have Fun in {member.guild.name}!")
  embed.set_thumbnail(url='https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80')
  await chal.send(embed=embed)

#--------------------------------------------------
@bot.command(name='create-channel',help='Creates a channel with given name')
@commands.has_role('Admin'or 'Lal')
async def create_channel(ctx,channel_name):
  guild=ctx.guild
  category = ctx.guild.category
  existing_channel=discord.utils.get(guild.channels,channel_name)
  if not existing_channel:
    await ctx.send(f"Creating channel {channel_name}!!")
  # await ctx.guild.create_category(channel_cataegory, overwrites=None)
    await ctx.guild.create_text_channel(channel_name,category=category,overwrites=None,reason=None)
  # else:
  #   await ctx.send("lal!")

#--------------------------------------------------
@bot.command(name='insult',help="Tell me the name of User who annoys you, I'll take care of it.",category='Toxic')
async def insult(ctx,user: discord.Member):
  if user.name==bot.user.name:
    await ctx.send(f"{ctx.author.mention} Bade harami ho beta!!")
  else:
    url = "https://evilinsult.com/generate_insult.php"
    params = {
      'lang': 'en',
      'type': 'json'
    }
    r = requests.get(url, params=params)
    ticktok = r.json()
    await ctx.send(f"{user.mention} " +ticktok['insult'])
#--------------------------------------------------

@bot.command(name='pull-paste',help='Retrieve Pastebin paste.Still Developing')
async def pull_paste(ctx):
  await ctx.send("Getting your paste!!")
  await ctx.send('`'+pull_paste_backfunc()+'`')

@bot.command(name='list-pastes')
async def list_pastes(ctx):
  res=list_pastes_backend()
  soup=BeautifulSoup(res,'html.parser')
  paste_key,paste_title=soup.paste.paste_key.string, soup.paste.paste_title.string
  await ctx.send("Pastes are:\n")
  await ctx.send("`Paste Title: "+paste_title+"\nPaste key: " +paste_key+'`')


keep_alive() #this function is important to be upar than bot.run(token)
bot.run(TOKEN)
# client.run(TOKEN)

