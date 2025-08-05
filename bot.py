import os
import io #because someone else decided to use print command
from contextlib import redirect_stdout

import discord
from dotenv import load_dotenv #so yall cant steal my discord
import re #because stupid
import datetime
import shutil
from id import id_from_cam#id.py
import sys
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stderr
        sys.stdout = self._stringio = io.StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stderr = self._stdout
def day_month_year():
    return datetime.datetime.now().strftime("%d-%m-%Y")

#sorry, global variable
load_dotenv("/home/qsqcqs/py/.env")
TOKEN = os.getenv('DISCORD_TOKEN')
#GUILD = os.getenv('DISCORD_GUILD')
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = io.StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout




intents = discord.Intents.all()
client = discord.Client(intents=intents)


async def take_pic_n_send():
    try:
        shutil.rmtree("runs")
    except:
        pass
    with Capturing() as output:
        id_from_cam()
    val=str(output)

    image=discord.File(os.getcwd()+"/runs/segment/predict/image0.jpg")
    val=re.sub("\n"," ",val)
    val=eval(val)
    if val[0]=="no cracks lol":
        return
    crackdata=""
    print(val[0])
    if(val.__len__()%2==0):
        
        for i in range(0,int(val.__len__()/2)):
            
            crackdata+=f"{val[2*i]}\n{val[2*i+1]}\n"
    print(crackdata)
    guild="need to do this bc python is dumb about scope"
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

@client.event
async def on_message(message):
    if message.content==".cap":
        await take_pic_n_send()


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