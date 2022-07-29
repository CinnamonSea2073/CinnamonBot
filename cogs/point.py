import yaml
import discord
from discord.ext import commands
from discord import Option, OptionChoice, SlashCommandGroup
from googletrans import Translator
import random
import copy
import os
import requests
import urllib
import json

users = dict()
words = dict()
with open('./game.yaml', 'r', encoding="utf-8_sig") as f:
        tmp = yaml.safe_load(f)
        if tmp != None:
            users = tmp

with open('./genshin.yaml', 'r', encoding="utf-8_sig") as e:
        etmp = yaml.safe_load(e)
        if etmp != None:
            words = etmp
        
with open('./genshinH.yaml', 'r', encoding="utf-8_sig") as b:
        btmp = yaml.safe_load(b)
        if btmp != None:
            jhwords = btmp

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

    def genshingen(name):
        global words
        global jhwords
        if name in words:
            resalt = urllib.parse.quote(words[name]["zh"])
        elif name in jhwords:
            resalt = urllib.parse.quote(words[jhwords[name]["ja"]]["zh"])
        else:
            resalt = None
        return f"https://bbs.hoyolab.com/hoyowiki/picture/character/{resalt}/avatar.png"

    icon = "https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png"

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

    @games.command(name="genshin",description="ガチャシミュレーター実装前テストコマンド")
    async def genshin(
        self,
        ctx: discord.ApplicationContext,
        content: Option(str, required=True, description="キャラ名（ひらかなでもおｋ）", )
        ):
        picture = GamesCog.genshingen(content)
        if picture == "https://bbs.hoyolab.com/hoyowiki/picture/character/None/avatar.png":
            content = f" \"{content}\" は原神データベースに存在しません。"
        embed = discord.Embed(title=content,color=0x1e90ff,)
        embed.set_image(url=picture)
        embed.set_footer(text="made by CinnamonSea2073",icon_url=GamesCog.icon)
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(GamesCog(bot))