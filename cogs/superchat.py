import os
import discord
from discord.ext import commands
from discord import Option, SlashCommandGroup
import joblib
import requests
import yaml
import cogs.point as point

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


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


COLORDATA = {199: 0x1e88e5, 499: 0x00e5ff, 999: 0x1de9b6,
             1999: 0xffca28, 4999: 0xf57c00, 9999: 0xe91e63, 50000: 0xe62117}


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
        send: Option(str, description='メンションで対象のメンバーを指定できます（デフォルトはしなもん）', default='698127042977333248'),
        money: Option(int, description='送る金額を決めます 100 - 50,000', min_value=100, max_value=50000, default=500),
        message: Option(str, description='メッセージの内容を決定します', default=''),
    ):
        embed = discord.Embed(
            title="¥ {:,}".format(money),
            color=getColor(money=money),
            description=message,
        )
        id = ctx.author.id
        if self.users.get(id) == None:
            await ctx.respond(f"<@{id}> /superchat set で登録してください。")
        elif point.GamesCog.point(id, ctx.author.name) < money:
            await ctx.respond(f"<@{id}> お金が足りません。/money up で増やしてください。\nあなたの所持金は**{point.GamesCog.point(id,ctx.author.name)}￥**です。")
        else:
            point.GamesCog.getpoint(id, ctx.author.name, -money)
            if send != None:
                point.GamesCog.getpoint(int(send.strip('<!@>')), None, money)
            embed.set_author(name=ctx.author.name, icon_url=self.users.get(id))
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
