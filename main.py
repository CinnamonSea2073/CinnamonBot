from discord.ext import commands
from dotenv import load_dotenv
import os

bot = commands.Bot(debug_guilds=[879288794560471050])
load_dotenv()
TOKEN = os.getenv('TOKEN')
print(TOKEN)

path = "./cogs"


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(error, ephemeral=True)
    else:
        raise error


@bot.event
async def on_ready():
    print(f"Bot名:{bot.user} On ready!!")

bot.load_extension('cogs.others')
bot.load_extension('cogs.itudoko')
bot.load_extension('cogs.point')
bot.load_extension('cogs.hogestory')
bot.load_extension('cogs.superchat')
bot.load_extension('cogs.button_test')
bot.load_extension('cogs.todo')
bot.load_extension('cogs.shogi')
bot.load_extension('cogs.nb')

bot.run(TOKEN)
