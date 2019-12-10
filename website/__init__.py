from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
import threading
from flask_login import LoginManager
import asyncio

global flaskLoop
flaskLoop = asyncio.get_event_loop()
app=Flask(__name__)

def create_app(discordClient):
    global client
    client = discordClient

    # this is the name of the module/package that is calling this app
    app.debug=False
    app.secret_key='notASecret'

    bootstrap = Bootstrap(app)

    UPLOAD_FOLDER = 'website\\static\\fonts'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    #initialize the login manager
    login_manager = LoginManager()

    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from settings.models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.getWithID(int(user_id))

    from . import adminPanel 
    app.register_blueprint(adminPanel.bp)

    from . import publicLeaderboard
    app.register_blueprint(publicLeaderboard.bp)

    from . import settingsAPI
    app.register_blueprint(settingsAPI.bp)

    from . import fancyStatsAPI
    app.register_blueprint(fancyStatsAPI.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    @app.errorhandler(404)
    def pageNotFound(e):
        return render_template('404.html'), 404

    return app

def isDiscordBotReady():
    if not client.is_ready():
        return render_template('notready.html')
    return True