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

def add(content,ans1,ans2,ans3,ans4,a):
        global minhaya
        for num in range(100):
            try:
                hoge = minhaya[num]
                print(hoge)
                continue
            except KeyError:
                minhaya[num] = {"exam": content, "ans": [ans1,ans2,ans3,ans4], "a": a}
                minhayaYaml.save_yaml(minhaya)
                return str(minhaya[num]["exam"])

class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, label: str):
        super().__init__(style=discord.ButtonStyle.secondary, label=label)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view

        self.style = discord.ButtonStyle.danger
        content = f'{self.view.exam}\nはずれ'
        if self.label == self.view.a:
            self.style = discord.ButtonStyle.success
            content = f'{self.view.exam}\n<@{interaction.user.id}> 正解！ **10,000円** を追加します。'
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
        self.exam = data["exam"]
        hoge = data.get('ans')
        random.shuffle(hoge)
        for v in hoge:
            self.add_item(TicTacToeButton(v))


class TicTacToeCog(commands.Cog):

    def __init__(self, bot):
        print('みんはやinit')
        self.bot = bot
    
    nb = SlashCommandGroup('hayaoshi', 'test')

    async def countdown(ctx: discord.ApplicationContext, n: int, message="{}"):
        await ctx.respond(message.format(str(n)))
        await asyncio.sleep(1)
        n -= 1
        for i in range(n):
            await ctx.interaction.edit_original_message(content=message.format(str(n-i)))
            await asyncio.sleep(1)

    @nb.command(name='問題をランダムで排出します', description='button')
    async def button(self, ctx: discord.ApplicationContext):
        # レスポンスで定義したボタンを返す
        hoge = get_question()
        await TicTacToeCog.countdown(ctx=ctx, n=3, message="{}秒後に問題が出ます")
        await ctx.interaction.edit_original_message(content=hoge['exam'], view=TicTacToe(hoge))
    
    @nb.command(name="add", description="問題を追加します")
    async def ans_add(
        self,
        ctx: discord.ApplicationContext,
        content: Option(str, required=True, description="問題の文章です", ),
        ans1: Option(str, required=True, description="問題の選択肢1", ),
        ans2: Option(str, required=True, description="問題の選択肢2", ),
        ans3: Option(str, required=True, description="問題の選択肢3", ),
        ans4: Option(str, required=True, description="問題の選択肢4", ),
        a: Option(str, required=True, description="問題の答え", )
    ):
        await ctx.respond(f"問題に **{add(content,ans1,ans2,ans3,ans4,a)}** を追加しました")
        point.GamesCog.getpoint(ctx.author.id,ctx.author.name,10000)
        await ctx.send(f"<@{ctx.author.id}> 10,000円が追加されました！問題追加ありがとう！！")
        #print([content,ans1,a])

def setup(bot):
    bot.add_cog(TicTacToeCog(bot))