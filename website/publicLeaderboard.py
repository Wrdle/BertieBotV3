from flask import Blueprint, render_template, request, url_for
import json

import start
from . import client
from settings import configFunctions, extraFunctions, welcomeMessages, serverChatLog, chatLeaderboard

bp = Blueprint('publicLeaderboard', __name__)

@bp.route('/serverleaderboard')
def publicLeaderboardPage():
    server = client.get_guild(start.serverid)

    leaderboard = chatLeaderboard.loadLeaderboard()
    leaderboard.sort(key = lambda x : x.xp, reverse=True) # Sort leaderboard by XP
    for user in leaderboard: # Attach roles to each leaderboard member
        member = server.get_member(user.userID)
        leaderboard[leaderboard.index(user)].roles = member.roles
        user.name = member.name

    autoRanks = chatLeaderboard.loadAutoRanks()    
    for rank in autoRanks:
        autoRanks[autoRanks.index(rank)].role = extraFunctions.getRole(server, str(rank.rankID))

    return render_template("publicleaderboard.html", server = server, leaderboard = leaderboard, autoRanks = autoRanks, client = client)
