import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup


# ボタンクラス
class Button(discord.ui.View):

    def __init__(self):
        super().__init__()

    @discord.ui.button(
        # ボタンの初期値を決める
        label="0",  # ボタンの値
        style=discord.ButtonStyle.red  # ボタンの色
    )
    async def no(
        self,
        button: discord.ui.Button,  # ボタンのオブジェクト（これをかきかえたりする
        interaction: discord.Interaction  # ctxみたいなもん（ボタンが押されたときの反応を返す
    ):
        # ボタンのラベルは基本的に文字列型
        number = int(button.label) if button.label else 0
        if number >= 4:
            button.style = discord.ButtonStyle.green
            button.disabled = True  # True でボタンがもう押せない状態になる
        button.label = str(number + 1)

        # Make sure to update the message with our updated selves
        await interaction.response.edit_message(view=self)


class ButtonTestCog(commands.Cog):

    def __init__(self, bot):
        print('test')
        self.bot = bot

    nb = SlashCommandGroup('button', 'test')

    @nb.command(name='test', description='button')
    async def button(self, ctx):
        await ctx.respond(view=Button())  # レスポンスで定義したボタンを返す


def setup(bot):
    bot.add_cog(ButtonTestCog(bot))
