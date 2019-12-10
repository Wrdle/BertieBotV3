from discord.ext import commands

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context=True)
    async def updateStats(self, ctx):
        await fancyStats.updateFancyStats(self.bot, ctx.guild)

    @commands.command(pass_context=True)
    async def enableChannelStat(self, ctx, statType):
        await fancyStats.enableChannelStat(self.bot, ctx.guild, statType)

    @commands.command(pass_context=True)
    async def disableChannelStat(self, ctx, statType):
        await fancyStats.disableChannelStat(self.bot, ctx.guild, statType)