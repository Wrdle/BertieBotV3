from discord.ext import commands
import sqlite3
import os, sys
from colorama import Fore, Back, Style

import start
from settings import serverChatLog, chatLeaderboard, configFunctions, welcomeMessages, extraFunctions

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def join(self, ctx):
        print(str(ctx))

    @commands.command()
    async def newWelcomeMessage(self, ctx):
        welcomeMessages.newMessage(ctx.message.content)

    @commands.command()
    async def getRandomWelcomeMessage(self, ctx):
        message = welcomeMessages.getRandomMessage(ctx.message.author)
        if (message == None):
            await ctx.message.channel.send("You have not set any welcome messages yet")
            return
        await ctx.message.channel.send(message)
        
    
    @commands.command(pass_context=True)
    async def allroles(self, ctx):
        message = "Roles: \n"
        for role in ctx.message.guild.roles:
            message += role.name + " : " + str(role.id) + "\n"
        await ctx.message.channel.send(message)

    @commands.command(pass_context=True)
    async def clear(self, ctx, amount=100):
        channel = ctx.message.channel
        messages = []
        async for message in self.bot.logs_from(channel, limit=int(amount) + 1):
            messages.append(message)
        await self.bot.delete_messages(messages)
        await message.channel.send('Messages deleted')

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.GREEN + 'Discord Bot Ready and Logged in!')
        print(Fore.GREEN + 'Logged in as: ', self.bot.user)
        print(Fore.GREEN + 'ID:', self.bot.user.id)
        print(Style.RESET_ALL)

        # Bot cannot have more than one discord sever
        if (len(self.bot.guilds) == 1):
            start.serverid = self.bot.guilds[0].id # Get ID of only server
        else:
            print("ERROR: You cannot have more than one server assigned to a bot.")
            exit()

        if os.path.isfile('./botdatabase.db') != True:
            conn = sqlite3.connect('botdatabase.db')
            sql = conn.cursor()

            sql.execute('CREATE TABLE ChatLog (messageID integer NOT NULL UNIQUE PRIMARY KEY, channelID integer NOT NULL, userID integer NOT NULL, content text, tts blob, attachments blob, time text NOT NULL);')
            sql.execute("CREATE TABLE ChatLeaderboard (userID integer NOT NULL UNIQUE PRIMARY KEY, xp integer NOT NULL);")
            sql.execute("CREATE TABLE WelcomeMessages (wMessageID integer NOT NULL UNIQUE PRIMARY KEY, creationTime text NOT NULL, content text NOT NULL);")
            sql.execute("CREATE TABLE AutoRanks (roleID integer NOT NULL UNIQUE PRIMARY KEY, xp integer NOT NULL);")

            conn.commit()
            sql.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        serverChatLog.newMessage(message)
        chatLeaderboard.newMessage(message.author, message)
        await chatLeaderboard.autoRank(message.author, message.guild, self.bot)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        serverConfig = configFunctions.reloadServerConfig()

        # NEED TO ADD A WAY FOR THE USER TO SELECT A CHANNEL IN WEBSITE GUI TO SEND MESSAGES TO   
        if serverConfig["greetingChannel"] != None:
            greetingChannel = self.bot.get_channel(serverConfig["greetingChannel"])
            welcomeMessage = welcomeMessages.getRandomMessage(member)
            if welcomeMessage != None:
                await greetingChannel.send(welcomeMessages.getRandomMessage(member))

        try:
            if serverConfig['defaultRole'] != None:
                await member.add_roles(member.guild.get_role(configFunctions.getAutoRole()))
        except:
            if member.dm_channel == None:
                await member.create_dm()
            await member.dm_channel.send("There was an error adding the default role to a newly joined server member. Please login to the web panel and ensure that the role you have chosen still exists")