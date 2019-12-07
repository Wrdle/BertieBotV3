import discord
import threading 

def getRole(guild, id):
    for role in guild.roles:
        if role.id == id:
            return role

def getAllTextChannels(guild):
    channels = []
    for channel in guild.channels:
        if channel.type.name == 'text':
            channels.append(channel)
    return channels

def getIDFromMention(mention):
    id = ''
    for char in mention:
        if char.isdigit():
            id += char
    return int(id)
