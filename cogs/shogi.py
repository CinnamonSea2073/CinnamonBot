from lib.yamlutil import yaml
import discord
from discord.ext import commands
from discord.ui import View
from discord import Option, OptionChoice, SlashCommandGroup
import random
import cogs.point as point
import asyncio

from typing import List

minhayaYaml = yaml('minhaya.yaml')
minhaya = minhayaYaml.load_yaml()
minhaya_genreYaml = yaml('minhaya_genre.yaml')
minhaya_genre = minhaya_genreYaml.load_yaml()

genre_list = [
    OptionChoice(name='いろいろ', value='all'),
    #OptionChoice(name='ITパスポート', value='IT'),
]

def get_question():
    return random.choice(minhaya)

def add(genre,content,ans1,ans2,ans3,ans4,a):
        global minhaya
        #genreがallだったら、適当なprintしてifを飛ばす
        if genre == "all":
            print("tomatomatomato")
        if genre == "IT":
            minhaya = minhaya_genre["it"]
            #このprint見る限りではminhayaがちゃんとit用に上書きされてる
            print(f"hogehogehogehogehogehoge{minhaya}\nhogehogehogehoge{minhaya[1]}")
            minhayaYaml = minhaya_genreYaml
        for num in range(100):
            try:
                hoge = minhaya[num]
                print(hoge)
                continue
            except KeyError:
                #genreがitの時、多分minhaya["it"][num] = {"exam"...ってなってるはず
                minhaya[num] = {"exam": content, "ans": [ans1,ans2,ans3,ans4], "a": a}
                #genreがitの時、多分minhaya_genreYamlになってるはず
                minhayaYaml.save_yaml(minhaya)
                #このsaveの結果、minhaya_gen.yamlで一番最初の「it」が消えて普通の奴と同じように「0」とかから始まってしまう
                return str(minhaya[num]["exam"])

class helpselectView(View):
    @discord.ui.select(
            placeholder="出題するジャンルを指定してね",
            options=[
                discord.SelectOption(
                    label="All",
                    emoji="💥",
                    description="登録されてる全ての問題から出題！",
                    #default=True
                    ),
                discord.SelectOption(
                    label="雑学とか",
                    emoji="💬",
                    description="いろんな知識を習得して雑学王になろう！",
                    #default=True
                    ),
                discord.SelectOption(
                    label="ITパスポート",
                    emoji="💻",
                    description="みんなもこれでITパスポートに合格してドヤろう！※PCでの参加を推奨します",
                    #default=True
                    )
        ])
    async def select_callback(self, select:discord.ui.Select, interaction):
        embed = discord.Embed(title=f"みんはや：{select.values[0]}",color=0x1e90ff)
        await interaction.response.edit_message(embed=embed, view=None)
        if select.values[0] == "ITパスポート":
            for n in range(10):
                print("IT")
                select.disabled = True
                hoge = random.choice(minhaya_genre['it'])
                await interaction.followup.send(content=hoge['exam'], view=TicTacToe_row(hoge))
        elif select.values[0] == "雑学とか":
            for n in range(10):
                print("雑学")
                select.disabled = True
                hoge = random.choice(minhaya)
                await interaction.followup.send(content=hoge['exam'], view=TicTacToe_row(hoge))
        elif select.values[0] == "All":
            for n in range(10):
                print("All")
                select.disabled = True
                hogehoge = random.choice([0,1])
                if hogehoge == 0:
                    hoge = random.choice(minhaya)
                elif hogehoge == 1:
                    hoge = random.choice(minhaya_genre['it'])
                await interaction.followup.send(content=hoge['exam'], view=TicTacToe_row(hoge))

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

class TicTacToe_RowButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, label: str):
        super().__init__(style=discord.ButtonStyle.secondary, label=label)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view

        self.style = discord.ButtonStyle.danger
        content = f'{self.view.exam}\nはずれ'
        if self.label == self.view.a:
            self.style = discord.ButtonStyle.success
            content = f'{self.view.exam}\n<@{interaction.user.id}> 正解！ **30,000円** を追加します。'
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

class TicTacToe_row(discord.ui.View):
    children: List[TicTacToeButton]

    def __init__(self, data):
        super().__init__(timeout=190)
        self.a = data["a"]
        self.exam = data["exam"]
        hoge = data.get('ans')
        random.shuffle(hoge)
        for v in hoge:
            self.add_item(TicTacToe_RowButton(v))


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

    @nb.command(name='get', description='【競技用推奨】登録されている問題からランダムで排出します')
    async def button(self, ctx: discord.ApplicationContext):
        # レスポンスで定義したボタンを返す
        hoge = get_question()
        await TicTacToeCog.countdown(ctx=ctx, n=3, message="{}秒後に問題が出ます")
        await ctx.interaction.edit_original_message(content=hoge['exam'], view=TicTacToe(hoge))

    @nb.command(name='genre_get', description='【カウントダウン等が無いため、競技非推奨】ジャンルを指定してから問題を10問ほどランダムで排出します')
    async def button_genre(self, ctx: discord.ApplicationContext):
        view = helpselectView()
        await ctx.respond("出題するジャンルを指定してね\n**PCを推奨します**",view=view)
    
    @nb.command(name="add", description="ジャンルを指定して問題を追加します")
    async def ans_add(
        self,
        ctx: discord.ApplicationContext,
        genre: Option(str, choices=genre_list, required=True, description="ジャンルを指定してね", ),
        content: Option(str, required=True, description="問題の文章です", ),
        ans1: Option(str, required=True, description="【間違いを入力】問題の選択肢1", ),
        ans2: Option(str, required=True, description="【間違いを入力】問題の選択肢2", ),
        ans3: Option(str, required=True, description="【間違いを入力】問題の選択肢3", ),
        a: Option(str, required=True, description="【答えを入力】問題の答え", )
    ):
        await ctx.respond(f"ジャンル：**{genre}**\n問題に **{add(genre,content,ans1,ans2,ans3,a,a)}** を追加しました")
        point.GamesCog.getpoint(ctx.author.id,ctx.author.name,10000)
        await ctx.send(f"<@{ctx.author.id}> 10,000円が追加されました！問題追加ありがとう！！")
        #print([content,ans1,a])

def setup(bot):
    bot.add_cog(TicTacToeCog(bot))