import discord
from discord.ext import commands
from discord import Option, SlashCommandGroup
from lib.faceutil import get_face, UUID_NotFoundException
from lib.chouen import getChouen
from discord_buttons_plugin import *

buttons = "hoge"


class OthersCog(commands.Cog):

    def __init__(self, bot):
        print('そのた初期化.')
        self.bot = bot
        global buttons
        buttons = ButtonsClient(bot)

    # コマンドグループを定義っ！！！
    others = SlashCommandGroup('etc', 'test')

    @others.command(name="hello", description="あなたの名前か入力した名前に挨拶します")
    async def hello(
        self,
        ctx: discord.ApplicationContext,
        name: Option(str, required=False, description="名前を入力してね", )
    ):
        if not name:
            name = ctx.author
        await ctx.respond(f"こんにちは！ {name} さん！")

    @others.command(name="mention", description="しなもんにメンションを爆撃します")
    async def mention(
        self,
        ctx: discord.ApplicationContext,
        contents: Option(str, required=False,
                         description="しなもんに爆撃したい内容を書いてね", )
    ):
        await ctx.respond(f"<@698127042977333248> {contents} ")

    @others.command(name="face", description="MCIDから顔面を生成っ！")
    async def face(
        self,
        ctx: discord.ApplicationContext,
        mcid: Option(str, required=True, description="マイクラIDをかいてね", )
    ):
        try:
            embed = discord.Embed(title=f"{mcid} のお顔")
            embed.set_image(url=await get_face(username=mcid))
            await ctx.respond(embed=embed)
        except UUID_NotFoundException as e:
            await ctx.respond(e)

    @others.command(name="seichi", description="整地から逃げるな(ほぼ自分用)")
    async def seichi(
        self,
        ctx: discord.ApplicationContext,
        contents: Option(str, required=False,
                         description="しなもんに整地させたい内容を書いてね", )
    ):
        if not contents:
            contents = "整地から逃げるな"
        embed = discord.Embed(  # Embedを定義する
            title="整地から逃げるな",  # タイトル
            color=0x1e90ff,  # フレーム色指定(今回は緑)
            description="整地から逃げるな<@698127042977333248>",  # Embedの説明文 必要に応じて

        )

        embed.add_field(
            name="JMS投票しよう（日課）", value="https://minecraft.jp/servers/54d3529e4ddda180780041a7")
        embed.add_field(name="monocraft投票しよう（日課）",
                        value="https://monocraft.net/servers/Cf3BffNIRMERDNbAfWQm/vote")
        embed.add_field(
            name="サイト", value="https://www.seichi.network/gigantic")

        embed.set_footer(text="made by CinnamonSea2073",  # フッターには開発者の情報でも入れてみる
                         icon_url="https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png")

        await ctx.respond(f"<@698127042977333248> {contents} ")
        await ctx.respond(embed=embed)

    @others.command(name="code", description="コードをみやすくするよ")
    async def code(
        self,
        ctx: discord.ApplicationContext,
        code: Option(str, required=True, description="コード種類（pyなど）を書いてね", ),
        contents: Option(str, required=True, description="コードを書いてね", )
    ):
        contents = contents.replace("\\n", "\n")
        await ctx.respond(f"```{code}\n{contents}``` ")

    @others.command(name="github", description="このボットのコードだよ")
    async def github(
        self,
        ctx: discord.ApplicationContext,
    ):
        embed = discord.Embed(  # Embedを定義する
            title="Github - CinnamonBot",  # タイトル
            color=0x1e90ff,  # フレーム色指定(今回は緑)
            description="https://github.com/CinnamonSea2073/CinnamonBot",  # Embedの説明文 必要に応じて
        )

        embed.set_footer(text="made by CinnamonSea2073",  # フッターには開発者の情報でも入れてみる
                         icon_url="https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png")

        await ctx.respond(embed=embed)

    @others.command(name="reference", description="pycodeのリファレンスだよ")
    async def reference(
        self,
        ctx: discord.ApplicationContext,
    ):
        embed = discord.Embed(  # Embedを定義する
            title="Pycode - reference",  # タイトル
            color=0x1e90ff,  # フレーム色指定(今回は緑)
            description="https://docs.pycord.dev/en/master/api.html",  # Embedの説明文 必要に応じて
        )

        embed.set_footer(text="made by CinnamonSea2073",  # フッターには開発者の情報でも入れてみる
                         icon_url="https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png")
        await ctx.respond(embed=embed)

    @others.command(name="5000oku", description="5000億円欲しい！")
    async def oku(
        self,
        ctx: discord.ApplicationContext,
        up: Option(str, required=True, description="上文字列", ),
        down: Option(str, required=True, description="下文字列", )
    ):
        await ctx.respond(getChouen(top=up, bottom=down))

    @others.command(name="test", description="tessssssssssst")
    async def test(
        self,
        ctx: discord.ApplicationContext,
    ):
        await buttons.send(
            content="テストボタン",
            channel=ctx.channel.id,
            components=[
                ActionRow([
                    Button(
                        label="Hello",
                        style=ButtonType().Primary,
                        custom_id="button_hello"
                    )
                ]), ActionRow([
                    Button(
                        label="Ephemeral",
                        style=ButtonType().Danger,
                        custom_id="button_ephemeral"
                    )
                ])
            ]
        )


def setup(bot):
    bot.add_cog(OthersCog(bot))
