from flask import Blueprint, render_template, request, url_for, flash, redirect
import json, os
from werkzeug import secure_filename

import start
from . import client
from settings import fancyStats, configFunctions, extraFunctions, welcomeMessages, serverChatLog, chatLeaderboard

bp = Blueprint('fancyStatsAPI', __name__, url_prefix='/fancyStatsAPI')

@bp.route('/memberCount', methods=['POST'])
def memberCount():
    enabled = request.form.get('enabled')
    if enabled == 'true':
        pass
        #async_to_sync(fancyStats.enableChannelStat)(client, client.get_guild(start.serverid), "Member Count")
    return "oof"

