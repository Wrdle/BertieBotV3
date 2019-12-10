from . import botDB

async def enableChannelStat(client, guild, statType):
    print("running")
    statTypes = getAllStatTypes()
    if statType in statTypes:
        with botDB.Database() as db:
            channel = await guild.create_voice_channel(name=statType, position=0, reason="Bertie Bot fancyStats")
            db.execute("UPDATE fancyStats SET enabled = 1, channelID = {0} WHERE statType = '{1}'".format(channel.id, statType))
    await updateFancyStats(client, guild)

async def disableChannelStat(client, guild, statType):
    statTypes = getAllStatTypes()
    if statType in statTypes:
        fancyStat = getFancyStat(client, guild, statType)
        await fancyStat.discordChannelObject.delete(reason="Bertie Bot FancyStat Disabled")
        with botDB.Database() as db:
            db.execute("UPDATE fancyStats SET enabled = 0, channelID=NULL WHERE statType = '{0}'".format(statType))

def moveToChannelGroup(client, guild):
    pass

async def updateFancyStats(client, guild):
    channels = await getAllChannels(client, guild)
    for channel in channels:

        # Member Count
        if channel.statType == "Member Count" and channel.enabled is True:
            await channel.discordChannelObject.edit(name=("Member Count: " + str(channel.discordChannelObject.guild.member_count)))

        # Channel Count
        elif channel.statType == "Channel Count" and channel.enabled is True:
            await channel.discordChannelObject.edit(name=("Channel Count: " + str(len(channel.discordChannelObject.guild.channels))))

        # Role Count
        elif channel.statType == "Role Count" and channel.enabled is True:
            await channel.discordChannelObject.edit(name=("Role Count: " + str(len(channel.discordChannelObject.guild.roles))))

        # Bot Count
        elif channel.statType == "Bot Count" and channel.enabled is True:
            members = channel.discordChannelObject.guild.members # Get all members
            bots = 0

            # Get only bots
            for member in members:
                if member.bot is True:
                    bots += 1

            await channel.discordChannelObject.edit(name=("Bot Count: " + str(bots)))

        # User Count    
        elif channel.statType == "User Count" and channel.enabled is True:
            members = channel.discordChannelObject.guild.members # Get all members
            users = 0
            
            # Get only users excluding bots
            for member in members:
                if member.bot is False:
                    users += 1
            await channel.discordChannelObject.edit(name=("User Count: " + str(users)))

        # Admin Count
        elif channel.statType == "Admin Count" and channel.enabled is True:
            members = channel.discordChannelObject.guild.members # Get all members
            admins = 0
            
            # Get only online and DND members
            for member in members:
                if member.guild_permissions.administrator:
                    admins += 1
            await channel.discordChannelObject.edit(name=("Admin Count: " + str(admins)))

        # Online Count
        elif channel.statType == "Online Count" and channel.enabled is True:
            members = channel.discordChannelObject.guild.members # Get all members
            users = 0
            
            # Get only online and DND members
            for member in members:
                if member.status.name is "online" or member.status.name is "do_not_disturb":
                    users += 1
            await channel.discordChannelObject.edit(name=("Online Count: " + str(users)))
        
        # Offline Count
        elif channel.statType == "Offline Count" and channel.enabled is True:
            members = channel.discordChannelObject.guild.members # Get all members
            users = 0
            
            # Get only online and DND members
            for member in members:
                if member.status.name is "offline" or member.status.name is "invisible":
                    users += 1
            await channel.discordChannelObject.edit(name=("Offline Count: " + str(users)))


async def getAllChannels(client, guild):
    channels = []
    with botDB.Database() as db:
        data = db.execute("SELECT * FROM fancyStats")
        for row in data:
            channels.append(fancyStatsChannel(row[0], bool(row[1]), row[2]))
    channels = await attachDiscordChannelObjects(client, guild, channels)
    return channels


async def attachDiscordChannelObjects(client, guild, fancyStatsChannelList):
    for channel in fancyStatsChannelList:
        if channel.channelID is not None:
            channel.discordChannelObject = client.get_channel(channel.channelID)
            # Create new channel if bot could not find old one
            if channel.discordChannelObject == None:
                newChannel = await guild.create_voice_channel(name=channel.statType, position=0, reason="Bertie Bot fancyStats")
                updateFancyStatChannelID(channel.statType, newChannel.id)
                channel.discordChannelObject = newChannel

    return fancyStatsChannelList

def getFancyStat(client, guild, statType):
    channels = getAllChannels(client, guild)
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

def updateFancyStatChannelID(statType, newChannelID):
    with botDB.Database() as db:
        db.execute('UPDATE fancyStats SET channelID = {0} WHERE statType = "{1}"'.format(newChannelID, statType))


class fancyStatsChannel():
    def __init__(self, statType, enabled, channelID):
        self.statType = statType
        self.enabled = enabled
        self.channelID = channelID