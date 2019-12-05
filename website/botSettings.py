from flask import Blueprint, render_template, request, url_for, flash, redirect
import json, os
from werkzeug import secure_filename

import start
from . import client
from settings import configFunctions, extraFunctions, welcomeMessages, serverChatLog, chatLeaderboard

bp = Blueprint('botSettings', __name__, url_prefix='/botSettings')

ALLOWED_EXTENSIONS = set(['ttf', 'otf'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/processSettings', methods=['POST'])
def processSettings():
    description = request.form.get('description')
    if description == "webAddressUpdate":
        webURL = request.form.get('webAddress')
        if webURL is not None:
            configFunctions.updateWebURL(webURL)
            return("URL updated")
    elif description == "resetFont":
        configFunctions.setPublicLeaderboardFont(None)
        return("Font reset")

@bp.route('/uploadFont', methods=['POST'])
def processFontUpload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = "/website/static/fonts/" + secure_filename(file.filename)
        print(os.path.join(filename))
        file.save(os.path.join(filename))
        configFunctions.setPublicLeaderboardFont(filename)
        return 'Upload Successful'

@bp.route('/processBotSettings', methods=['POST'])
def processBotSettings():
    description = request.form.get('description')
    if description == 'portNumberUpdate':
        portNumber = request.form.get('portNumber')
        if portNumber is not None:
            configFunctions.setPortNumber(portNumber)
            return "Port number updated"
    elif description == 'botTokenUpdate':
        botToken = request.form.get('botToken')
        if botToken is not None:
            configFunctions.setBotToken(botToken)
            return "Bot token updated"

