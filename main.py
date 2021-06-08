import os
import discord
from discord.ext import commands
import disputils
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
from discord_components import DiscordComponents, Button
from discord.ext.commands import Bot

from discord import Embed
from discord.ext.commands import command, Cog
from discord_components import DiscordComponents, Button, ButtonStyle

from asyncio import TimeoutError, sleep
from random import choice
import asyncio

import random
from random import randint
import pyttsx3

#command prefix
bot = commands.Bot(command_prefix='-')

# ddb = DiscordButton(bot)

#Bot TOKEN
my_secret = os.environ['TOKEN']

#on_ready command
@bot.event
async def on_ready():
    DiscordComponents(bot)
    bot.add_cog(TicTacToe(bot))
    print(f"Logged in as {bot.user}!")


@bot.command()
async def weather(ctx):
    pass


#choice command
@bot.command()
async def choice(ctx):
    multiple_choice = BotMultipleChoice(ctx, ['one', 'two', 'three', 'four', 'five', 'Hello'], "Testing stuff")
    await multiple_choice.run()

    await multiple_choice.quit(multiple_choice.choice)

#confirm command
@bot.command()
async def confirm(ctx):
    confirmation = BotConfirmation(ctx, 0x012345)
    await confirmation.confirm("Are you sure?")

    if confirmation.confirmed:
        await confirmation.update("Confirmed", color=0x55ff55)
    else:
        await confirmation.update("Not confirmed", hide_author=True, color=0xff5555)

#paginate command
@bot.command()
async def paginate(ctx):
    embeds = [
        discord.Embed(title="test page 1", description="This is just some test content!", color=0x115599),
        discord.Embed(title="test page 2", description="Nothing interesting here.", color=0x5599ff),
        discord.Embed(title="test page 3", description="Why are you still here?", color=0x191638)
    ]

    paginator = BotEmbedPaginator(ctx, embeds)
    await paginator.run()

#button command
@bot.command()
async def button(ctx):
    await ctx.send(
        "Search Engine",
        components = [
          [
            Button(label="Google"),
            Button(label="Bing"),
            Button(label="DuckDuckGo")
			]
        ]
    )

    def check(res):
      return True

    while True:
      interaction = await bot.wait_for("button_click", check=check)
      #await msg.edit(components=[])
      await interaction.respond(content = "https://www.google.com") 
	
#Random Response Command
@bot.command(aliases=['ques'])
async def question(ctx,*,ques):
    responses = [
        'Yes',
        'No',
        'Not Sure',
        'Definitly',
        'Try Hard',
        'Possible',
        'Ask Again',
        'learn every waking hour',
        'Believe'
    ]
    await ctx.send(f'Question: {ques}\nAnswer: {random.choice(responses)}')	

@bot.command()
async def ask(ctx, question):
  answer = randint(1, 5)
  if answer == 1:
    await ctx.send("I'll say YES!")
  if answer == 2:
    await ctx.send("I'm not really sure, sorry.")
  if answer == 3:
    await ctx.send("Isn't that impossible?")
  if answer == 4:
    await ctx.send("I have to say yes for now...")
  if answer == 5:
    await ctx.send("It's a big fat NO for me.")

@bot.command()
async def ask_tts(ctx, question):
  answer = randint(1, 5)
  if answer == 1:
    await ctx.send("you should!", tts = True)
  if answer == 2:
    await ctx.send("not really sure about that...", tts = True)
  if answer == 3:
    await ctx.send("No! How ridiculous", tts = True)
  if answer == 4:
    await ctx.send("I have to say yes for now...", tts = True)
  if answer == 5:
    await ctx.send("It's a No for me...", tts = True)

