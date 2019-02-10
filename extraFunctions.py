import discord
import threading 

def getRole(server, id):
    for role in server.roles:
        if role.id == id:
            return role