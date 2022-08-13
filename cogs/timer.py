import asyncio
from threading import Timer
import discord
from discord.ext import commands
from discord import Option, OptionChoice, SlashCommandGroup

icon = "https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png"

timerget = 0

class TimerCog(commands.Cog):

    def __init__(self, bot):
        print('たいまっ初期化')
        self.bot = bot

    # コマンドグループを定義っ！！！
    timer = SlashCommandGroup('timer', 'test')

    @timer.command(name="set", description="タイマーを設定します。")
    async def timer_set(
        self,
        ctx: discord.ApplicationContext,
        seconds: Option(int, min_value=1, max_value=3600, default=60, description='秒数を設定してください。')
        ):
        global timerget
        try:
            await ctx.respond(f"{seconds}秒のタイマーを起動しました。")
            time = seconds
            for t in range(time):
                if time == 0:
                    break
                time -= 1
                timerget = time
                await asyncio.sleep(1)
                print(t)
                continue
            await ctx.respond(f"<@{ctx.author.id}>\n{seconds}秒のタイマーが終了しました。") 
        except:
            await ctx.respond("原因不明のエラーが発生しました。") 

    @timer.command(name="get", description="現在動いているタイマーを取得します。")
    async def timer_get(
        self,
        ctx: discord.ApplicationContext
        ):
        global timerget
        if timerget == 0:
            await ctx.respond(f"<@{ctx.author.id}>\n現在タイマーは稼働していません。") 
        else:
            await ctx.respond(f"<@{ctx.author.id}>\n現在{timerget}秒のタイマーが稼働しています。") 

def setup(bot):
    bot.add_cog(TimerCog(bot))