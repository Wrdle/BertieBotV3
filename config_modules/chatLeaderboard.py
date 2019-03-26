import json
import os

import extraFunctions

def loadLeaderboard():
    leaderboard = []
    if os.path.isfile('dserverconfig/ChatLeaderboard.json') != True:
        with open('dserverconfig/ChatLeaderboard.json', 'w') as f:
            json.dump(leaderboard, f)
    with open('dserverconfig/ChatLeaderboard.json') as f:
        leaderboard = json.load(f)
    return leaderboard

def getMemberXP(member):
    leaderboard = loadLeaderboard()
    for user in leaderboard:
        if user['memberID'] == member.id:
            return user['xp']
    return 0

def newMessage(member, message):
    if member.bot == False:
        if message.content[0].strip() != '.':
            leaderboard = loadLeaderboard()
            memberExists = False
            for  row in leaderboard:
                if row["memberID"] == member.id:
                    memberExists = True
                    row["xp"] = row["xp"] + 1
                    if member.name != row["name"]:
                        row["name"] = member.name
            if memberExists == False:
                newUser = {
                    "memberID" : member.id,
                    "name" : member.name,
                    "xp" : 1
                }
                leaderboard.append(newUser)
        
            with open('dserverconfig/ChatLeaderboard.json', 'w') as f:
                json.dump(leaderboard, f)

def loadAutoRanks():
    ranks = []
    if os.path.isfile('dserverconfig/AutoRanks.json') == True:
        with open('dserverconfig/AutoRanks.json') as f:
            ranks = json.load(f)
            ranks.sort(key= lambda x : int(x['xp']))
    else:
        with open('dserverconfig/AutoRanks.json', 'w') as f:
            json.dump(ranks, f)
    return ranks
    
async def autoRanks(member, server, client):
    ranks = loadAutoRanks()
    if len(ranks) > 0:
        memberXP = getMemberXP(member)

        for rank in ranks:
            if int(rank['xp']) < memberXP:
                role = extraFunctions.getRole(server, rank["id"])
                if role not in member.roles:
                    await client.add_roles(member, role)

def addNewAutoRank(newAutoRank, newAutoRankXP):
    newEntry = {
        "id" : newAutoRank,
        "xp" : newAutoRankXP
    }

    ranks = []

    with open('dserverconfig/AutoRanks.json') as f:
        ranks = json.load(f)

    rankExists = False
    for rank in ranks:
        if rank['id'] == newEntry['id']:
            rank['xp'] = newEntry['xp']
            rankExists = True

    if rankExists == False:
        ranks.append(newEntry)

    with open('dserverconfig/AutoRanks.json', 'w') as f:
        json.dump(ranks, f)

def removeAutoRank(id):
    autoRanks = loadAutoRanks()
    
    for rank in autoRanks:
        if rank['id'] == id:
            autoRanks.remove(rank)

    with open('dserverconfig/AutoRanks.json', 'w') as f:
        json.dump(autoRanks, f)



