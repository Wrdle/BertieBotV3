import json
import os
import logging

'''
logger = logging.getLogger('discord')
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='log.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
'''

def reloadServerConfig():
    serverConfig = None
    try:
        with open('configFiles/ServerConfig.json') as f:
            serverConfig = json.load(f)
    except:
        #logger.info("Either file 'ServerConfig.json' or directory 'configFiles'")
        try:
            os.makedirs('configFiles')
        except:
            pass
            #logger.info("Directory 'configFiles', already exists")

        #logger.info("Attempting to create file 'configFiles/ServerConfig.json'")
        with open ('configFiles/ServerConfig.json', 'w+') as f:
            serverConfig = {
                "defaultRole": None, 
                "externalDomain": None,
                "commandPrefix": ".",
                "token": None,
                "greetingChannel": None,
                "portNumber": 5000,
                "publicLeaderboardFont": None
            }
            json.dump(serverConfig, f)
    return serverConfig

def saveServerConfig(config):
    with open('configFiles/ServerConfig.json', 'w+') as f:
        json.dump(config, f)

def updateWebURL(url):
    serverConfig = None
    with open('configFiles/ServerConfig.json') as f:
        serverConfig = json.load(f)

    if url.strip() != "":
        serverConfig['externalURL'] = url
    else:
        serverConfig['externalURL'] = None

    with open('configFiles/ServerConfig.json', 'w') as f:
        json.dump(serverConfig, f)
        
def getAutoRole():
    return reloadServerConfig()["defaultRole"]

def setAutoRole(roleID):
    serverConfig = reloadServerConfig()
    serverConfig["defaultRole"] = roleID
    saveServerConfig(serverConfig)

def setGreetingChannelID(channelId):
    serverConfig = reloadServerConfig()
    if id == None:
        serverConfig["greetingChannel"] = None
    else: 
        serverConfig["greetingChannel"] = id
    saveServerConfig(serverConfig)

def getGreetingChannelID():
        return reloadServerConfig()["grettingChannel"]

def getCommandPrefix():
    return reloadServerConfig()["commandPrefix"]

def getBotToken():
    return reloadServerConfig()["token"]

def setBotToken(token):
    serverConfig = reloadServerConfig()
    serverConfig["token"] = token
    saveServerConfig(serverConfig)

def setPortNumber(portNumber):
    serverConfig = reloadServerConfig()
    serverConfig["portNumber"] = portNumber
    saveServerConfig(serverConfig)

def getPortNumber():
    return reloadServerConfig()["portNumber"]

def getPublicLeaderboardFont():
    return reloadServerConfig()["publicLeaderboardFont"]

def setPublicLeaderboardFont(fontName):
    serverConfig = reloadServerConfig()
    serverConfig["publicLeaderboardFont"] = fontName
    saveServerConfig(serverConfig)
