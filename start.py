import threading
from discord.ext import commands
import discord

from website import create_app
from cogs import main
from settings import configFunctions

serverconfig = configFunctions.reloadServerConfig()

client =  commands.Bot(command_prefix=commands.when_mentioned_or(serverconfig["commandPrefix"]), description='Your local BertieBot')

global serverid

def startWebsite():
    napp=create_app(client)
    napp.run(port=5000)

if __name__=='__main__':
    websiteThread = threading.Thread(target=startWebsite)
    websiteThread.start()
    client.add_cog(main.Main(client))
    client.add_cog(main.Events(client))
    client.run(configFunctions.getBotToken())

