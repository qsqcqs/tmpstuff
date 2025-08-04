import os
import time
import discord
from dotenv import load_dotenv
import datetime
def day_month_year():
    return datetime.datetime.now().strftime("%d-%m-%Y")
import sys
crackdata=""
if(sys.argv.__len__()%2==0):
    for i in range(0,int(sys.argv.__len__()/2)-1):
        
        crackdata+=f"{sys.argv[2*i+1]}\n{sys.argv[2*i+2]}\n"
#sorry, global variable
load_dotenv("/home/qsqcqs/py/.env")
TOKEN = os.getenv('DISCORD_TOKEN')
#GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
image=discord.File(os.getcwd()+"/"+sys.argv[-1]+"/image0.jpg")
@client.event
async def on_ready():
    guild="need to do this bc python is dumb"
    for tmp_guild in client.guilds:
        if tmp_guild.name == "image dump":
            guild=tmp_guild
    channel="not defined yet"
    for tmp_channel in guild.channels:
        
        if tmp_channel.name == day_month_year():
            channel=tmp_channel
    if channel=="not defined yet":
        channel = await guild.create_text_channel(day_month_year())
    await channel.send(crackdata[:-1],file=image)
    sys.exit(0)

#@client.event
#async def on_message(message):
#    if message.author==client.user:
#        return
#    if isinstance(message.channel, discord.DMChannel):
#        # Reply to the DM
#        await message.channel.send("test upload pics lol")

                        

    
#    f'{guild.name}(id: {guild.id})'
#@client.event
#async def on_message(message):

        

client.run(TOKEN)