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
                "commandPrefix": "."
            }
            json.dump(serverConfig, f)
    return serverConfig

def updateWebURL(url):
    serverConfig = None
    with open('dserverconfig/ServerConfig.json') as f:
        serverConfig = json.load(f)

    serverConfig['externalURL'] = url

    with open('dserverconfig/ServerConfig.json', 'w') as f:
        json.dump(serverConfig, f)


def reloadWelcomeMessages():
    welcomeMessages = []
    try:
        with open('dserverconfig/WelcomeMessages.json') as f:
            welcomeMessages = json.load(f)
    except:
        print('Error opening welcome messages. File may not exist.')
        with open ('dserverconfig/WelcomeMessages.json', 'w+') as f:
            json.dump(welcomeMessages, f)
    return welcomeMessages