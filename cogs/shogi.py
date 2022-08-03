from lib.yamlutil import yaml
import discord
from discord.ext import commands
from discord import Option, OptionChoice, SlashCommandGroup
import random
import cogs.point as point
import asyncio

from typing import List

minhayaYaml = yaml('minhaya.yaml')
minhaya = minhayaYaml.load_yaml()

def get_question():
    return random.choice(minhaya)


class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, label: str):
        super().__init__(style=discord.ButtonStyle.secondary, label=label)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view

        self.style = discord.ButtonStyle.danger
        content = 'はずれ'
        if self.label == self.view.a:
            self.style = discord.ButtonStyle.success
            content = f'<@{interaction.user.id}> 正解！ **10,000円** を追加します。'
            point.GamesCog.getpoint(interaction.user.id,interaction.user.name,10000)
            print(interaction.user.id)
            for child in self.view.children:
                child.disabled = True

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]

    def __init__(self, data):
        super().__init__(timeout=190)
        self.a = data["a"]
        for v in data.get('ans'):
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
        await ctx.respond("3秒後に問題が出ます")
        asyncio.sleep(2)
        await ctx.send("2秒後に問題が出ます")
        asyncio.sleep(2)
        await ctx.send("1秒後に問題が出ます")
        asyncio.sleep(2)
        await ctx.respond(hoge['exam'], view=TicTacToe(hoge))


def setup(bot):
    bot.add_cog(TicTacToeCog(bot))