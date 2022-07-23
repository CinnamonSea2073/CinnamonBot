import yaml
import discord
from discord.ext import commands
from discord import Option, OptionChoice, SlashCommandGroup
from googletrans import Translator
import random
import copy
import os
import requests

class GamesCog(commands.Cog):

    def __init__(self, bot):
        print('げーむ初期化.')
        self.bot = bot

    def point(name):
        with open('./game.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            name = f"{name}s"
            data = data[name]
            return "".join(data)

    def getpoint(name,newpoint,bool):
        with open('./game.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            #Discordidにsをつける
            name = f"{name}s"
            #その人のリストを参照
            list = data[name]
            #突っ込む前のポイントを参照
            oldpoint = data[name]
            #リストを文字列にする
            oldpoint = "".join(oldpoint)
            newpoint = "".join(newpoint)
            print (oldpoint)
            #計算する（int）
            if bool == True:
                point = int(newpoint) + int(oldpoint)
            else:
                point = int(oldpoint) - int(newpoint)
            #python内で最初のデータに新しいポイントを突っ込む
            list[0] = str(point)
            print (list)
            #突っ込んだものをyamlに突っ込む準備
            data[name] = list
            print (data)
            f.seek(0)
            yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
            return "".join(data[name])


    #コマンドグループを定義っ！！！
    games = SlashCommandGroup('game', 'test')

    @games.command(name="check",description="ポイントを確認します")
    async def check(
        self,
        ctx: discord.ApplicationContext,
        ):
        print (ctx.author.id)
        await ctx.respond(f"現在のあなたのポイントは **{GamesCog.point(ctx.author.id)}** です！")

    @games.command(name="up",description="ポイントを増やします")
    async def up(
        self,
        ctx: discord.ApplicationContext,
        point: Option(str, required=True, description="追加する量を設定してください", )
        ):
        print (ctx.author.id)
        id = ctx.author.id
        await ctx.respond(f"現在のあなたのポイントは **{GamesCog.getpoint(id,point,True)}** です！")
    
    @games.command(name="down",description="ポイントを減らします")
    async def down(
        self,
        ctx: discord.ApplicationContext,
        point: Option(str, required=True, description="減らす量を設定してください", )
        ):
        print (ctx.author.id)
        id = ctx.author.id
        await ctx.respond(f"現在のあなたのポイントは **{GamesCog.getpoint(id,point,False)}** です！")

def setup(bot):
    bot.add_cog(GamesCog(bot))