import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord import Option, OptionChoice
from lib.chouen import getChouen
from lib.yamlutil import yaml
import random

nbYaml = yaml("nb.yaml")


class NbCog(commands.Cog):

    def __init__(self, bot):
        print('NBさんの初期化')
        self.bot = bot
        self.nb_messages: list[str] = nbYaml.load_yaml([])

    nb = SlashCommandGroup('nb', 'ここの説明文の使い方わからん')

    flag = [
        OptionChoice(name="ON", value=1)
    ]

    @nb.command(name='home', description='褒められたときに名前を入れて使いましょう')
    async def nb_home(
        self,
        ctx: discord.ApplicationContext,
        name: Option(str, default='NB', required=False, description='ない場合はNBさんになります'),
        homenai: Option(str, default='褒められる', required=False, description='もし、褒めないられない場合はここで変更'),
        nanika: Option(str, default='自信', required=False,
                       description='もし、自信以外の場合はここで変更'),
        gaming: Option(int, default=0, choices=flag, required=False,
                       description='Gamingタイプにできます')
    ):

        top = f'{name}さんに{homenai}と'
        bottom = f'{nanika}になります！'

        await ctx.respond(getChouen(top=top, bottom=bottom, rainbow=[False, True][gaming]))

    values = [
        OptionChoice(name='悲報', value='【悲報wwwwwwwwww】'),
        OptionChoice(name='朗報', value='【朗報wwwwwwwwww】'),
        OptionChoice(name='良報', value='【良報WWwwwWwWwWww】'),
        OptionChoice(name='速報', value='【速報wwwwwwwwwww】')
    ]

    @nb.command(name='youtube', description='NB構文Y型')
    async def get_nb2(
        self,
        ctx: discord.ApplicationContext,
        any_hou: Option(str, default=values[0].value, choices=values, required=False, description='何報ですか？'),
        honbun: Option(str, default='ワイ氏パチスロにいって', required=False,
                       description='本文を入力しよう→{本文}しまうwwwwwwwwww'),
        gaming: Option(int, default=0, choices=flag, required=False,
                       description='Gamingタイプにできます')
    ):
        bottom = f'{honbun}しまうwwwwwwwwww'
        await ctx.respond(getChouen(top=any_hou, bottom=bottom, rainbow=[False, True][gaming]))

    @nb.command(name='meigen', description='NBさんの明言を出力します')
    async def alive(
        self,
        ctx: discord.ApplicationContext,
    ):
        param: str = [None, None]
        for i, s in enumerate(random.choice(self.nb_messages).split('\n')):
            param[i] = s
        await ctx.respond(getChouen(top=param[0], bottom=param[1], rainbow=True))


def setup(bot):
    bot.add_cog(NbCog(bot))
