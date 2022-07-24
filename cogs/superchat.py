import os
import discord
from discord.ext import commands
from discord import Option, SlashCommandGroup
import joblib
import requests


class UUID_NotFoundException(Exception):
    pass


def get_face(username):
    mojang = requests.get(
        f"https://api.mojang.com/users/profiles/minecraft/{username}").json()
    isvalid = mojang.get("id", None)
    if isvalid is None:
        raise UUID_NotFoundException(f"{username}のUUIDが見つからないよ")
    else:
        return f"https://crafatar.com/avatars/{mojang['id']}"



COLORDATA = {199: 0x3233ff, 499: 0x32ccfd, 999: 0x00ff99,
            1999: 0x00ff99, 4999: 0xfe9900, 9999: 0xfe9900, 50000: 0xfd0001}


def getColor(money: int):
    for v in COLORDATA:
        if money <= v:
            return COLORDATA[v]

FILENAME = 'uuidlist.txt'


class SuperChatCog(commands.Cog):


    def __init__(self, bot):
        print('superchat init')
        self.bot = bot
        if os.path.exists(FILENAME):
            self.users = joblib.load(FILENAME)
        else:
            self.users = dict()


    superchat = SlashCommandGroup('superchat', 'superchat')

    @superchat.command(name='give', description='スーパーチャットを送ります')
    async def give(
        self,
        ctx: discord.ApplicationContext,
        money: Option(int, description='送る金額を決めます 100 - 50,000', min_value=100, max_value=50000, default=500),
        message: Option(str, description='メッセージの内容を決定します', default=''),
    ):
        embed = discord.Embed(
            title="¥ {:,}".format(money),
            color=getColor(money=money),
            description=message,
        )
        embed.set_author(name=ctx.author.name, icon_url=self.users.get(ctx.author.id))
        await ctx.respond(embed=embed)

    @superchat.command(name='set', description='ユーザーの顔アイコンを登録するよ')
    async def set(
        self,
        ctx: discord.ApplicationContext,
        mc_name: Option(str, description='マイクラでの自分のユーザー名を登録してね'),
    ):
        try:
            self.users[ctx.author.id] = get_face(mc_name)
            joblib.dump(self.users, FILENAME, 3)
        except UUID_NotFoundException as e:
            await ctx.respond(e)
        await ctx.respond(f'{mc_name}の顔を登録したよ')


def setup(bot):
    bot.add_cog(SuperChatCog(bot))