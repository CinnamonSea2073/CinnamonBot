from telnetlib import GA
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
import numpy

np = numpy
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
            users[id] = {"name":name, "point":100, "top":0}
            with open('./game.yaml', 'w',encoding="utf-8_sig") as f:
                yaml.dump(users, f,default_flow_style=False,allow_unicode=True)
        return users[id]["point"] 

    def getpoint(id,name,point):
        global users
        if id in users:
            point += users[id]["point"]
            top = users[id]["top"]
        else:
            point += 100
            top = 0
        users[id] = {"name":name, "point":point, "top":top}

        with open('./game.yaml', 'w',encoding="utf-8_sig") as f:
            yaml.dump(users, f,default_flow_style=False,allow_unicode=True)
        return str(users[id]["point"])

    def genshinliset(id,name,top):
        global users
        print(top)
        if id not in users:
            users[id] = {"name":name, "point":100, "top":top}
        else:
            users[id] = {"name":name, "point":users[id]["point"], "top":top}
        with open('./game.yaml', 'w',encoding="utf-8_sig") as f:
            yaml.dump(users, f,default_flow_style=False,allow_unicode=True)
        return 

    def genshinget(id,name):
        global users
        top = 1
        if id in users:
            top += users[id]["top"]
            point = users[id]["point"]
        else:
            top += 0
            point = 100
        users[id] = {"name":name, "point":point, "top":top}

        with open('./game.yaml', 'w',encoding="utf-8_sig") as f:
            yaml.dump(users, f,default_flow_style=False,allow_unicode=True)
        return int(top)

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

    @games.command(name="genshinwish",description="原神ガチャシミュレーター")
    async def genshinwish(
        self,
        ctx: discord.ApplicationContext,
        ):
        id = ctx.author.id
        name = ctx.author.name
        resalt = GamesCog.genshinget(id,name)
        if resalt < 9:
            p = False
            s = False
        elif resalt == 9:
            p = True
            s = False
        elif resalt < 18:
            p = False
            s = True
        elif resalt == 18:
            p = True
            s = True
        
        #randomresalt = []
        if s == False and p == False:
            randomresalt = np.random.choice(["3","4","5","6"], size=9, p=[0.943,0.051,0.003,0.003])
            randomresalt = randomresalt.tolist()
            randomresalt.append("4")
            await ctx.respond(randomresalt)
            if "4" in any(randomresalt):
                print("hoge")
                GamesCog.genshinliset(id,name,9) 
            elif "6" == any(randomresalt):
                GamesCog.genshinliset(id,name,0)      
        elif s == False and p == True:
            randomresalt = np.random.choice(["3","4","5","6"], size=9, p=[0.943,0.051,0.003,0.003])
            randomresalt = randomresalt.tolist()
            srinuke = np.random.choice(["5","6"], size=1, p=[0.5,0.5])
            srinuke = srinuke.tolist()
            randomresalt.append("".join(srinuke))
            if "5" == any(randomresalt):
                GamesCog.genshinliset(id,name,9) 
            elif "6" == any(randomresalt):
                GamesCog.genshinliset(id,name,0)   
        if s == True and p == False:
            randomresalt = np.random.choice(["3","4","6"], size=9, p=[0.943,0.051,0.006])
            randomresalt = randomresalt.tolist()
            randomresalt.append("4")
            if "6" == any(randomresalt):
                GamesCog.genshinliset(id,name,0)      
        elif s == True and p == True:
            randomresalt = np.random.choice(["3","4","5","6"], size=9, p=[0.943,0.051,0.003,0.003])
            randomresalt = randomresalt.tolist()
            randomresalt.append("6")
            if "5" == any(randomresalt):
                GamesCog.genshinliset(id,name,0) 
            elif "6" == any(randomresalt):
                GamesCog.genshinliset(id,name,0) 

        await ctx.respond(randomresalt)    

def setup(bot):
    bot.add_cog(GamesCog(bot))