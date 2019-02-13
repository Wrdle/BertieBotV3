import json

def getAuditLog():
    auditLog = None
    try:
        with open('dserverconfig/auditLog.json') as f:
            auditLog = json.load(f)
    except:
        print('Error opening Audit Log. File may not exist.')
        with open ('dserverconfig/auditLog.json', 'w+') as f:
            auditLog = []
            json.dump(auditLog, f)
    return auditLog

def saveAuditLog(auditLog):
    with open ('dserverconfig/auditLog.json', 'w') as f:
        json.dump(auditLog, f)

def newMemberJoin(user, time):
    auditLog = getAuditLog()
    newEntry = {
        "user": user.id,
        "time": time.strftime("%d/%m/%y %I:%M%p"),
        "action": "nmj",
        "comment": "User " + user.name + " joined the server"
    }

    auditLog.append(newEntry)
    saveAuditLog(auditLog)

def memberLeave(user, time):
    auditLog = getAuditLog()
    newEntry = {
        "user": user.id,
        "time": time.strftime("%d/%m/%y %I:%M%p"),
        "action": "ml",
        "comment": "User " + user.name + " left the server"
    }

    auditLog.append(newEntry)
    saveAuditLog(auditLog)

