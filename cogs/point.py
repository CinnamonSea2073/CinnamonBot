import yaml
import discord
from discord.ext import commands
from discord import Option, OptionChoice, SlashCommandGroup
from googletrans import Translator
import random
import copy
import os
import requests

users = dict()
with open('./game.yaml', 'r', encoding="utf-8_sig") as f:
        tmp = yaml.safe_load(f)
        if tmp != None:
            users = tmp

class GamesCog(commands.Cog):

    def __init__(self, bot):
        print('げーむ初期化.')
        self.bot = bot

    def point(id, name):
        global users
        if id not in users:
            users[id] = {"name":name, "point":100}
            with open('./game.yaml', 'w',encoding="utf-8_sig") as f:
                yaml.dump(users, f,default_flow_style=False,allow_unicode=True)
        return users[id]["point"] 

    def getpoint(id,name,point):
        global users
        if id in users:
            point += users[id]["point"]
        else:
            point += 100
        users[id] = {"name":name, "point":point}

        with open('./game.yaml', 'w',encoding="utf-8_sig") as f:
            yaml.dump(users, f,default_flow_style=False,allow_unicode=True)
        return str(users[id]["point"])


    #コマンドグループを定義っ！！！
    games = SlashCommandGroup('game', 'test')

    @games.command(name="check",description="ポイントを確認します")
    async def check(
        self,
        ctx: discord.ApplicationContext,
        ):
        print (ctx.author.id)
        await ctx.respond(f"現在のあなたのポイントは **{GamesCog.point(ctx.author.id, ctx.author.name)}** です！")

    @games.command(name="up",description="ポイントを増やします")
    async def up(
        self,
        ctx: discord.ApplicationContext,
        point: Option(int, required=True, description="追加する量を設定してください", )
        ):
        print (ctx.author.id)
        id = ctx.author.id
        name = ctx.author.name
        await ctx.respond(f"現在のあなたのポイントは **{GamesCog.getpoint(id,name,point)}** です！")
    
    @games.command(name="down",description="ポイントを減らします")
    async def down(
        self,
        ctx: discord.ApplicationContext,
        point: Option(int, required=True, description="減らす量を設定してください", )
        ):
        print (ctx.author.id)
        id = ctx.author.id
        name = ctx.author.name
        await ctx.respond(f"現在のあなたのポイントは **{GamesCog.getpoint(id,name,-point)}** です！")

def setup(bot):
    bot.add_cog(GamesCog(bot))