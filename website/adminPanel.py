from flask import Blueprint, render_template, request, url_for
import json

import start
from . import client, isDiscordBotReady
from settings import configFunctions, extraFunctions, welcomeMessages, serverChatLog, chatLeaderboard
from flask_login import login_required, current_user
from settings import botDB

bp = Blueprint('adminPanel', __name__)

@bp.route('/')
@login_required
def index():
    status = isDiscordBotReady()
    if status is not True:
        return status

    allTextChannels = extraFunctions.getAllTextChannels(client.get_guild(start.serverid))
    return render_template("home.html", client=client, allChannels=allTextChannels)


@bp.route("/joinmessages", methods=['GET', 'POST'])
@login_required
def joinMessages():
    status = isDiscordBotReady()
    if status is not True:
        return status

    allTextChannels = extraFunctions.getAllTextChannels(client.get_guild(start.serverid))
    #Checks if message sent from website is empty. If its not, add it to WelcomeMessages.json
    message = request.form.get("newWelcomeMessage")
    if message is not None:
        welcomeMessages.newMessage(message)

    greetingChannel = request.form.get('greetingChannel')
    if greetingChannel == "NoSelectedChannel":
        configFunctions.setGreetingChannelID(None)
    elif greetingChannel is not None:
        configFunctions.setGreetingChannelID(int(greetingChannel))
        
    #Checks if user requested to remove a message by checking if ID is empty.
    #If not empty, remove message with ID
    removeMessageID = request.form.get('removeMessage')
    if removeMessageID is not None:
        welcomeMessages.removeMessage(removeMessageID)

    allWelcomeMessages = welcomeMessages.getAllWelcomeMessages()
    currentGreetingChannelID = configFunctions.getGreetingChannelID()
    return render_template("joinmessages.html", client=client, allChannels=allTextChannels, currentGreetingChannelID = currentGreetingChannelID, welcomeMessages = allWelcomeMessages)


@bp.route("/channel", methods=['GET'])
@login_required
def channelPage():
    status = isDiscordBotReady()
    if status is not True:
        return status

    allTextChannels = extraFunctions.getAllTextChannels(client.get_guild(start.serverid))
    channel = client.get_channel(int(request.values.get('channelid')))
    channelLog = serverChatLog.getChannelLog(channel)
    return render_template("channel.html", allChannels=allTextChannels, client=client, channelLog=channelLog, currentChannel=channel)


@bp.route('/ranking', methods=['GET', 'POST'])
@login_required
def ranking():
    status = isDiscordBotReady()
    if status is not True:
        return status

    serverConfig = configFunctions.reloadServerConfig()
    if request.method == 'POST':
        removeRankID = request.form.get('removeRankID')
        if removeRankID is not None:
            chatLeaderboard.removeAutoRank(removeRankID)

        newAutoRank = request.form.get('autoRank')
        newAutoRankXP = request.form.get('rankRequiredXP')
        newAutoRankInvites = request.form.get('rankRequiredInvites')
        if newAutoRank is not None and newAutoRankXP is not None and newAutoRankInvites is not None:
            chatLeaderboard.addNewAutoRank(newAutoRank, newAutoRankXP, newAutoRankInvites)

    currentAutoRanks = chatLeaderboard.loadAutoRanks()
    currentAutoRanks.sort(key = lambda x : x.xp, reverse=True)

    server = client.get_guild(start.serverid)
    allRolesLoop = server.roles
    allAvailableRoles = server.roles
    for role in allRolesLoop:
        if role.name == '@everyone':
            allAvailableRoles.remove(role)
            continue

        for autoRank in currentAutoRanks:
            if role.id == autoRank.rankID:
                allAvailableRoles.remove(role)
                autoRank.name = role.name

    autoRole = request.form.get("autoRole")
    if autoRole is not None:
        with open('configFiles/ServerConfig.json') as f:
            config = json.load(f)
        config["defaultRole"] = int(autoRole)

        with open('configFiles/ServerConfig.json', 'w') as f:
            json.dump(config, f)
        serverConfig = configFunctions.reloadServerConfig()
    currentDefaultRole = extraFunctions.getRole(server, serverConfig["defaultRole"])

    allTextChannels = extraFunctions.getAllTextChannels(client.get_guild(start.serverid))

    return render_template("ranking.html", extraFunctions = extraFunctions, allRoles = server.roles, currentDefaultRole=currentDefaultRole, allChannels = allTextChannels, data=request.values, allAvailableRoles = allAvailableRoles, currentAutoRanks = currentAutoRanks, client = client, server = server)

@bp.route("/leaderboard")
@login_required
def leaderboardPage():
    status = isDiscordBotReady()
    if status is not True:
        return status

    leaderboard = chatLeaderboard.loadLeaderboard()
    leaderboard.sort(key = lambda x : x.xp, reverse=True) 

    allTextChannels = extraFunctions.getAllTextChannels(client.get_guild(start.serverid))
    return render_template("leaderboard.html", client = client, allChannels=allTextChannels, leaderboard = leaderboard)

@bp.route('/websitesettings', methods=['GET', 'POST'])
@login_required
def settingsPage():
    status = isDiscordBotReady()
    if status is not True:
        return status

    serverConfig = configFunctions.reloadServerConfig()
    allTextChannels = extraFunctions.getAllTextChannels(client.get_guild(start.serverid))
    return render_template("websitesettings.html", allChannels=allTextChannels, serverConfig = serverConfig)

@bp.route('/botsettings', methods=['GET', 'POST'])
@login_required
def botSettings():
    status = isDiscordBotReady()
    if status is not True:
        return status

    serverConfig = configFunctions.reloadServerConfig()
    allTextChannels = extraFunctions.getAllTextChannels(client.get_guild(start.serverid))
    return render_template("botsettings.html", allChannels = allTextChannels, serverConfig = serverConfig)