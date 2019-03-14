import discord
from discord.ext import commands
import time
import threading
import datetime
import json
from flask import Flask, render_template, request
from random import randint
from requests import get

#CUSTOM
import configFunctions
import extraFunctions
import auditlog
import chatLeaderboard

app = Flask(__name__)

def flaskThread():
    app.run(host='0.0.0.0')

#TOKEN = open("C://Users//mattd//OneDrive//Coding//Bertie Bot V3//BertieBotV3//token.txt", "r").read()
TOKEN = 'MjcxNzY2NTc5NTc2ODMyMDAw.Dy16UA.kUYz2bKmwGsW9vnJvyKNT1taCfs'

serverConfig = configFunctions.reloadServerConfig()
welcomeMessages = configFunctions.reloadWelcomeMessages()
client = commands.Bot(command_prefix = serverConfig['commandPrefix'])
serverid = open("dserverconfig/serverid.txt", "r").read()

@client.event
async def on_ready():
    print('Bot is ready')
    if len(client.servers) > 1:
        print("\033[1;37;41m Bot is connected to more than one server \033[0;37;40m")
    
    for cserver in client.servers:
        open("dserverconfig/serverid.txt", "w").write(cserver.id)
    if webThread.isAlive != True:
        webThread.start()


@client.event
async def on_member_join(member):
    auditlog.newMemberJoin(member, datetime.datetime.now())
    serverConfig = configFunctions.reloadServerConfig()
    welcomeMessages = configFunctions.reloadWelcomeMessages()
    try:
        if (serverConfig['defaultRole'] != None ):
            await client.add_roles(member, extraFunctions.getRole(member.server, serverConfig['defaultRole']))
    except:
        await client.send_message(member.server.owner, "There was an error adding the default role to a newly joined server member. Please login to the web panel and ensure that the role you have chosen still exists")
    
    if len(welcomeMessages) > 0:
        message = ""
        if len(welcomeMessages) == 1:
            message = welcomeMessages[0]['content']
        else:
            message = welcomeMessages[randint(0, len(welcomeMessages) - 1)]['content']
        
        if '{*USER*}' in message:
            message = message.replace('{*USER*}', member.mention)    
        await client.send_message(member.server.default_channel, message)

@client.event
async def on_member_remove(member):
    auditlog.memberLeave(member, datetime.datetime.now())

@client.command(pass_context=True)
async def echo(ctx):
    await client.say('ServerID: ' + ctx.message.server.id)
    await client.say('ChannelID: ' + ctx.message.channel.id)
    channel = client.get_channel(ctx.message.channel.id)
    await client.send_message(channel, 'oof')

@client.command(pass_context=True)
async def allroles(ctx):
    message = "Roles: \n"
    for role in ctx.message.server.roles:
        message += role.name + " : " + role.id + "\n"
    await client.say(message)

@client.command(pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) + 1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Messages deleted')

@client.command(pass_context=True)
async def xp(ctx):
    leaderboard = chatLeaderboard.loadLeaderboard()
    for row in leaderboard:
        if row['memberID'] == ctx.message.author.id:
            await client.say('You have ' + str(row['xp']) + 'XP ' + ctx.message.author.mention)

@client.command(pass_context=True)
async def leaderboard(ctx):
    leaderboard = chatLeaderboard.loadLeaderboard()
    leaderboard.sort(key = lambda x : x['xp'], reverse=True)

    serverConfig = configFunctions.reloadServerConfig()
    
    em = discord.Embed(title='Chat Leaderboard', colour=0x00D3DE)

    em.description = "The top 5 people on the leaderboard are:\n"

    appinfo = await client.application_info()
    em.set_author(name = appinfo.name, icon_url= appinfo.icon_url)
    iterations = 0
    for row in leaderboard:
        iterations += 1
        if iterations <= 5:
            em.description += str(iterations) + ".   " + row["name"] + ": " + str(row["xp"]) + "XP\n"
    
    if serverConfig["externalURL"] is not None:
        em.description += "Leaderboard available at: " + serverConfig['externalURL'] + ":5000/leaderboard"
    await client.send_message(ctx.message.channel, embed=em)       



