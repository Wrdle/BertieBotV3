import json
import datetime
import os 

def newMessage(message):
    newMessageDictionary = {
        "id": message.id,
        "time": str(datetime.datetime.now().strftime("%d/%m/%y %I:%M%p")),
        "channel": message.channel.id,
        "user": message.author.id,
        "content": message.content,
        "tts": str(message.tts),
        "attachments": str(message.attachments)
    }
    with open(os.path.abspath(os.curdir) + '/dserverconfig/ServerChatLog.json') as f:
        data = json.load(f)
    data.append(newMessageDictionary)

    with open(os.path.abspath(os.curdir) + '/dserverconfig/ServerChatLog.json', 'w') as f:
        json.dump(data, f)

def getChannelLog(channel):
    with open(os.path.abspath(os.curdir) + '/dserverconfig/ServerChatLog.json') as f:
        data = json.load(f)

    channelLog = []
    for message in reversed(data):
        if message["channel"] == channel.id:
            channelLog.append(message)
    return channelLog