import json
import os
import sqlite3

import config_modules.botDB as botDB

def loadLeaderboard():
    leaderboard = []
    with botDB.Database() as db:
        data = db.execute('SELECT * FROM ChatLeaderboard;')
        for row in data:
            leaderboard.append((leaderboardEntry(row[0], row[1])))
    return leaderboard

def getMemberXP(member):
    xp = sqlite3.connect('./botdatabase.db').cursor().execute('SELECT xp FROM ChatLeaderboard WHERE userID = {0}'.format(member.id)).fetchone()
    return xp[0]

def newMessage(member, message):
    if member.bot == False:
        if message.content != None:
            if message.content[0].strip() != '.':
                conn = sqlite3.connect('./botdatabase.db')
                sql = conn.cursor()

                if sql.execute('SELECT 1 FROM ChatLeaderboard WHERE userID = {0}'.format(member.id)).fetchone() != None:
                    sql.execute('UPDATE ChatLeaderboard SET xp = (SELECT xp FROM ChatLeaderboard WHERE userID = ?) + 1 WHERE userID = ?', (member.id, member.id))
                    conn.commit()
                else:
                    sql.execute('INSERT INTO ChatLeaderboard VALUES(?, ?)', (member.id, 1))
                    conn.commit()
                sql.close()

class leaderboardEntry():
    def __init__(self, userID, xp):
        self.userID = userID
        self.xp = xp



# ========================= AutoRanks =========================

def loadAutoRanks():
    ranks = []
    with botDB.Database() as db:
        data = db.execute('SELECT * FROM AutoRanks')
        for row in data:
            ranks.append(autoRankEntry(row[0], row[1]))
    ranks.sort(key= lambda x : int(x.xp))
    return ranks
    
async def autoRank(member, guild):
    ranks = loadAutoRanks()
    if len(ranks) > 0:
        memberXP = getMemberXP(member)

        for rank in ranks:
            if int(rank.xp) < memberXP:
                role = guild.get_role(rank.rankID)
                if role not in member.roles:
                    await member.add_roles(role)

def addNewAutoRank(newAutoRank, newAutoRankXP):
    query = 'INSERT INTO AutoRanks VALUES({},{})'.format(newAutoRank, newAutoRankXP)
    with botDB.Database() as db:
        db.execute(query)

def removeAutoRank(roleID):
    query = 'DELETE FROM AutoRanks WHERE roleID == {}'.format(roleID)
    with botDB.Database() as db:
        db.execute(query)


class autoRankEntry():
    def __init__(self, rankID, xp):
        self.rankID = rankID
        self.xp = xp



