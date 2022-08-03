from lib.yamlutil import yaml
import discord
from discord.ext import commands
from discord import Option, OptionChoice, SlashCommandGroup
import random
import urllib
import asyncio

from typing import List

minhayaYaml = yaml('minhaya.yaml')
minhaya = minhayaYaml.load_yaml()

cinnamonBazz = {
    "exam": "しなもんさんのツイートの最大いいね数は？",
    "ans": ['7000', '10000', '25000', '50000']
}

def get_question():
    global minhaya
    #指定したランダムな数字で問題番号の内容を叩く
    number = random.randint(0,1)
    exam = str("".join(minhaya[number]["exam"]))
    ans = minhaya[number]["ans"]
    a = str(minhaya[number]["a"])
    resalt = {
        "exam": exam,
        "ans": ans}
    return resalt,a,ans



class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, label: str):
        super().__init__(style=discord.ButtonStyle.secondary, label=label)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view

        self.style = discord.ButtonStyle.success
        resalt = get_question()
        content = 'はずれ'
        if self.label == resalt[1]:
            content = 'せいかい'
            for child in self.view.children:
                child.disabled = True

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]

    def __init__(self):
        super().__init__(timeout=190)
        
        resalt = get_question()
        hoge = resalt[0]
        for v in hoge.get('ans'):
            self.add_item(TicTacToeButton(v))


class TicTacToeCog(commands.Cog):

    def __init__(self, bot):
        print('test')
        self.bot = bot

    nb = SlashCommandGroup('hayaoshi', 'test')

    @nb.command(name='test', description='button')
    async def button(self, ctx):
        # レスポンスで定義したボタンを返す
        hoge = get_question()
        hoge = hoge[1]
        await ctx.respond(hoge['exam'], view=TicTacToe())


def setup(bot):
    bot.add_cog(TicTacToeCog(bot))