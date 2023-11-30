import requests
from lib.yamlutil import yaml
import discord
from discord.ext import commands
from discord.ui import View
from discord import Option, OptionChoice, SlashCommandGroup
import cogs.point as point
import os
from dotenv import load_dotenv
from janome.tokenizer import Tokenizer

load_dotenv()
talkAPIkey = os.getenv('talkAPIkey')
t = Tokenizer()
icon = "https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png"

def talk_api(message):
    apikey = talkAPIkey
    talk_url = "https://api.a3rt.recruit.co.jp/talk/v1/smalltalk"    #4
    print(message)
    payload = {"apikey": apikey, "query": message}    #5
    response = requests.post(talk_url, data=payload)
    print(response.json()["status"])
    try:
        hoge = response.json()
        return hoge["results"][0]["reply"]    #6
    except:
        return f"えらーだよ\nhttpエラー：{response.json()['status']}"

class TalkCog(commands.Cog):

    def __init__(self, bot):
        print('Talkの初期化')
        self.bot = bot

    talk = SlashCommandGroup('talk', 'nanikore')

    @talk.command(name='get', description='AIと話せます。政治発言や差別用語、下ネタなど変なことは言わないようにお願いします。')
    async def nb_home(
        self,
        ctx: discord.ApplicationContext,
        message: Option(str, required=True, description='政治発言や差別用語、下ネタなど変なことは言わないようにお願いします。'),
    ):
        await ctx.respond(f"あなた：{message}\nBOT：**{talk_api(message)}**")

    @talk.command(name='test', description='機械学習のテスト')
    async def nb_home(
        self,
        ctx: discord.ApplicationContext,
        message: Option(str, required=True, description='文章を分析させます。'),
    ):
        hoge = []
        for token in t.tokenize(message):
            print(token)
            hoge.append(str(token))
        hogehoge = "\n".join(hoge)
        embed = discord.Embed(title=f"Tokenizeによる機械学習結果", color=0x1e90ff,)
        embed.add_field(
                name=f"入力した文字\n**{message}**", value=hogehoge)
        embed.set_footer(text="made by CinnamonSea2073", icon_url=icon)
        await ctx.respond(embed=embed)
        

def setup(bot):
    bot.add_cog(TalkCog(bot))

