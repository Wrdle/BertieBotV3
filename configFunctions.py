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

    if url.strip() != "":
        serverConfig['externalURL'] = url
    else:
        serverConfig['externalURL'] = None

    with open('dserverconfig/ServerConfig.json', 'w') as f:
        json.dump(serverConfig, f)