import json
import sqlite3
import datetime
import os

import config_modules.botDB as botDB

def newMessage(message):
    message = 'INSERT INTO ChatLog VALUES ({}, {}, {}, "{}", {}, "{}", "{}");'.format(message.id, message.channel.id, message.author.id, message.content, int(message.tts), "Experimental", str(datetime.datetime.now().strftime("%d/%m/%y %I:%M%p")))
    with botDB.Database() as db:
        db.execute(message)

def getChannelLog(channel):
    query = 'SELECT * FROM ChatLog WHERE channelID = {}'.format(channel.id)
    channelLog = []
    with botDB.Database() as db:
        data = db.execute(query)
        for row in data:
            channelLog.append(cLogMessage(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    return channelLog

def getAllMessages():
    query = 'SELECT * FROM ChatLog'
    channelLog = []
    with botDB.Database() as db:
        data = db.execute(query)
        for row in data:
            channelLog.append(cLogMessage(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    return channelLog


class cLogMessage():
    def __init__(self, messageID, channelID, userID, content, tts, attachments, time):
        self.messageID = messageID
        self.channelID = channelID
        self.userID = userID
        self.content = content
        self.tts = tts
        self.attachments = attachments
        self.time = time