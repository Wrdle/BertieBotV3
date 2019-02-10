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
                "customWelcomeMessages": False,
                "commandPrefix": "."
            }
            json.dump(serverConfig, f)
    return serverConfig