#TicTacToe Class (Game)
class TicTacToe(Cog):
    def __init__(self, bot):
        self.bot = bot


    @command()
    async def tictactoe(self, ctx, member: discord.Member):
        if ctx.author == member:
            return await ctx.send("You can't play against yourself!")
        embed = discord.Embed(color=0xF5F5F5, title=f"Hey, {ctx.author.name} wants to play tic-tac-toe with you!")
        acceptdenycomps = [
            [
                Button(style=ButtonStyle.green, label="Accept"),
                Button(style=ButtonStyle.red, label="Decline")
            ]
        ]
        #
        board = [
            [
                Button(style=ButtonStyle.grey, label="⠀", id="0 0"),
                Button(style=ButtonStyle.grey, label="⠀", id="0 1"),
                Button(style=ButtonStyle.grey, label="⠀", id="0 2")

            ],
            [
                Button(style=ButtonStyle.grey, label="⠀", id="1 0"),
                Button(style=ButtonStyle.grey, label="⠀", id="1 1"),
                Button(style=ButtonStyle.grey, label="⠀", id="1 2")

            ],
            [
                Button(style=ButtonStyle.grey, label="⠀", id="2 0"),
                Button(style=ButtonStyle.grey, label="⠀", id="2 1"),
                Button(style=ButtonStyle.grey, label="⠀", id="2 2")
            ]
        ]
        selections = [
            [
                "unchosen",
                "unchosen",
                "unchosen"
            ],
            [
                "unchosen",
                "unchosen",
                "unchosen"
            ],
            [
                "unchosen",
                "unchosen",
                "unchosen"
            ]
        ]
        
        m = await ctx.send(embed=embed, components=acceptdenycomps, content=member.mention)
        def haswon(team):
            if selections[0][0] == team and selections[0][1] == team and selections[0][2] == team:
                return True
            if selections[1][0] == team and selections[1][1] == team and selections[1][2] == team:
                return True
            if selections[2][0] == team and selections[2][1] == team and selections[2][2] == team:
                return True
            if selections[0][0] == team and selections[1][0] == team and selections[2][0] == team:
                return True
            if selections[0][1] == team and selections[1][1] == team and selections[2][1] == team:
                return True
            if selections[0][2] == team and selections[1][2] == team and selections[2][2] == team:
                return True
            if selections[0][0] == team and selections[1][1] == team and selections[2][2] == team:
                return True
            if selections[0][2] == team and selections[1][1] == team and selections[2][0] == team:
                return True
            else:
                return False
        def istie(team):
            if not "unchosen" in str(selections):
                if not haswon(team):

                    return True
                else:

                    return False
            else:

                return False


        def confirmcheck(res):
            return res.user.id == member.id and res.channel.id == ctx.channel.id and str(res.message.id) == str(m.id)

        try:
            res = await self.bot.wait_for("button_click", check=confirmcheck, timeout=50)
        except asyncio.TimeoutError:
            await m.edit(
                embed=Embed(color=0xED564E, title="Timeout!", description="No-one reacted. ☹️"),
                components=[
                    Button(style=ButtonStyle.red, label="Oh-no! Timeout reached!", disabled=True),
                    Button(style=ButtonStyle.URL, label="View creator", url="https://github.com/MadhanArts")
                ],
            )
            return
        await res.respond(type=6)
        if res.component.label == "Accept":
            accept = True
            embed = discord.Embed(color=discord.Colour.green(), title=f'{member.name} has accepted!', description="The game will now begin...")
            await m.edit(embed=embed)
            await asyncio.sleep(1)

        else:
            accept = False
            embed = discord.Embed(color=discord.Colour.red(), title=f'{member.name} has declined.')
            await m.edit(embed=embed)
            return
        
        async def winner(team):
            if team == "red":
                color = discord.Colour.red()
                user = member
            if team == "green":
                color = discord.Colour.green()
                user = ctx.author
            e = discord.Embed(color=color, title=f"{user.name} has won!")
            board.append(Button(style=ButtonStyle.URL, label="View creator", url="https://github.com/MadhanArts"))
            await m.edit(embed=e, components=board)
            return

            
        
        greensturnembed = discord.Embed(color=0xF5F5F5, title=f"{ctx.author.name}'s turn")
        redsturnembed = discord.Embed(color=0xF5F5F5, title=f"{member.name}'s turn")
        greenstatus = True
        # True = green False = red
        def greensturncheck(res):
            return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id and res.message.id == m.id
        def redsturncheck(res):
            return res.user.id == member.id and res.channel.id == ctx.channel.id and res.message.id == m.id
        while accept:
            if greenstatus:
                await m.edit(embed=greensturnembed, components=board)
                try:
                    res = await self.bot.wait_for("button_click", check=greensturncheck, timeout=50)
                    await res.respond(type=6)
                    listid = res.component.id
                    firstpart, secondpart = listid.split(' ')
                    board[int(firstpart)][int(secondpart)] = Button(style=ButtonStyle.green, label="⠀", id="1 0", disabled=True)
                    selections[int(firstpart)][int(secondpart)] = "green"
                    if haswon('green'):
                        await winner('green')
                        accept = False
                        return
                    if istie('green'):
                        e = discord.Embed(color=0xF5F5F5, title=f"Call it a tie!")
                        board.append(Button(style=ButtonStyle.URL, label="View creator", url="https://github.com/MadhanArts"))
                        await m.edit(embed=e, components=board)
                        accept = False
                        return
                    greenstatus = False
                    pass
                    

                except asyncio.TimeoutError:
                    await m.edit(
                        embed=Embed(color=0xED564E, title="Timeout!", description="No-one reacted. ☹️"),
                        components=[
                            Button(style=ButtonStyle.red, label="Oh-no! Timeout reached!", disabled=True),
                            Button(style=ButtonStyle.URL, label="View creator", url="https://github.com/MadhanArts")
                        ],
                    )
                    return
            if not greenstatus:
                await m.edit(embed=redsturnembed, components=board)
                try:
                    res = await self.bot.wait_for("button_click", check=redsturncheck, timeout=50)
                    await res.respond(type=6)
                    listid = res.component.id
                    firstpart, secondpart = listid.split(' ')
                    board[int(firstpart)][int(secondpart)] = Button(style=ButtonStyle.red, label="⠀", id="1 0",
                                                                 disabled=True)
                    selections[int(firstpart)][int(secondpart)] = "red"
                    if haswon('red'):
                        await winner('red')
                        accept = False
                        return
                    if istie('red'):
                        e = discord.Embed(color=0xF5F5F5, title=f"Call it a tie!")
                        board.append(Button(style=ButtonStyle.URL, label="View creator", url="https://github.com/MadhanArts"))
                        await m.edit(embed=e, components=board)
                        accept = False
                        return
                        
                    greenstatus = True
                    pass


                except asyncio.TimeoutError:
                    await m.edit(
                        embed=Embed(color=0xED564E, title="Timeout!", description="No-one reacted. ☹️"),
                        components=[
                            Button(style=ButtonStyle.red, label="Oh-no! Timeout reached!", disabled=True),
                            Button(style=ButtonStyle.URL, label="View creator", url="https://github.com/MadhanArts")
                        ],
                    )
                    return
#error event
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.errors.MissingRequiredArgument):
    await ctx.send("You didn't provide any answers.")

bot.run(my_secret)