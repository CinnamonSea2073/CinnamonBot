import discord
from discord.ext import commands
from discord import Option, SlashCommandGroup

class TestCog(commands.Cog):

    def __init__(self, bot):
        print('test初期化.')
        self.bot = bot

    test = SlashCommandGroup('test', 'test')

    @test.command(name="ping", description="pingするで")
    async def ping(self, ctx: discord.ApplicationContext,):
        await ctx.respond("pong!")

def setup(bot):
    bot.add_cog(TestCog(bot))