from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import threading

app=Flask(__name__)

def create_app(discordClient):
    global client
    client = discordClient

    # this is the name of the module/package that is calling this app
    app.debug=False
    app.secret_key='notASecret'

    bootstrap = Bootstrap(app)

    from . import adminPanel 
    app.register_blueprint(adminPanel.bp)

    from . import publicLeaderboard
    app.register_blueprint(publicLeaderboard.bp)

    return app