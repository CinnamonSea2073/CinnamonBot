import os
import discord
from discord.ext import commands
from discord import Option, SlashCommandGroup
from ..lib import face
import joblib

FILENAME = 'uuidlist.txt'

COLORDATA = {199: 0x3233ff, 499: 0x32ccfd, 999: 0x00ff99,
             1999: 0x00ff99, 4999: 0xfe9900, 9999: 0xfe9900, 50000: 0xfd0001}


def getColor(money: int):
    for v in COLORDATA:
        if money < v:
            return COLORDATA[v]


class SuperChatCog(commands.Cog):

    def __init__(self, bot):
        print('すぱちゃ初期化')
        self.bot = bot
        if os.path.exists(FILENAME):
            self.users = joblib.load(FILENAME)
        else:
            self.users = dict()

    superchat = SlashCommandGroup('superchat')

    @superchat.command(name='give', description='スーパーチャットを送ります')
    async def give(
        self,
        money: Option(int, description='送る金額を決めます 100 - 50,000', min_value=100, max_value=50000, default=500, required=False),
        message: Option(str, description='メッセージの内容を決定します', default=''),
        ctx: discord.ApplicationContext
    ):
        embed = discord.Embed(
            title=ctx.author.name,
            color=getColor(money=money),
            description=message,
        )
        embed.set_author(icon_url=self.users[ctx.author.id])
        await ctx.respond(embed)

    @superchat.command(name='set', description='ユーザーの顔アイコンを登録するよ')
    async def set(
        self,
        mc_name: Option(str, description='マイクラでの自分のユーザー名を登録してね'),
        ctx: discord.ApplicationContext
    ):
        try:
            self.users[ctx.author.id] = face.get_face(mc_name)
            joblib.dump(self.users, FILENAME, 3)
        except face.UUID_NotFoundException as e:
            await ctx.respond(e)
        await ctx.respond(f'{mc_name}の顔を登録したよ')


def setup(bot):
    bot.add_cog(SuperChatCog(bot))