@client.event
async def on_message(message):
    newMessage = {
        "id": message.id,
        "time": str(datetime.datetime.now().strftime("%d/%m/%y %I:%M%p")),
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

    chatLeaderboard.newMessage(message.author, message)
    await chatLeaderboard.autoRanks(message.author, message.server, client)
    

# ---- WEB SERVER ----#
@app.route("/")
def homePage():
    allChannelz = client.get_all_channels()

    totalMessagesPastMonth = 0
    with open('dserverconfig/ServerChatLog.json') as f:
        messages = json.load(f)
        for message in messages:
            if datetime.datetime.now() - datetime.datetime.strptime(message['time'], "%d/%m/%y %I:%M%p") < datetime.timedelta(days=30):
                totalMessagesPastMonth += 1
    return render_template("home.html", client=client, allChannelz=allChannelz, totalMessagesPastMonth=totalMessagesPastMonth)

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

@app.route("/memberjoin", methods=['GET', 'POST'])
def memberJoinPage():
    server = client.get_server(serverid)
    serverConfig = configFunctions.reloadServerConfig()


    autoRole = request.form.get("autoRole")
    if autoRole is not None:
        with open('dserverconfig/ServerConfig.json') as f:
            config = json.load(f)
        config["defaultRole"] = autoRole

        with open('dserverconfig/ServerConfig.json', 'w') as f:
            json.dump(config, f)
        serverConfig = configFunctions.reloadServerConfig()
    currentDefaultRole = extraFunctions.getRole(server, serverConfig["defaultRole"])

    newWelcomeMessage = request.form.get("newWelcomeMessage")
    if newWelcomeMessage is not None:
        messages = []

        with open('dserverconfig/WelcomeMessages.json') as f:
            messages = json.load(f)

        newWelcomeMessageEntry = {
            "id" : messages[-1]['id'] + 1,
            "creationTime" : datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "content" : newWelcomeMessage
        }

        with open('dserverconfig/WelcomeMessages.json', 'w') as f:
            messages.append(newWelcomeMessageEntry)
            json.dump(messages, f)

    removeMessage = request.form.get('removeMessage')
    if removeMessage is not None:
        messages = []   
        with open('dserverconfig/WelcomeMessages.json') as f:
            messages = json.load(f)

        for message in messages:
            if message['id'] == int(removeMessage):
                messages.remove(message)
        
        with open('dserverconfig/WelcomeMessages.json', 'w') as f:
            json.dump(messages, f)

    welcomeMessages = configFunctions.reloadWelcomeMessages()

    return render_template("memberjoin.html", client=client, allRoles = server.roles, currentDefaultRole=currentDefaultRole, data=request.values, welcomeMessages=welcomeMessages)

@app.route("/leaderboard")
def leaderboardPage():
    leaderboard = chatLeaderboard.loadLeaderboard()
    leaderboard.sort(key = lambda x : x['xp'], reverse=True) 
    return render_template("leaderboard.html", client = client, leaderboard = leaderboard)

@app.route('/autorank', methods=['GET', 'POST'])
def autoRankPage():
    if request.method == 'POST':
        newAutoRank = request.form.get('autoRank')
        newAutoRankXP = request.form.get('rankRequiredXP')
        if newAutoRank is not None and newAutoRankXP is not None:
            chatLeaderboard.addNewAutoRank(newAutoRank, newAutoRankXP)
    
    server = client.get_server(serverid)
    allRoles = server.roles
    for role in allRoles:
        if role.name == '@everyone':
            allRoles.remove(role)
    
    currentAutoRanks = chatLeaderboard.loadAutoRanks()
    currentAutoRanks.sort(key = lambda x : x['xp'], reverse=True)

    return render_template("autorank.html", extraFunctions = extraFunctions, allRoles = server.roles, currentAutoRanks = currentAutoRanks, client = client, server = server)

@app.route('/settings', methods=['GET', 'POST'])
def settingsPage():
    if request.method == 'POST':
        webURL = request.form.get('webAddress')
        if webURL is not None:
            configFunctions.updateWebURL(webURL)

    serverConfig = configFunctions.reloadServerConfig()
    return render_template("settings.html", serverConfig = serverConfig)

@app.route('/publicleaderboard')
def publicLeaderboardPage():
    server = client.get_server(serverid)

    leaderboard = chatLeaderboard.loadLeaderboard()
    leaderboard.sort(key = lambda x : x['xp'], reverse=True)    
    for user in leaderboard:
        leaderboard[leaderboard.index(user)]["roles"] = (server.get_member(user["memberID"]).roles)

    autoRanks = chatLeaderboard.loadAutoRanks()    
    for rank in autoRanks:
        autoRanks[autoRanks.index(rank)]["role"] = extraFunctions.getRole(server, rank['id'])

    return render_template("publicleaderboard.html", server = server, leaderboard = leaderboard, autoRanks = autoRanks)


@app.context_processor
def inject_channels():
    allChannels = client.get_all_channels()
    return dict(allChannels=allChannels) 
    
# Starts a seperate thread for the web server 
# allowing the bot and the webserver to run independantly
webThread = threading.Thread(target=flaskThread)
try:
    client.run(TOKEN)
except:
    try:
        client.run(TOKEN)
    except:
        raise