import yaml
import discord
from discord.ext import commands
from discord import Option, OptionChoice, SlashCommandGroup
from lib.yamlutil import yaml
import aiohttp

server_Yaml = yaml('serverURL.yaml')
server_Yaml = server_Yaml.load_yaml()
server_urltmp = "".join(server_Yaml["url"])
server_url = f"https://api.mcsrvstat.us/2/{server_urltmp}"
icon = "https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png"
dynmap_url = f"http://{server_urltmp}/mc/"

class StatCog(commands.Cog):

    def __init__(self, bot):
        print('Stat初期化')
        self.bot = bot

    # コマンドグループを定義っ！！！
    stat = SlashCommandGroup('stat', 'test')

    @stat.command(name="get", description="ふぃぼ鯖の状態を表示します")
    async def stat_get(self,ctx: discord.ApplicationContext):
        await ctx.respond("読み込み中...(5秒程度かかります)") 
        async with aiohttp.ClientSession() as session:
            async with session.get(server_url) as response:
                resp = await response.json()
        try:
            if resp["online"] == True:
                embed = discord.Embed( 
                                    title="Server Stat",
                                    color=0x1e90ff, 
                                    description="サーバーはオンラインです。\n(５分程度の遅延がある場合があります)", 
                                    url=server_url 
                                    )
                embed.add_field(inline=False,name="アドレス",value=resp['hostname'])
                embed.add_field(inline=False,name="バージョン",value=resp['version'])
                online = str(resp["online"])
                try:
                    if resp['players']['online'] == 0:
                        players = "現在プレイヤーは誰もいません。"
                    else:
                        players = "\n".join(resp['players']['list'])
                except:
                    players = "なんらかの理由により現在のプレイヤーを取得できませんでした。"
                if "True" in online:
                    embed.add_field(inline=False,name="ソフトウェア",value=resp['software'])
                    embed.add_field(inline=False,name="現在の接続中のプレイヤー",value=f"**{resp['players']['online']}/{resp['players']['max']}**\n{players}")
                embed.set_footer(text="made by CinnamonSea2073", icon_url=icon)
                await ctx.send(embed=embed) 
            else:
                await ctx.send("なんか現在オフラインっぽいで")
        except:
            await ctx.send(f"エラーが発生しました。APIを確認してからもう一度お試しください。\n{server_url}") 
                
    @stat.command(name="set", description="ふぃぼ鯖のurlを設定します。")
    async def stat_set(
        self,
        ctx: discord.ApplicationContext,
        url: Option(str, required=True, description="urlを設定してください", ),
    ):
        before_url = server_Yaml["url"]
        server_Yaml["url"] = url
        server_Yaml.save_yaml(server_Yaml)
        await ctx.respond(f"鯖のurlを{before_url}から{url}に変更しました。")

    @stat.command(name="dynmap", description="ふぃぼ鯖のdynmapを取得します。")
    async def stat_dynmap(self,ctx: discord.ApplicationContext):
        url = "http://nikawarasbian.ddns.net/mc/"
        await ctx.respond(url)

def setup(bot):
    bot.add_cog(StatCog(bot))