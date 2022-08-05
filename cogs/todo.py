from lib.yamlutil import yaml
import discord
from discord.ext import commands
from discord import Option, SlashCommandGroup
import cogs.point as point
import datetime

todoYaml = yaml('todo.yaml')

class todoCog(commands.Cog):

    def __init__(self, bot):
        print('とど初期化.')
        self.bot = bot
        self.todo: list[dict[str:str]] = todoYaml.load_yaml([])

    icon = "https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png"

    def embeded(title, description, url):
        embed = discord.Embed(title=title, color=0x1e90ff,
                              description=description)
        embed.set_image(url=url)
        embed.set_footer(text="made by CinnamonSea2073",
                         icon_url=todoCog.icon)
        return embed

    def todoadd(self, name, content):
        dt_now = datetime.datetime.now()
        self.todo.append({"name": name, "content": content, "time": dt_now.strftime('%m月%d日 %H:%M')})
        todoYaml.save_yaml(self.todo)

    def todoremove(self, number):
        self.todo.pop(number)
        todoYaml.save_yaml(self.todo)
        #todoCog.todoliset()

    todo = SlashCommandGroup('todo', 'superchat')

    @todo.command(name='set', description='todoに追加します')
    async def set(
        self,
        ctx: discord.ApplicationContext,
        content: Option(str, required=True, description='todoの内容')
    ):
        print(content)
        self.todoadd(ctx.author.name,content)
        await ctx.respond(f'todo番号 **{len(self.todo)}** に「**{content}**」を追加しました。\ntodoリストを再度表示するには、/todo checkを実行してください。')
        embed = discord.Embed(title=f"TODO (10秒後削除されます)", color=0x1e90ff,)
        for i, data in enumerate(self.todo):
            name = data["name"]
            content = data["content"]
            time = data["time"]
            embed.add_field(
                name=f"{i+1}", value=f"{content}\n=====\nBy **{name}**\n{time} 追加")
        embed.set_footer(text="made by CinnamonSea2073", icon_url=todoCog.icon)
        await ctx.respond(embed=embed,delete_after=10)
        channel = self.bot.get_partial_messageable(1005110196361760871)
        await channel.send(embed=embed)

    @todo.command(name='check', description='todoを確認します。')
    async def check(
        self,
        ctx: discord.ApplicationContext,
    ):
        embed = discord.Embed(title=f"TODO (30秒後削除されます)", color=0x1e90ff,)
        for i, data in enumerate(self.todo):
            name = data["name"]
            content = data["content"]
            time = data["time"]
            embed.add_field(
                name=f"{i+1}", value=f"{content}\n=====\nBy **{name}**\n{time} 追加")
        embed.set_footer(text="made by CinnamonSea2073", icon_url=todoCog.icon)
        await ctx.respond(embed=embed,delete_after=30)
        channel = self.bot.get_partial_messageable(1005110196361760871)
        await channel.send(embed=embed)

    @todo.command(name='remove', description='todoを達成して削除します。')
    async def remove(
        self,
        ctx: discord.ApplicationContext,
        number: Option(int, required=True, description='todoの番号')
    ):
        try:
            self.todoremove(number-1)
            await ctx.respond(f"**{number}** を完了しました🎉\ntodoリストを再度表示するには、/todo checkを実行してください。")
            point.GamesCog.getpoint(ctx.author.id,ctx.author.name,10000)
            await ctx.send(f"<@{ctx.author.id}> 10,000円が追加されました！お疲れ様でした。")
        except IndexError:
            await ctx.respond("このリストの数字で指定しやがれください")
        embed = discord.Embed(title=f"TODO (10秒後削除されます)", color=0x1e90ff,)
        for i, data in enumerate(self.todo):
            name = data["name"]
            content = data["content"]
            time = data["time"]
            embed.add_field(
                name=f"{i+1}", value=f"{content}\n=====\nBy **{name}**\n{time} 追加")
        embed.set_footer(text="made by CinnamonSea2073", icon_url=todoCog.icon)
        await ctx.respond(embed=embed,delete_after=10)
        channel = self.bot.get_partial_messageable(1005110196361760871)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(todoCog(bot))
