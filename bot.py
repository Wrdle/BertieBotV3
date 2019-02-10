import discord
from discord.ext import commands
import time
import threading
import datetime
import json
import configFunctions
import extraFunctions
from flask import Flask, render_template, request

app = Flask(__name__)

def flaskThread():
    app.run(host='0.0.0.0')

#TOKEN = open("C://Users//mattd//OneDrive//Coding//Bertie Bot V3//BertieBotV3//token.txt", "r").read()
TOKEN = 'MjcxNzY2NTc5NTc2ODMyMDAw.Dy16UA.kUYz2bKmwGsW9vnJvyKNT1taCfs'

serverConfig = configFunctions.reloadServerConfig()
client = commands.Bot(command_prefix = serverConfig['commandPrefix'])
serverid = open("dserverconfig/serverid.txt", "r").read()

@client.event
async def on_ready():
    print('Bot is ready')
    if len(client.servers) > 1:
        print("\033[1;37;41m Bot is connected to more than one server \033[0;37;40m")
    
    for cserver in client.servers:
        open("dserverconfig/serverid.txt", "w").write(cserver.id)
    webThread.start()


@client.event
async def on_member_join(member):
    serverConfig = configFunctions.reloadServerConfig()
    try:
        if (serverConfig['defaultRole'] != None ):
            await client.add_roles(member, extraFunctions.getRole(member.server, serverConfig['defaultRole']))
    except:
        await client.send_message(member.server.owner, "There was an error adding the default role to a newly joined server member. Please login to the web panel and ensure that the role you have chosen still exists")

@client.command(pass_context=True)
async def echo(ctx):
    await client.say('ServerID: ' + ctx.message.server.id)
    await client.say('ChannelID: ' + ctx.message.channel.id)
    channel = client.get_channel(ctx.message.channel.id)
    print(type(channel.id))
    await client.send_message(channel, 'oof')

@client.command(pass_context=True)
async def allroles(ctx):
    message = "Roles: \n"
    for role in ctx.message.server.roles:
        message += role.name + " : " + role.id + "\n"
    await client.say(message)


@client.event
async def on_message(message):
    newMessage = {
        "id": message.id,
        "time": str(message.timestamp),
        "channel": message.channel.id,
        "user": message.author.id,
        "content": message.content,
        "tts": str(message.tts),
        "attachments": str(message.attachments)
    }
    with open('dserverconfig/ServerChatLog.json') as f:
        data = json.load(f)
    data.append(newMessage)

    with open('dserverconfig/ServerChatLog.json', 'w') as f:
        json.dump(data, f)
    await client.process_commands(message)
    

# ---- WEB SERVER ----#
@app.route("/")
def homePage():
    allChannelz = client.get_all_channels()
    return render_template("home.html", client=client, allChannelz=allChannelz)

@app.route("/channel", methods=['GET'])
def channelPage():
    currentChannel = client.get_channel(request.values.get('channelid'))
    with open('dserverconfig/ServerChatLog.json') as f:
        data = json.load(f)

    channelLog = []
    for message in reversed(data):
        if message["channel"] == currentChannel.id:
            channelLog.append(message)
    return render_template("channel.html", client=client, channelLog=channelLog, currentChannel=currentChannel)

@app.route("/memberjoin", methods=['GET'])
def memberJoinPage():
    server = client.get_server(serverid)
    autoRole = request.args.get("autoRole")
    if autoRole is not None:
        with open('dserverconfig/ServerConfig.json') as f:
            config = json.load(f)
        config["defaultRole"] = autoRole

        with open('dserverconfig/ServerConfig.json', 'w') as f:
            json.dump(config, f)
        serverConfig = configFunctions.reloadServerConfig()

    currentDefaultRole = extraFunctions.getRole(server, serverConfig["defaultRole"])
    return render_template("memberjoin.html", client=client, allRoles = server.roles, currentDefaultRole=currentDefaultRole, data=request.values)
    

@app.context_processor
def inject_channels():
    allChannels = client.get_all_channels()
    return dict(allChannels=allChannels) 

webThread = threading.Thread(target=flaskThread)
client.run(TOKEN)