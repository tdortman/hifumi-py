import datetime
import operator
import random
import urllib
import urllib.request
import discord
import qrcode
import urbandict
from discord.ext import commands
import asyncio
from datetime import datetime
import importlib
from PIL import Image
import requests
import shutil
import os

import reddit
import music
import encryption

bot = commands.Bot(command_prefix="h!")
file = open(r'/files/token.txt', 'r')
TOKEN = file.readline()
file.close()

# Reactions (will do extra files for them eventually)
pat_reactions = [
    "<:Poiblush:476836982727639050> T-Thanks for the p-pat! *blushes deeply*",
    "<a:pikasparkle:699689694639947916> Thank chu so so much!! *smiles brightly*"]

cookie_reactions = [
    "Thank you very much!! *noms*",
    "Your cookies are the best! They're super duper yummy!!",
    "COOKIEEEEEEEEEEEEEEESSSSSSSSSSSS"]


@bot.event
async def on_message(message):
    if message.content.startswith("$cookie <@!665224627353681921>") or \
            message.content.startswith("~cookie <@!665224627353681921>"):
        await message.channel.send(random.choice(cookie_reactions))
    elif message.content.startswith("$pat <@!665224627353681921>") or \
            message.content.startswith("~pat <@!665224627353681921>"):
        await message.channel.send(random.choice(pat_reactions))

    await bot.process_commands(message)


@bot.event
async def on_ready():
    now = datetime.now()
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    channel = await bot.fetch_channel(655484804405657642)
    time = now.strftime("%d/%m/%Y %H:%M:%S")
    await channel.send(f"Logged in as:\n{bot.user.name}\nTime: {time}\n"
                       f"--------------------------")
    game = discord.Game("with best girl Annie!")
    await bot.change_presence(activity=game)


async def reload_modules():
    importlib.reload(encryption)
    importlib.reload(music)
    importlib.reload(reddit)


def current_time():
    return datetime.utcnow()


