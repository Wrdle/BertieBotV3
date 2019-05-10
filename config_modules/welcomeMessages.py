import json
from random import randint
from datetime import datetime

import config_modules.botDB as botDB

# Adds new Welcome Message to the database 
def newMessage(message):
    query = 'INSERT INTO WelcomeMessages(creationTime, content) VALUES("{}", "{}");'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), message)
    with botDB.Database() as db:
        db.execute(query)

# Removes message with corrosponding ID from database
def removeMessage(messageid):
    query = 'DELETE FROM WelcomeMessages WHERE wMessageID = {};'.format(messageid)
    with botDB.Database() as db:
        db.execute(query)

# Returns a list of all Welcome Messages
def getAllWelcomeMessages():
    welcomeMessages = []
    with botDB.Database() as db:
        data = db.execute("SELECT * FROM WelcomeMessages")

        # Puts data into welcomeMessage objects and adds them to a list
        for row in data:
            welcomeMessages.append(welcomeMessage(row[0], row[1], row[2]))

    return welcomeMessages

# Returns specifically one random welcome message and only its content
def getRandomMessage(member):
    welcomeMessages = getAllWelcomeMessages()
    if len(welcomeMessages) > 0:
        message = welcomeMessages[randint(0, len(welcomeMessages) - 1)].content
        if '{*USER*}' in message:
            message = message.replace('{*USER*}', member.mention)    
        return message

class welcomeMessage():
    def __init__(self, wMessageID, creationTime, content):
        self.wMessageID = wMessageID
        self.creationTime = creationTime
        self.content = content
    
