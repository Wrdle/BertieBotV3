from datetime import datetime
from . import repeatedTimer, botDB
import start as main

def updateMemberCount(client):
    with botDB.Database() as db:
        guild = client.get_guild(main.serverid)
        time = datetime.now().strftime("%d/%m/%Y")
        getTodaysDBRecord = db.execute('SELECT * FROM DailyMemberCountStats WHERE Date = "{0}";'.format(time)).fetchone()
        if getTodaysDBRecord != None:
            db.execute('UPDATE DailyMemberCountStats SET MemberCount = {0} WHERE Date = "{1}"'.format(len(guild.members), time))
        else:
            db.execute('INSERT INTO DailyMemberCountStats VALUES("{0}",{1})'.format(datetime.now().strftime("%d/%m/%Y"), len(guild.members)))



def startStatisticsDaemon(client):
    memberCountDaemon = repeatedTimer.RepeatedTimer(2, updateMemberCount, client)