import discord
from discord.ext import commands
import asyncio
from discord.commands import SlashCommandGroup
import json
import cogs.point as point
import random

horses: list = json.load(open("data/uma.json", "r", encoding="utf-8"))
odds = [2, 4, 7, 15, 24, 30]

class Select_Horse_Menu_2(discord.ui.Select):
    def __init__(self):
        self.horses_ = horses.copy()
        self.odds_ = odds.copy()
        random.shuffle(self.horses_)
        random.shuffle(self.odds_)
        self.ketu = dict(zip(self.horses_, self.odds_))
        options = []
        for name, oddds in self.ketu.items():
            options.append(discord.SelectOption(label=name, description=str(oddds)))
        super().__init__(
            min_values=1,
            max_values=1,
            options=options,
        )
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content=f"<@{interaction.user.id}>\nあなたは{self.values[0]}を選んだ。賭け額を決めろ。", view=Select_Bet_2(self.values[0], self.ketu))

async def is_win(odds):
    a = list()
    for i in range(odds):
        a.append(None)
    a.append("あたり")
    x = random.choice(a)
    if x == "あたり":
        return True
    else:
        return False

class Select_Horse_2(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our View object
        self.add_item(Select_Horse_Menu_2())

class Select_Bet_Menu_2(discord.ui.Select):
    def __init__(self, uma, ketu):
        self.uma = uma
        self.ketu = ketu
        
        options = [
            discord.SelectOption(label="100,000", description=f"入手可能額: {100000*ketu[uma]}"),
            discord.SelectOption(label="50,000", description=f"入手可能額: {50000*ketu[uma]}"),
            discord.SelectOption(label="20,000", description=f"入手可能額: {20000*ketu[uma]}"),
            discord.SelectOption(label="10,000", description=f"入手可能額: {10000*ketu[uma]}"),
            discord.SelectOption(label="5000", description=f"入手可能額: {5000*ketu[uma]}")
                ]
        super().__init__(
            min_values=1,
            max_values=1,
            options=options,
        )
    async def callback(self, interaction: discord.Interaction):
        betint = int(self.values[0].replace(',', ''))
        await interaction.response.edit_message(content=f"<@{interaction.user.id}>\nあなたは{self.uma}に{self.values[0]}円を賭けた。結果を待て。", view=None)
        point.GamesCog.getpoint(interaction.user.id, interaction.user.name, -betint)
        await asyncio.sleep(2)
        res = await is_win(self.ketu[self.uma])
        if res:
            await interaction.message.edit(f"{self.uma}が1着でゴールした。\n<@{interaction.user.id}> **{betint*self.ketu[self.uma]:,}**円を獲得した。")
            point.GamesCog.getpoint(interaction.user.id, interaction.user.name, betint*self.ketu[self.uma]+betint)
        else:
            await interaction.message.edit(content="{}が{}着でゴールした。".format(self.uma, random.randint(2, 6)))

class Select_Bet_2(discord.ui.View):
    def __init__(self, uma, ketu):
        super().__init__()

        # Adds the dropdown to our View object
        self.add_item(Select_Bet_Menu_2(uma, ketu))

class KeibaCog(commands.Cog):
    def __init__(self, bot):
        print("競馬初期化")
        self.bot = bot

    kb = SlashCommandGroup('keiba', '死か、ぼろ儲けか。')

    @kb.command(name="register", description="賭けが始まる。どれに賭けるかは君次第だ。")
    async def kkkkeibaiaaa(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"<@{ctx.user.id}>\n賭けが始まる。賭ける馬を選べ。", view=Select_Horse_2())

def setup(bot):
    bot.add_cog(KeibaCog(bot))