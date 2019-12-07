import json
import os
import sqlite3

from . import extraFunctions, botDB, configFunctions

def loadLeaderboard():
    leaderboard = []
    with botDB.Database() as db:
        data = db.execute('SELECT * FROM ChatLeaderboard;')
        for row in data:
            leaderboard.append((leaderboardEntry(row[0], row[1])))
    return leaderboard

def getMemberXP(member):
    xp = sqlite3.connect('./botdatabase.db').cursor().execute('SELECT xp FROM ChatLeaderboard WHERE userID = {0}'.format(member.id)).fetchone()
    if xp is None:
        return 0
    return xp[0]

def addMemberXP(member, xp):
    with botDB.Database() as db:
        memberXP = getMemberXP(member)
        if memberXP > 0:
            db.execute('UPDATE ChatLeaderboard SET xp = (SELECT xp FROM ChatLeaderboard WHERE userID = {0}) + {1} WHERE userID = {2}'.format(member.id, xp, member.id))
        else:
            db.execute('INSERT INTO ChatLeaderboard VALUES({0}, {1});'.format(member.id, xp))

def newMessage(member, message):
    serverConfig = configFunctions.reloadServerConfig()
    if member.bot == False:
        if message.content != None:
            if message.content != '' and message.content[0].strip() != serverConfig["commandPrefix"]:
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

# ========================= Invitiations =========================

def addInviteEntry(invitee, inviter):
    with botDB.Database() as db:
        db.execute('INSERT INTO Invitations VALUES ({0}, {1});'.format(invitee.id, inviter.id))
    
def doesInviteEntryExist(invitee):
    with botDB.Database() as db:
        data = db.execute('SELECT * FROM Invitations WHERE inviteeMemberID == {0};'.format(invitee.id)).fetchone()
        if data is None:
            return False
        return True

def getMemberInvites(member):
    with botDB.Database() as db:
        data = db.execute('SELECT COUNT(inviterMemberID) FROM Invitations WHERE inviterMemberID == {0};'.format(member.id)).fetchone()
        if data is None:
            return 0
        return int(data[0])


# ========================= AutoRanks =========================

def loadAutoRanks():
    ranks = []
    with botDB.Database() as db:
        data = db.execute('SELECT * FROM AutoRanks')
        for row in data:
            ranks.append(autoRankEntry(row[0], row[1], row[2]))
    ranks.sort(key= lambda x : int(x.xp))
    return ranks
    
async def autoRank(member, server, client):
    ranks = loadAutoRanks()
    if len(ranks) > 0:
        memberXP = getMemberXP(member)
        memberInvites = getMemberInvites(member)

        for rank in ranks:
            if rank.xp <= memberXP and rank.invites <= memberInvites:
                role = extraFunctions.getRole(server, rank.rankID)
                if role not in member.roles:
                    await member.add_roles(role, reason = "Auto Rank")

def addNewAutoRank(newAutoRank, newAutoRankXP, newAutoRankInvites):
    query = 'INSERT INTO AutoRanks VALUES({},{},{})'.format(newAutoRank, newAutoRankXP, newAutoRankInvites)
    with botDB.Database() as db:
        db.execute(query)

def removeAutoRank(roleID):
    query = 'DELETE FROM AutoRanks WHERE roleID == {}'.format(roleID)
    with botDB.Database() as db:
        db.execute(query)


class autoRankEntry():
    def __init__(self, rankID, xp, invites):
        self.rankID = rankID
        self.xp = xp
        self.invites = invites



