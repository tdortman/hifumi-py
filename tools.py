from datetime import datetime
import traceback
import discord

bot = None


def passClientVar(client):
    global bot
    bot = client


async def error_log(message=None, error_msg=None, cmd=None):
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")

    if cmd is None and message is not None:
        cmd = message.content.split()[0][2:]
    elif cmd is None:
        cmd = 'unknown, message missing'
    else:
        cmd = 'unknown'

    tb = str(traceback.format_exc())

    if message is None:
        msg = f"An Error occurred on {current_time}\n" \
              f"**Command used**: {cmd}\n" \
              f"Message data unavailable due to the error not being client-side!\n" \
              f"Error:\n{error_msg}\n\n**{tb}**\n<@258993932262834188>"
    else:
        msg = f"An Error occurred on {current_time}\n" \
              f'**Server:** {message.guild} - {message.guild.id}\n' \
              f'**Room:** {message.channel} - {message.channel.id}\n' \
              f'**User:** {message.author} - {message.author.id}\n' \
              f"**Command used**: {message.content}\n" \
              f"**Error**:\n{error_msg}\n\n**{tb}**\n<@258993932262834188>"

    if message is None:
        channel = bot.get_channel(655484804405657642)
    elif message.channel.id in [655484859405303809, 551588329003548683]:
        channel = message.channel
    else:
        channel = bot.get_channel(655484804405657642)

    try:
        await channel.send(msg)
    except discord.errors.HTTPException:
        await channel.send(f"An Error occurred on {current_time}\nCheck console for full error (2000 character limit)\n"
                           f"<@258993932262834188>")
        print(msg)


async def download_attachments(message):
    if message.attachments and not message.author.bot:
        for item in message.attachments:
            attach = await item.to_file(use_cached=True)
            await message.channel.send(file=attach)


async def help_cmd(message):
    msgs = ["**h!avatar @user/user-id** - take a nice look at that cool avatar "
            "your friend or even a stranger has\n\n**h!emoji <name> <emoji/url>** - lets you quickly add any "
            "emoji/image as an emoji in your server\n\n**h!convert <amount> <currency1> <currency2>** - for all those "
            "occasions where you might wanna quickly convert money from one currency to another\n\n**h!currencies** - "
            "gives you a nice list of all the currencies you can use for conversion\n\n**h!qr <text>** - for whenever "
            "you want to generate a QR-code from any text\n\n**h!calc <num1> <operator> <num2>** - a very basic "
            "calculator to play around with for fun\n\n**h!coinflip** - for all those indecisive people who can't "
            "decide what to eat for dinner\n\n**h!urban <term>** - gives you the first five definitions"
            " on Urban Dictionary for your search term\n\n**h!cipher <text> <num>** - a nice and simple encryption"
            " method if you want to send secret messages\n\n**h!numguess** - let's you guess a number"
            " between 1 and 100\n\n"
            "**h!beautiful @user/user-id** - shows your friend how beautiful they are, even if they don't want to"
            " admit it\n\n**h!resize <width> <emoji/url>** - let's you resize any emoji or image you want\n\n"
            "**h!imgur <url>** - let's you upload any image to imgur",

            "**h!sub <name>** - gives you one of the hot or top rated image posts from a "
            "specific subreddit\n\n**h!sub text <name>** - gives you one of the hot or top rated text posts from a "
            "specific subreddit\n\n**h!kitsune** - fox girls, who doesn't love them\n\n"
            "**h!neko** - for all you cat girl lovers (nsfw)\n\n**h!wholesome** - your daily dose of wholesome"
            " anime memes\n\n**h!bunny** - bunny girls, what were you expecting\n\n**h!thicc** - for all you thigh"
            " connoisseurs out there (nsfw)\n\n**h!animegirl** - sometimes simple girls are best girl\n\n"
            "**h!redditor <name>** - for a nice breakdown of someone's reddit profile"]

    titles = ["**List of Yukino's commands**", "**Reddit commands**"]

    for i in range(2):
        embed = discord.Embed(title=f"{titles[i]}", description=f"{msgs[i]}", colour=0xce3a9b)
        await message.channel.send(embed=embed)


