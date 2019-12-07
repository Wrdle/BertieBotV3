import discord
import os, sys
from discord.ext import commands

import start
from settings import serverChatLog, chatLeaderboard, configFunctions, welcomeMessages, extraFunctions

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def xp(self, ctx):
        xp = chatLeaderboard.getMemberXP(ctx.message.author)
        await ctx.channel.send('You have ' + str(xp) + 'XP ' + ctx.message.author.mention)

    @commands.command(pass_context=True)
    async def leaderboard(self, ctx):
        leaderboard = chatLeaderboard.loadLeaderboard()
        leaderboard.sort(key = lambda x : x.xp, reverse=True)

        serverConfig = configFunctions.reloadServerConfig()
        
        em = discord.Embed(title='Chat Leaderboard', colour=0x00D3DE)
        em.description = "The top 5 people on the leaderboard are:\n"

        appinfo = await self.bot.application_info()
        em.set_author(name = appinfo.name, icon_url= appinfo.icon_url)
        iterations = 0
        for row in leaderboard:
            iterations += 1
            if iterations <= 5:
                user = await self.bot.fetch_user(row.userID)
                em.description += str(iterations) + ".   " + user.name + ": " + str(row.xp) + "XP\n"
        
        if serverConfig["externalDomain"] is not None:
            em.description += "Leaderboard available at: " + serverConfig['externalDomain'] + ":5000/leaderboard"
        await ctx.channel.send(embed=em)

    @commands.command(pass_context=True)   
    async def invitedBy(self, ctx, mention):
        if chatLeaderboard.doesInviteEntryExist(ctx.message.author) == True:
            await ctx.channel.send("Sorry but you have already claimed your invite.")
        else:
            inviter = ctx.message.guild.get_member(extraFunctions.getIDFromMention(mention))
            if inviter.bot is False and inviter != ctx.message.author:
                chatLeaderboard.addInviteEntry(ctx.message.author, inviter)
                chatLeaderboard.addMemberXP(inviter, 50)
                await chatLeaderboard.autoRank(inviter, ctx.guild, self.bot)
                await ctx.channel.send("Invite claimed :)")
            else:
                await ctx.channel.send("Sorry but you cannot claim that person as your inviter.")