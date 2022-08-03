from lib.yamlutil import yaml
import discord
from discord.ext import commands
from discord import Embed, Option, OptionChoice, SlashCommandGroup
from discord_buttons_plugin import *

buttons = "hoge"



todoYaml = yaml('todo.yaml')

todo = todoYaml.load_yaml()

class todoCog(commands.Cog):
    
    def __init__(self, bot):
        print('とど初期化.')
        self.bot = bot
        global buttons
        buttons = ButtonsClient(bot)

    icon = "https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png"

    def embeded(title, description, url):
        embed = discord.Embed(title=title, color=0x1e90ff,
                              description=description)
        embed.set_image(url=url)
        embed.set_footer(text="made by CinnamonSea2073",
                         icon_url=todoCog.icon)
        return embed

    def todo(number):
        global todo
        if number not in todo:
            return
        return todo[number]

    def todoadd(number,name,content):
        global todo
        #if number in todo:
            #return
        todo[number] = {"name": name, "content": content}
        todoYaml.save_yaml(todo)
        return str(todo[number]["content"])

    def todoremove(number):
        global todo
        if number not in todo:
            return
        todo[number] = {"name": None, "content": None}
        todoYaml.save_yaml(todo)
        return number

    todo = SlashCommandGroup('todo', 'superchat')

    @todo.command(name='set', description='todoに追加します')
    async def set(
        self,
        ctx: discord.ApplicationContext,
        number: Option(int, required=True, description='todoの番号'),
        content: Option(str, required=True, description='todoの内容')
    ):
        content = todoCog.todoadd(number,ctx.author.name,content)
        if content == None:
            await ctx.respond("その番号はすでに追加されていますが、上書きしますか？")
            await buttons.send(
                content = None, 
                channel = ctx.channel.id,
                components = [
                    ActionRow([
                        Button(
                            label="Yes", 
                            style=ButtonType().Danger, 
                            custom_id="button_Yes"
                        )
                    ]),ActionRow([
                        Button(
                            label="No",
                            style=ButtonType().Primary,
                            custom_id="button_No"
                        )
                    ])
                ]
            )
        else:
            await ctx.respond(f'todo番号 **{number}** に「**{content}**」を追加しました。')

    @todo.command(name='check', description='todoを確認します。')
    async def check(
        self,
        ctx: discord.ApplicationContext,
    ):
        embed = discord.Embed(title=f"TODO", color=0x1e90ff,)
        for number, value in todo.items():
            try:
                name = value["name"]
                content = value["content"]
                if name == None:
                    continue
                embed.add_field(
                        name=f"{number}", value=f"{content}\nBy **{name}**")
            except KeyError:
                continue
        embed.set_footer(text="made by CinnamonSea2073",icon_url=todoCog.icon)
        await ctx.respond(embed=embed)

    @todo.command(name='remove', description='todoを削除します。')
    async def remove(
        self,
        ctx: discord.ApplicationContext,
        number: Option(int, required=True, description='todoの番号')
    ):
        remove = todoCog.todoremove(number)
        if remove == None:
            await ctx.respond("その番号は存在しません")
        else:
            await ctx.respond(f"**{remove}** を削除しました。")

def setup(bot):
    bot.add_cog(todoCog(bot))