@bot.command()
async def beautiful(ctx):
    try:
        beautiful_img = Image.open('/files/background.png', 'r')
        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        else:
            user = await bot.fetch_user(int(ctx.message.content.split()[1]))

        user_avatar = str(user.avatar_url).replace("webp", "png")
        r = requests.get(
            user_avatar, stream=True, headers={
                'User-agent': 'Mozilla/5.0'})

        with open(f"/files/{user.id}.png", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

        basewidth = 180
        img = Image.open(f"/files/{user.id}.png")
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save(f'/files/{user.id}_resized.png')

        canvas = Image.new("RGBA", (640, 674))
        canvas.paste(img, (422, 35))
        canvas.paste(img, (430, 377))
        canvas.paste(beautiful_img, None, beautiful_img)
        canvas.save(f"/files/beautiful.png")

        with open(f"/files/beautiful.png", "rb") as g:
            picture = discord.File(g)
            await ctx.send(file=picture)

        os.remove(f"/files/{user.id}.png")
        os.remove(f"/files/{user.id}_resized.png")
        os.remove(f"/files/beautiful.png")

    except ValueError:
        await ctx.send("Invalid ID! Use numbers only please!")
    except IndexError:
        await ctx.send("Seems like you didn't mention anyone!")
    except discord.errors.NotFound:
        await ctx.send("That's not a valid ID!")


@bot.command()
async def redditor(username):
    await reddit.profile(username)


@bot.command()
async def kitsune(ctx):
    await reddit.kitsune(ctx)


@bot.command()
async def sub(message):
    await reddit.sub(message)


@bot.command()
async def wholesome(ctx):
    await reddit.wholesome(ctx)


@bot.command()
async def bunny(ctx):
    await reddit.bunny(ctx)


@bot.command()
async def neko(ctx):
    await reddit.neko(ctx)


@bot.command()
async def thicc(ctx):
    await reddit.thicc(ctx)


@bot.command()
async def animegirl(ctx):
    await reddit.animegirl(ctx)


@bot.command()
async def cipher(ctx):
    await encryption.caeser_cipher(ctx)


@bot.command()
async def emoji(ctx):
    if ctx.message.author.guild_permissions.manage_emojis:
        try:
            content = ctx.message.content.split()
            name, url = content[1], content[2]
            if 'jpg' in url:
                img_type = 'jpg'
            elif 'png' in url:
                img_type = 'png'
            elif 'gif' in url:
                img_type = 'gif'

            r = requests.get(
                url, stream=True, headers={
                    'User-agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                emoji = None
                with open(
                        f"/emojis/{name}.{img_type}",
                        'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                with open(
                        f'/emojis/{name}.{img_type}',
                        'rb') as picture:

                    emoji = await ctx.message.guild.create_custom_emoji(
                        name=name, image=picture.read())

                if emoji and img_type != "gif":
                    msg = f'<:{emoji.name}:{emoji.id}>'
                elif emoji and img_type == "gif":
                    msg = f"<a:{emoji.name}:{emoji.id}>"
                else:
                    msg = 'Emoji object not retrieved!'
                await ctx.message.channel.send(msg)
        except discord.errors.Forbidden:
            msg = "I don't have the permissions for this!"
            await ctx.message.channel.send(msg)
    else:
        await ctx.send("Insufficient Permissions!!")


@bot.command(aliases=["pfp"])
async def avatar(ctx):
    try:
        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        else:
            user = await bot.fetch_user(int(ctx.message.content.split()[1]))
        pfp = str(user.avatar_url).replace(".webp", ".png")
        desc = f"*{user.name}'s avatar*"
        embed = discord.Embed(description=desc, color=0xce3a9b)
        embed.set_image(url=pfp)
        await ctx.send(embed=embed)
    except ValueError:
        await ctx.send("Invalid ID! Use numbers only please!")
    except IndexError:
        await ctx.send("Seems like you didn't mention anyone!")
    except discord.errors.NotFound:
        await ctx.send("That's not a valid ID!")


@bot.command()
async def bye(ctx):
    if ctx.message.author.id == 258993932262834188:
        await ctx.send("Bai baaaaaaaai!!")
        await bot.logout()


@bot.command()
async def ping(ctx):
    if ctx.message.author.id == 258993932262834188:
        while True:
            await ctx.channel.send("<@!258993932262834188>", delete_after=0.2)
            await asyncio.sleep(0.2)
    else:
        await ctx.channel.send("Insufficient permissions!")


@bot.command(aliases=["j"])
async def join(ctx):
    await music.join(ctx)


@bot.command(aliases=["l"])
async def leave(ctx):
    await music.leave(ctx)


@bot.command(aliases=["p"])
async def play(ctx, url: str):
    await music.play(ctx, url)


@bot.command()
async def urban(ctx, message):
    try:
        urban_list = []
        term = message
        word = urbandict.define(term)
        urban_list.append(word[0])
        embed = discord.Embed(title=urban_list[0]["word"],
                              description=urban_list[0]["def"], color=0xce3a9b)

        await ctx.channel.send(embed=embed)
    except urllib.error.HTTPError:
        await ctx.channel.send(
            "I'm sorry, but the definition is either not existent,"
            " or the server"
            " is having issues processing your request.")


@bot.command()
async def calc(ctx, num1, operation, num2):
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '%': operator.mod,
        '/': operator.truediv,
        '//': operator.floordiv,
        '**': operator.pow
    }

    if operation in operators:
        await ctx.channel.send(operators[operation](int(num1), int(num2)))


@bot.command()
async def coinflip(ctx):
    rand_num = random.randint(0, 1)
    if rand_num == 0:
        await ctx.channel.send("Tails!")
    else:
        await ctx.channel.send("Heads!")


@bot.command()
async def qr(ctx, message):
    m = message
    now = datetime.now()
    current_time = now.strftime("%Y%m%d%H%M%S")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=5,
        border=0,
    )
    qr.add_data(m)
    qr.make(fit=True)

    file_name = '{0}.png'.format(current_time[2:])
    img = qr.make_image(fill_color="black", back_color="white")

    img.save(r'/hifumi_qr_code/{0}'.format(
        file_name))
    with open(
            r'/hifumi_qr_code/{0}'.format(
                file_name), 'rb') as picture:
        await ctx.channel.send(file=discord.File(picture, "new_filename.png"))


@bot.command()
async def test1(ctx):
    await ctx.channel.send('Learning Python is fun!!')


@bot.command()
async def cuddle(ctx, message):
    await ctx.channel.send(
        f"*{ctx.message.author.mention} goes up to {message} and cuddles "
        f"tightly, "
        "trying their best to comfort them*")


@bot.command(name='numguess',
             brief='Guess a number between 1 and 100')
async def numguess(ctx, message):
    number = random.randint(1, 100)
    turns = 5
    await ctx.send(
        "Welcome! Time to guess some numbers! You have 5 tries. I'll think"
        " of a number between 1 and 100.")

    def check(author):
        def inner_check(ctx):
            if ctx.message.author != author:
                return False
            try:
                int(ctx.message.content)
                return True
            except ValueError:
                return False

        return inner_check

    while turns != 0:
        await ctx.send("Go try your luck and take a guess!")
        msg = await bot.wait_for("message", check=check, timeout=60)
        guess = int(msg.content)

        if guess > number and turns != 0:
            await message.channel.send(
                f"Woah there, this is way too high!"
                f" Maybe try and guess a lower number next time."
                f" You still have {turns - 1} guesses left")
            turns -= 1
        elif guess < number and turns != 0:
            await message.channel.send(
                f"Awww, too bad! Might wanna go higher next time!"
                f" You have {turns - 1} guesses left!")

            turns -= 1
        if guess == number:
            await message.channel.send(
                f"Yes!! You guessed right! I'm so proud of you!!")
            break
        if guess == number and turns == 5:
            await message.channel.send("YOU'RE SO GOOD!!!! FIRST TRY!!")
            break
        if turns == 0 and guess != number:
            await message.channel.send(
                f"Maybe next time! In case you wondered, my number was {number}!")
            break


@bot.command()
async def test2(ctx, *args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await ctx.channel.send(output)


bot.run(TOKEN)
