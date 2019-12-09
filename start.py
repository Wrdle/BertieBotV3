import threading
from discord.ext import commands
import discord

from website import create_app
from cogs import generalCommands, events, leaderboard
from settings import configFunctions

global client
client =  commands.Bot(command_prefix=commands.when_mentioned_or(configFunctions.getCommandPrefix()), description='Your local BertieBot')

global serverid

def startWebsite():
    napp=create_app(client)
    napp.run('0.0.0.0', port=configFunctions.getPortNumber())

if __name__=='__main__':
    websiteThread = threading.Thread(target=startWebsite)
    websiteThread.start()
    client.add_cog(generalCommands.GeneralCommands(client))
    client.add_cog(events.Events(client))
    client.add_cog(leaderboard.Leaderboard(client))
    client.run(configFunctions.getBotToken())

