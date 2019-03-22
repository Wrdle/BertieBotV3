import json
from random import randint
from datetime import datetime

def newMessage(message):
    messages = []
    with open('dserverconfig/WelcomeMessages.json') as f:
        messages = json.load(f)

    newWelcomeMessageEntry = {
        "id" : messages[-1]['id'] + 1,
        "creationTime" : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "content" : message
    }

    with open('dserverconfig/WelcomeMessages.json', 'w') as f:
        messages.append(newWelcomeMessageEntry)
        json.dump(messages, f)

def removeMessage(messageid):
        messages = []   
        with open('dserverconfig/WelcomeMessages.json') as f:
            messages = json.load(f)

        for message in messages:
            if message['id'] == int(messageid):
                messages.remove(message)
        
        with open('dserverconfig/WelcomeMessages.json', 'w') as f:
            json.dump(messages, f)

def getAllWelcomeMessages():
    welcomeMessages = []
    try:
        with open('dserverconfig/WelcomeMessages.json') as f:
            welcomeMessages = json.load(f)
    except:
        print('Error opening welcome messages. File may not exist.')
        with open ('dserverconfig/WelcomeMessages.json', 'w+') as f:
            json.dump(welcomeMessages, f)
    return welcomeMessages

def getRandomMessage(member):
    welcomeMessages = getAllWelcomeMessages()
    if len(welcomeMessages) > 0:
        message = ""
        if len(welcomeMessages) == 1:
            message = welcomeMessages[0]['content']
        else:
            message = welcomeMessages[randint(0, len(welcomeMessages) - 1)]['content']
        
        if '{*USER*}' in message:
            message = message.replace('{*USER*}', member.mention)    
        return message
    
