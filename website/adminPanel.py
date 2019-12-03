from flask import Blueprint, render_template, request, url_for
import json

import start
from . import client
from settings import configFunctions, extraFunctions, welcomeMessages, serverChatLog, chatLeaderboard

bp = Blueprint('adminPanel', __name__)

@bp.route('/')
def index():
    allTextChannels = extraFunctions.getAllTextChannels(client.get_guild(start.serverid))
    return render_template("home.html", client=client, allChannels=allTextChannels)


@bp.route("/memberjoin", methods=['GET', 'POST'])
def memberJoinPage():
    server = client.get_guild(start.serverid)
    serverConfig = configFunctions.reloadServerConfig()


    autoRole = request.form.get("autoRole")
    if autoRole is not None:
        with open('configFiles/ServerConfig.json') as f:
            config = json.load(f)
        config["defaultRole"] = int(autoRole)

        with open('dserverconfig/ServerConfig.json', 'w') as f:
            json.dump(config, f)
        serverConfig = configFunctions.reloadServerConfig()
    currentDefaultRole = extraFunctions.getRole(server, serverConfig["defaultRole"])

    #Checks if message sent from website is empty. If its not, add it to WelcomeMessages.json
    message = request.form.get("newWelcomeMessage")
    if message is not None:
        welcomeMessages.newMessage(message)
        
    #Checks if user requested to remove a message by checking if ID is empty.
    #If not empty, remove message with ID
    removeMessageID = request.form.get('removeMessage')
    if removeMessageID is not None:
        welcomeMessages.removeMessage(removeMessageID)

    allWelcomeMessages = welcomeMessages.getAllWelcomeMessages()

    return render_template("memberjoin.html", client=client, allRoles = server.roles, currentDefaultRole=currentDefaultRole, data=request.values, welcomeMessages=allWelcomeMessages)

@bp.route("/channel", methods=['GET'])
def channelPage():
    allTextChannels = extraFunctions.getAllTextChannels(client.get_guild(start.serverid))
    channel = client.get_channel(int(request.values.get('channelid')))
    channelLog = serverChatLog.getChannelLog(channel)
    return render_template("channel.html", client=client, channelLog=channelLog, currentChannel=channel, allChannels=allTextChannels)

@bp.route('/autorank', methods=['GET', 'POST'])
def autoRankPage():
    if request.method == 'POST':
        removeRankID = request.form.get('removeRankID')
        if removeRankID is not None:
            chatLeaderboard.removeAutoRank(removeRankID)

        newAutoRank = request.form.get('autoRank')
        newAutoRankXP = request.form.get('rankRequiredXP')
        if newAutoRank is not None and newAutoRankXP is not None:
            chatLeaderboard.addNewAutoRank(newAutoRank, newAutoRankXP)

    currentAutoRanks = chatLeaderboard.loadAutoRanks()
    currentAutoRanks.sort(key = lambda x : x.xp, reverse=True)

    server = client.get_guild(start.serverid)
    allRolesLoop = server.roles
    allRoles = server.roles
    for role in allRolesLoop:
        if role.name == '@everyone':
            allRoles.remove(role)
            continue

        for autoRank in currentAutoRanks:
            if role.id == autoRank.rankID:
                allRoles.remove(role)
                autoRank.name = role.name

    return render_template("autorank.html", extraFunctions = extraFunctions, allRoles = allRoles, currentAutoRanks = currentAutoRanks, client = client, server = server)