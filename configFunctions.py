import json
import os
import logging

logger = logging.getLogger('discord')
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='log.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def reloadServerConfig():
    serverConfig = None
    try:
        with open('dserverconfig/ServerConfig.json') as f:
            serverConfig = json.load(f)
    except:
        logger.info("Either file 'ServerConfig.json' or directory 'dserverconfig'")
        try:
            os.makedirs('dserverconfig')
        except:
            logger.info("Directory 'dserverconfig', already exists")

        logger.info("Attempting to create file 'dserverconfig/ServerConfig.json'")
        with open ('dserverconfig/ServerConfig.json', 'w+') as f:
            serverConfig = {
                "defaultRole": None, 
                "externalDomain": None,
                "commandPrefix": ".",
                "token": None,
                "greetingChannel": None,
                "publicLeaderboardFont": None
            }
            json.dump(serverConfig, f)
    return serverConfig

def saveServerConfig(config):
    with open('dserverconfig/ServerConfig.json', 'w+') as f:
        json.dump(config, f)

def updateWebURL(url):
    serverConfig = None
    with open('dserverconfig/ServerConfig.json') as f:
        serverConfig = json.load(f)

    if url.strip() != "":
        serverConfig['externalURL'] = url
    else:
        serverConfig['externalURL'] = None

    with open('dserverconfig/ServerConfig.json', 'w') as f:
        json.dump(serverConfig, f)
        
def getAutoRole():
    return reloadServerConfig()["defaultRole"]

def setAutoRole(roleID):
    serverConfig = reloadServerConfig()
    serverConfig["defaultRole"] = roleID
    saveServerConfig(serverConfig)

def getCommandPrefix():
    return reloadServerConfig()["commandPrefix"]

def getBotToken():
    return reloadServerConfig()["token"]

def setBotToken(token):
    serverConfig = reloadServerConfig()
    serverConfig["token"] = token
    saveServerConfig(serverConfig)

def getPublicLeaderboardFont():
    return reloadServerConfig()["publicLeaderboardFont"]

def setPublicLeaderboardFont(fontName):
    serverConfig = reloadServerConfig()
    serverConfig["publicLeaderboardFont"] = fontName
    saveServerConfig(serverConfig)
