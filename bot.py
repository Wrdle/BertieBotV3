import discord
from discord.ext import commands
import time
import threading
from flask import Flask, render_template

app= Flask(__name__)

def flaskThread():
    app.run()

#TOKEN = open("C://Users//mattd//OneDrive//Coding//Bertie Bot V3//BertieBotV3//token.txt", "r").read()
TOKEN = 'MjcxNzY2NTc5NTc2ODMyMDAw.Dy16UA.kUYz2bKmwGsW9vnJvyKNT1taCfs'

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot is ready')
    webThread.start()

@client.command(pass_context=True)
async def echo(ctx):
    await client.say('ServerID: ' + ctx.message.server.id)
    await client.say('ChannelID: ' + ctx.message.channel.id)
    channel = client.get_channel(ctx.message.channel.id)
    print(type(channel.id))
    await client.send_message(channel, 'oof')

@client.command()
async def oof():
    await client.say('Testing')

@app.route("/")
def homePage():
    allChannelz = client.get_all_channels()
    return render_template("home.html", client=client, allChannelz=allChannelz)

@app.context_processor
def inject_channels():
    allChannels = client.get_all_channels()
    return dict(allChannels=allChannels) 

webThread = threading.Thread(target=flaskThread)
client.run(TOKEN)
