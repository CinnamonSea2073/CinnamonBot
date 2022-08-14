import requests
from lib.yamlutil import yaml
import discord
from discord.ext import commands
from discord.ui import View
from discord import Option, OptionChoice, SlashCommandGroup
import cogs.point as point
import os
from dotenv import load_dotenv

load_dotenv()
talkAPIkey = os.getenv('talkAPIkey')

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

def setup(bot):
    bot.add_cog(TalkCog(bot))

