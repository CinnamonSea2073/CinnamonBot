import yaml
import discord
from discord.ext import commands
from discord import Option, OptionChoice, SlashCommandGroup
from googletrans import Translator
import random
import copy
import os
import requests

class OthersCog(commands.Cog):

    def __init__(self, bot):
        print('そのた初期化')
        self.bot = bot

    #コマンドグループを定義っ！！！
    others = SlashCommandGroup('etc', 'test')

    @others.command(name="hello",description="あなたの名前か入力した名前に挨拶します")
    async def hello(
        self,
        ctx: discord.ApplicationContext,
        name: Option(str, required=False, description="名前を入力してね", )
        ):
        if not name:
            name = ctx.author
        await ctx.respond(f"こんにちは！ {name} さん！")

    @others.command(name="mention",description="しなもんにメンションを爆撃します")
    async def mention(
        self,
        ctx: discord.ApplicationContext,
        contents: Option(str, required=False, description="しなもんに爆撃したい内容を書いてね", )
        ):
        await ctx.respond(f"<@698127042977333248> {contents} ")

    @others.command(name="face",description="MCIDから顔面を生成っ！")
    async def face(
        self,
        ctx: discord.ApplicationContext,
        mcid: Option(str, required=True, description="マイクラIDをかいてね", )
        ):
        if not mcid:
            mcid = ctx.author
        mojang = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{mcid}").json()
        isvalid = mojang.get("id",None)
        if isvalid is None:
            await ctx.respond("プレイヤー'{}'は存在しません。".format(mcid))
        else:
            crafatar = requests.get(f"https://crafatar.com/avatars/{mojang['id']}", stream=True)
            with open(f"{mcid}.png", "wb") as f:
                f.write(crafatar.content)
            file = discord.File(f"{mcid}.png", filename=f"{mcid}.png")
            embed = discord.Embed(title=f"{mcid} のお顔")
            embed.set_image(url=f"attachment://{mcid}.png")
            await ctx.respond(file=file,embed=embed)
            os.remove(f"{mcid}.png")

    @others.command(name="seichi",description="整地から逃げるな(ほぼ自分用)")
    async def seichi(
        self,
        ctx: discord.ApplicationContext,
        contents: Option(str, required=False, description="しなもんに整地させたい内容を書いてね", )
        ):
        if not contents:
            contents = "整地から逃げるな"
        embed = discord.Embed( # Embedを定義する
                          title="整地から逃げるな",# タイトル
                          color=0x1e90ff, # フレーム色指定(今回は緑)
                          description="整地から逃げるな<@698127042977333248>", # Embedの説明文 必要に応じて
                          
                          )

        embed.add_field(name="JMS投票しよう（日課）",value="https://minecraft.jp/servers/54d3529e4ddda180780041a7")
        embed.add_field(name="monocraft投票しよう（日課）",value="https://monocraft.net/servers/Cf3BffNIRMERDNbAfWQm/vote")
        embed.add_field(name="サイト",value="https://www.seichi.network/gigantic")

        embed.set_footer(text="made by CinnamonSea2073", # フッターには開発者の情報でも入れてみる
                     icon_url="https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png")

        await ctx.respond(f"<@698127042977333248> {contents} ")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(OthersCog(bot))