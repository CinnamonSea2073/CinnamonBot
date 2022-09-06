from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
import traceback

bot = commands.Bot(debug_guilds=[879288794560471050])
load_dotenv()
TOKEN = os.getenv('TOKEN')
print(TOKEN)

path = "./cogs"


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(error)
        await bot.get_partial_messageable(1009731664412426240).send(error)#traceback.format_exc())
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond(content="管理者限定やで", ephemeral=True)
    else: 
        await bot.get_partial_messageable(1009731664412426240).send(error)#traceback.format_exc())
        raise error


@bot.event
async def on_ready():
    print(f"Bot名:{bot.user} On ready!!")

bot.load_extension('cogs.others')
#bot.load_extension('cogs.itudoko')
#bot.load_extension('cogs.point')
#bot.load_extension('cogs.hogestory')
#bot.load_extension('cogs.superchat')
#bot.load_extension('cogs.help')
bot.load_extension('cogs.todo')
bot.load_extension('cogs.shogi', store=False)
#bot.load_extension('cogs.nb')
#bot.load_extension('cogs.keiba')
#bot.load_extension('cogs.stat')
#bot.load_extension('cogs.timer')
#bot.load_extension('cogs.talk')
#bot.load_extension('cogs.genshin', store=False)
#bot.load_extension('cogs.test')

bot.run(TOKEN)
