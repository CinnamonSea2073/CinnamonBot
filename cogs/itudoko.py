import yaml
import discord
from discord.ext import commands
from discord import Option, OptionChoice, SlashCommandGroup
from googletrans import Translator
import random
import copy
import os

class ItudokoCog(commands.Cog):

    def __init__(self, bot):
        print('いつどこ初期化')
        self.bot = bot

    #ランダム抽出をここでやっちゃう作戦
    def word():
        with open('./itudoko.yaml', 'r',encoding="utf-8_sig") as f:
            data = yaml.unsafe_load(f)
            itu = random.choice(data['itu'])
            dokode = random.choice(data['dokode'])
            darega = random.choice(data['darega'])
            donoyouni = random.choice(data['donoyouni'])
            naniwosita = random.choice(data['naniwosita'])
            message = f"{itu}\n{dokode}\n{darega}\n{donoyouni}\n{naniwosita}"
        #randomwordが完成したランダム抽出
        return message

    itudoko_list = [
        OptionChoice(name='itu', value=1),
        OptionChoice(name='dokode', value=2),
        OptionChoice(name='darega', value=3),
        OptionChoice(name='naniwosita', value=4)
    ]

    def set(number,content):
        with open('./itudoko.yaml', 'r+',encoding="utf-8_sig") as f:
                data = yaml.safe_load(f)
                number = itudoko_list
                hogedata = data[""]
                hogedata.append(content)
                print (hogedata)
                data['itu'] = hogedata
                print (data)
                f.seek(0)
                yaml.dump(data, f,default_flow_style=False,allow_unicode=True)

    #コマンドグループを定義っ！！！
    itudoko = SlashCommandGroup('itudoko', 'test')

    #いつどこランダム排出
    @itudoko.command(name="get",description="いつどこで誰が何をしたかランダムで排出します")
    async def itudoko_get(
            self,
            ctx: discord.ApplicationContext,
            ):
        await ctx.respond(ItudokoCog.word())

    @itudoko.command(name="set",description="いつどこで誰が何をしたかに単語を追加します")
    async def itudoko_set(
            self,
            ctx: discord.ApplicationContext,
            number: Option(str, required=True, description="追加する項目を設定してください \n 1:いつ \n 2:どこで \n 3:だれが \n 4:どのように \n 5:何をした", ),
            content: Option(str, required=True, description="追加する単語を設定してください", ),
            ):
        if number == "1":
            with open('./itudoko.yaml', 'r+',encoding="utf-8_sig") as f:
                data = yaml.safe_load(f)
                hogedata = data['itu']
                hogedata.append(content)
                print (hogedata)
                data['itu'] = hogedata
                print (data)
                f.seek(0)
                yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
            await ctx.respond(f"「いつ」に{content}を追加しました。")
        else :
            await ctx.respond(f"{number}は無効です。")

def setup(bot):
    bot.add_cog(ItudokoCog(bot))