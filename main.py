import os
import discord
from discord.ext import commands
import disputils
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
from discord_components import DiscordComponents, Button



bot = commands.Bot(command_prefix='-')

# ddb = DiscordButton(bot)

my_secret = os.environ['TOKEN']

@bot.event
async def on_ready():
    DiscordComponents(bot)
    print(f"Logged in as {bot.user}!")

@bot.command()
async def choice(ctx):
    multiple_choice = BotMultipleChoice(ctx, ['one', 'two', 'three', 'four', 'five', 'Hello'], "Testing stuff")
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

@bot.command()
async def paginate(ctx):
    embeds = [
        discord.Embed(title="test page 1", description="This is just some test content!", color=0x115599),
        discord.Embed(title="test page 2", description="Nothing interesting here.", color=0x5599ff),
        discord.Embed(title="test page 3", description="Why are you still here?", color=0x191638)
    ]

    paginator = BotEmbedPaginator(ctx, embeds)
    await paginator.run()


@bot.command()
async def button(ctx):
    await ctx.send(
        "Hello, World!",
        components = [
            Button(label = "WOW button!")
        ]
    )

    interaction = await bot.wait_for("button_click", check = lambda i: i.component.label.startswith("WOW"))
    await interaction.respond(content = "Button clicked!")


# @bot.event
# async def on_message(msg):
#     m = await msg.channel.send(
#         "Content",
#         buttons=[
#             Button(style=ButtonStyle.blue, label="Blue"),
#             Button(style=ButtonStyle.red, label="Red"),
#             Button(style=ButtonStyle.URL, label="url", url="https://google.com"),
#         ],
#     )

#     res = await ddb.wait_for_button_click(m)
#     await res.respond(
#         type=InteractionType.ChannelMessageWithSource,
#         content=f'{res.button.label} clicked'
#     )


bot.run(my_secret)