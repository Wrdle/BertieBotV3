from discord.ext import commands

import start
from settings import fancyStats, serverChatLog, chatLeaderboard, configFunctions, welcomeMessages, extraFunctions

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @commands.command(pass_context=True)
    async def updateStats(self, ctx):
        await fancyStats.updateFancyStats(self.bot, ctx.guild)

    @commands.command(pass_context=True)
    async def enableChannelStat(self, ctx, statType):
        await fancyStats.enableChannelStat(self.bot, ctx.guild, statType)

    @commands.command(pass_context=True)
    async def disableChannelStat(self, ctx, statType):
        await fancyStats.disableChannelStat(self.bot, ctx.guild, statType)
