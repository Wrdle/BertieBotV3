import discord
import os
import sqlite3
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
import config_modules.auditLog as auditLogConfig
import config_modules.serverChatLog as serverChatLogConfig
import config_modules.chatLeaderboard as chatLeaderboardConfig
import config_modules.welcomeMessages as welcomeMessagesConfig

app = Flask(__name__)

def flaskThread():
    app.run(host='0.0.0.0', port=int("8080"))

client = commands.Bot(command_prefix = configFunctions.getCommandPrefix())
serverid = int(open("dserverconfig/serverid.txt", "r").read())

@client.event
async def on_ready():
    print('Bot is ready')
    if len(client.guilds) > 1:
        print("\033[1;37;41m Bot is connected to more than one server \033[0;37;40m")
    
    for cserver in client.guilds:
        open("dserverconfig/serverid.txt", "w").write(str(cserver.id))

    sql = None

    if os.path.isfile('./botdatabase.db') != True:
        conn = sqlite3.connect('botdatabase.db')
        sql = conn.cursor()

        sql.execute('CREATE TABLE ChatLog (messageID integer NOT NULL UNIQUE PRIMARY KEY, channelID integer NOT NULL, userID integer NOT NULL, content text, tts blob, attachments blob, time text NOT NULL);')
        sql.execute("CREATE TABLE ChatLeaderboard (userID integer NOT NULL UNIQUE PRIMARY KEY, xp integer NOT NULL);")
        sql.execute("CREATE TABLE WelcomeMessages (wMessageID integer NOT NULL UNIQUE PRIMARY KEY, creationTime text NOT NULL, content text NOT NULL);")
        sql.execute("CREATE TABLE AutoRanks (roleID integer NOT NULL UNIQUE PRIMARY KEY, xp integer NOT NULL);")

        conn.commit()
        sql.close()
    if webThread.isAlive != True:
        webThread.start()

@client.event
async def on_message(message):
    serverChatLogConfig.newMessage(message)
    await client.process_commands(message)
    chatLeaderboardConfig.newMessage(message.author, message)
    await chatLeaderboardConfig.autoRank(message.author, message.guild)

@client.event
async def on_member_join(member):
    auditLogConfig.newMemberJoin(member, datetime.datetime.now())
    serverConfig = configFunctions.reloadServerConfig()

    try:
        if serverConfig['defaultRole'] != None:
            await member.add_roles(member.guild.get_role(configFunctions.getAutoRole()))
    except:
        if member.dm_channel == None:
            await member.create_dm()
        await member.dm_channel.send("There was an error adding the default role to a newly joined server member. Please login to the web panel and ensure that the role you have chosen still exists")

    # NEED TO ADD A WAY FOR THE USER TO SELECT A CHANNEL IN WEBSITE GUI TO SEND MESSAGES TO   
    if serverConfig["greetingChannel"] != None:
        greetingChannel = client.get_channel(serverConfig["greetingChannel"])
        greetingChannel.send(welcomeMessagesConfig.getRandomMessage(member))

@client.event
async def on_member_remove(member):
    auditLogConfig.memberLeave(member, datetime.datetime.now())

@client.command(pass_context=True)
async def echo(ctx):
    await ctx.channel.send('ServerID: ' + str(ctx.guild.id))
    await ctx.channel.send('ChannelID: ' + str(ctx.channel.id))

@client.command(pass_context=True)
async def allroles(ctx):
    message = "Roles: \n"
    for role in ctx.guild.roles:
        message += role.name + " : " + str(role.id) + "\n"
    await ctx.channel.send(message)

@client.command(pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=int(amount) + 1):
        messages.append(message)
    await channel.delete_messages(messages)
    await channel.send('Messages deleted')

@client.command(pass_context=True)
async def xp(ctx):
    xp = chatLeaderboardConfig.getMemberXP(ctx.message.author)
    await ctx.channel.send('You have ' + str(xp) + 'XP ' + ctx.message.author.mention)

@client.command(pass_context=True)
async def leaderboard(ctx):
    leaderboard = chatLeaderboardConfig.loadLeaderboard()
    leaderboard.sort(key = lambda x : x.xp, reverse=True)

    serverConfig = configFunctions.reloadServerConfig()
    
    em = discord.Embed(title='Chat Leaderboard', colour=0x00D3DE)
    em.description = "The top 5 people on the leaderboard are:\n"

    appinfo = await client.application_info()
    em.set_author(name = appinfo.name, icon_url= appinfo.icon_url)
    iterations = 0
    for row in leaderboard:
        iterations += 1
        if iterations <= 5:
            user = await client.fetch_user(row.userID)
            em.description += str(iterations) + ".   " + user.name + ": " + str(row.xp) + "XP\n"
    
    if serverConfig["externalURL"] is not None:
        em.description += "Leaderboard available at: " + serverConfig['externalURL'] + ":5000/leaderboard"
    await ctx.channel.send(embed=em)       

