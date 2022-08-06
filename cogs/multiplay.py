from dis import disco
from select import select
import discord
from discord.ui import Select,View
from discord.ext import commands
from discord.commands import SlashCommandGroup
from lib.yamlutil import yaml

memberYaml = yaml("matchmake.yaml")
member =memberYaml.load_yaml()
gameroom_1 = 1005284543521112094
gameroom_2 = 1005284570985418853

class roomselectView(View):

    hoge = ">,<@".join(member[0]["member"])
 
    @discord.ui.select(
            placeholder="入りたい部屋を選択してね",
            options=[
                discord.SelectOption(
                    label="room_1",
                    emoji="📰",
                    description=f"今入っている人：{hoge}",
                    )
        ])
    
    async def select_callback(self, select:discord.ui.Select, interaction):
        if select.values[0] == "room_1":
            print("main")
            select.disabled = True
            channel = discord.Bot.get_partial_messageable(gameroom_1)
            if matchmade.selectfalse == False:
                try:
                    #もう満員になったら、強制的に開始する。
                    if len(member[0]["member"]) == 3:
                        hoge = member[0]["member"]
                        member[0] = {"member": hoge.append(interaction.user.id)}
                        memberYaml.save_yaml(member)
                        await channel.send(content=f"<@{interaction.user.id}> が入室しました。")
                        matchmade.making_after(interaction,interaction.user.id,2)
                        await interaction.response.edit_message(content="#ゲーム部屋1 に移動してください。",view=self)
                    #もしメンバーが3人or2人だったら、ゲームを開始するか提案する。
                    elif len(member[0]["member"]) <= 2:
                        hoge = member[0]["member"]
                        member[0] = {"member": hoge.append(interaction.user.id)}
                        memberYaml.save_yaml(member)
                        await channel.send(content=f"<@{interaction.user.id}> が入室しました。")
                        await interaction.response.edit_message(content="#ゲーム部屋1 に移動してください。",view=self)
                #メンバーが誰もいなかったら、待つ
                except KeyError:
                    hoge = member[0]["member"]
                    member[0] = {"member": hoge.append(interaction.user.id)}
                    memberYaml.save_yaml(member)
                    await channel.send(content=f"<@{interaction.user.id}> が入室しました。")
                    await interaction.response.edit_message(content="#ゲーム部屋1 に移動してください。",view=self)
            elif matchmade.selectfalse == True:
                await interaction.response.edit_message(content="この部屋はもうゲームを開始してる！",view=self)

class matchmade():

    selectfalse = False

    async def making_after(self,interaction,id,room_number):
        matchmade.selectfalse = True
        print(f"成功！{interaction}{id}{room_number}")
    

class matchCog(commands.Cog):

    def __init__(self, bot):
        print('マルチ_initしたよ')
        self.bot = bot

    help = SlashCommandGroup('multiplay', 'test')

    @help.command(name='matchmaking', description='マッチメイキングシステムテスト')
    async def chelp(self, ctx):
        view = roomselectView()
        await ctx.respond("入りたい部屋を選択してね",view=view)  # レスポンスで定義したボタンを返す

def setup(bot):
    bot.add_cog(matchCog(bot))