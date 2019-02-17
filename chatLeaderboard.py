import json

def loadLeaderboard():
    leaderboard = []
    with open('dserverconfig/ChatLeaderboard.json') as f:
        leaderboard = json.load(f)
    return leaderboard

def newMessage(member):
    leaderboard = loadLeaderboard()
    memberExists = False
    memberXP = None
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


