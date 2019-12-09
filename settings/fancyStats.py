from . import botDB

async def enableChannelStat(client, guild, statType):
    statTypes = getAllStatTypes()
    if statType in statTypes:
        with botDB.Database() as db:
            channel = await guild.create_voice_channel(name=statType, position=0, reason="Bertie Bot fancyStats")
            db.execute("UPDATE fancyStats SET enabled = 1, channelID = {0} WHERE statType = '{1}'".format(channel.id, statType))
    await updateFancyStats(client)

async def disableChannelStat(client, guild, statType):
    statTypes = getAllStatTypes()
    if statType in statTypes:
        fancyStat = getFancyStat(client, statType)
        await fancyStat.discordChannelObject.delete(reason="Bertie Bot FancyStat Disabled")
        with botDB.Database() as db:
            db.execute("UPDATE fancyStats SET enabled = 0, channelID=NULL WHERE statType = '{0}'".format(statType))

def moveToChannelGroup(client, guild):
    pass

async def updateFancyStats(client):
    channels = getAllChannels(client)
    for channel in channels:
        if channel.statType == "Member Count" and channel.enabled is True:
            await channel.discordChannelObject.edit(name=("Member Count: " + str(channel.discordChannelObject.guild.member_count)))
        elif channel.statType == "Channel Count" and channel.enabled is True:
            await channel.discordChannelObject.edit(name=("Channel Count: " + str(len(channel.discordChannelObject.guild.channels))))

def getAllChannels(client):
    channels = []
    with botDB.Database() as db:
        data = db.execute("SELECT * FROM fancyStats")
        for row in data:
            channels.append(fancyStatsChannel(row[0], bool(row[1]), row[2]))
    channels = attachDiscordChannelObjects(client, channels)
    return channels


def attachDiscordChannelObjects(client, fancyStatsChannelList):
    for channel in fancyStatsChannelList:
        if channel.channelID is not None:
            channel.discordChannelObject = client.get_channel(channel.channelID)
    return fancyStatsChannelList

def getFancyStat(client, statType):
    channels = getAllChannels(client)
    for channel in channels: 
        if channel.statType == statType:
            return channel
    return None

def getAllStatTypes():
    statTypes = []
    with botDB.Database() as db:
        data = db.execute("SELECT statType FROM fancyStats;")
        for row in data:
            statTypes.append(row[0])
    return statTypes


class fancyStatsChannel():
    def __init__(self, statType, enabled, channelID):
        self.statType = statType
        self.enabled = enabled
        self.channelID = channelID