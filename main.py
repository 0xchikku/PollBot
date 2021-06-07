import os
import discord
from discord.ext import commands
import disputils
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice


bot = commands.Bot(command_prefix='-')

my_secret = os.environ['TOKEN']

@bot.command()
async def choice(ctx):
    multiple_choice = BotMultipleChoice(ctx, ['one', 'two', 'three', 'four', 'five', 'six'], "Testing stuff")
    await multiple_choice.run()

    await multiple_choice.quit(multiple_choice.choice)

@bot.command()
async def confirm(ctx):
    confirmation = BotConfirmation(ctx, 0x012345)
    await confirmation.confirm("Are you sure?")

    if confirmation.confirmed:
        await confirmation.update("Confirmed", color=0x55ff55)
    else:
        await confirmation.update("Not confirmed", hide_author=True, color=0xff5555)

bot.run(my_secret)