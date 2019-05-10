import json

def reloadServerConfig():
    serverConfig = None
    try:
        with open('dserverconfig/ServerConfig.json') as f:
            serverConfig = json.load(f)
    except:
        print('Error opening server config. File may not exist.')
        with open ('dserverconfig/ServerConfig.json', 'w+') as f:
            serverConfig = {
                "defaultRole": None, 
                "externalDomain": None,
                "commandPrefix": ".",
                "token": None,
                "greetingChannel": None
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