@client.command(pass_context=True)
async def getRandomWelcomeMessage(ctx):
    await ctx.channel.send(welcomeMessagesConfig.getRandomMessage(ctx.message.author))

# ---- WEB SERVER ----#
@app.route("/")
def homePage():
    totalMessagesPastMonth = 0
    messages = serverChatLogConfig.getAllMessages()
    for message in messages:
        if datetime.datetime.now() - datetime.datetime.strptime(message.time, "%d/%m/%y %I:%M%p") < datetime.timedelta(days=30):
            totalMessagesPastMonth += 1
    return render_template("home.html", client=client, totalMessagesPastMonth=totalMessagesPastMonth)

@app.route("/channel", methods=['GET'])
def channelPage():
    channel = client.get_channel(int(request.values.get('channelid')))
    channelLog = serverChatLogConfig.getChannelLog(channel)
    return render_template("channel.html", client=client, channelLog=channelLog, currentChannel=channel)

@app.route("/memberjoin", methods=['GET', 'POST'])
def memberJoinPage():
    guild = client.get_guild(serverid)

    autoRole = request.form.get("autoRole")
    if autoRole is not None:
        configFunctions.setAutoRole(int(autoRole))
    
    currentDefaultRole = guild.get_role(configFunctions.getAutoRole())

    #Checks if message sent from website is empty. If its not, add it to WelcomeMessages.json
    message = request.form.get("newWelcomeMessage")
    if message is not None:
        welcomeMessagesConfig.newMessage(message)
        
    #Checks if user requested to remove a message by checking if ID is empty.
    #If not empty, remove message with ID
    removeMessageID = request.form.get('removeMessage')
    if removeMessageID is not None:
        welcomeMessagesConfig.removeMessage(removeMessageID)

    allWelcomeMessages = welcomeMessagesConfig.getAllWelcomeMessages()
    return render_template("memberjoin.html", client=client, allRoles = guild.roles, currentDefaultRole=currentDefaultRole, data=request.values, welcomeMessages=allWelcomeMessages)

@app.route("/leaderboard")
def leaderboardPage():
    leaderboard = chatLeaderboardConfig.loadLeaderboard()
    leaderboard.sort(key = lambda x : x['xp'], reverse=True) 
    return render_template("leaderboard.html", client = client, leaderboard = leaderboard)

@app.route('/autorank', methods=['GET', 'POST'])
def autoRankPage():
    if request.method == 'POST':
        removeRankID = request.form.get('removeRankID')
        if removeRankID is not None:
            chatLeaderboardConfig.removeAutoRank(removeRankID)

        newAutoRank = request.form.get('autoRank')
        newAutoRankXP = request.form.get('rankRequiredXP')
        if newAutoRank is not None and newAutoRankXP is not None:
            chatLeaderboardConfig.addNewAutoRank(newAutoRank, newAutoRankXP)

    currentAutoRanks = chatLeaderboardConfig.loadAutoRanks()
    currentAutoRanks.sort(key = lambda x : x.xp, reverse=True)

    guild = client.get_guild(serverid)
    allRoles = guild.roles
    for role in allRoles:
        if role.name == '@everyone':
            allRoles.remove(role)
        for autoRank in currentAutoRanks:
            if role.id == autoRank.rankID:
                allRoles.remove(role)
                autoRank.name = role.name

    return render_template("autorank.html", allRoles = allRoles, currentAutoRanks = currentAutoRanks, client = client)

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
    guild = client.get_guild(serverid)

    leaderboard = chatLeaderboardConfig.loadLeaderboard()
    leaderboard.sort(key = lambda x : x.xp, reverse=True) # Sort leaderboard by XP
    for user in leaderboard: # Attach roles to each leaderboard member
        member = guild.get_member(user.userID)
        leaderboard[leaderboard.index(user)].roles = member.roles
        user.name = member.name

    autoRanks = chatLeaderboardConfig.loadAutoRanks()    
    for rank in autoRanks:
        autoRanks[autoRanks.index(rank)].role = guild.get_role(rank.rankID)

    return render_template("publicleaderboard.html", guild = guild, leaderboard = leaderboard, autoRanks = autoRanks, client = client)

@app.context_processor
def inject_channels():
    allChannels = client.get_all_channels()
    return dict(allChannels=allChannels) 
    
# Starts a seperate thread for the web server 
# allowing the bot and the webserver to run independantly
webThread = threading.Thread(target=flaskThread)
try:
    client.run(configFunctions.getBotToken())
except:
    try:
        client.run(configFunctions.getBotToken())
    except:
        raise