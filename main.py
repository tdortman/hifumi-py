import operator
import random
import urllib
from urllib import request
import discord
import qrcode
from udpy import UrbanClient
import asyncio
import importlib
from PIL import Image
import requests
import shutil
import os
from pathlib import Path
from PIL import ImageFile
from datetime import datetime as dt
import time
import reddit
import music
import encryption
import pillow
import tools
from tools import error_log

bot = None


def passClientVar(client):
    global bot
    bot = client


# Reactions (will do extra files for them eventually)
pat_reactions = [
    "<:Poiblush:476836982727639050> T-Thanks for the p-pat! *blushes deeply*",
    "<a:pikasparkle:699689694639947916> Thank chu so so much!! *smiles brightly*"]

cookie_reactions = [
    "Thank you very much!! *noms*",
    "Your cookies are the best! They're super duper yummy!!",
    "COOKIEEEEEEEEEEEEEEESSSSSSSSSSSS"]


async def message_in(message):
    try:
        if message.content.startswith("h!"):
            cmd = message.content.split()[0][2:].lower()

            try:
                sub_cmd = message.content.split()[1].lower()
            except:
                sub_cmd = None

            if cmd == "beautiful":
                await pillow.beautiful(message)
            if cmd == "redditor":
                await reddit.profile(message)
            if cmd == "kitsune":
                await reddit.sub(message, "kitsunemimi")
            if cmd == "sub":
                if sub_cmd == "text":
                    await reddit.self_posts(message)
                else:
                    await reddit.sub(message, message.content.split()[-1])
            if cmd == "wholesome":
                await reddit.sub(message, "wholesomeanimemes")
            if cmd == "bunny":
                await reddit.sub(message, "usagimimi")
            if cmd == "neko":
                await reddit.sub(message, "nekomimi")
            if cmd == "thicc":
                await reddit.sub(message, "thighdeology")
            if cmd == "animegirl":
                await reddit.sub(message, "animegirl")
            if cmd == "cipher":
                await encryption.caeser_cipher(message)
            if cmd == "emoji":
                await emoji(message)
            if cmd in ["pfp", "avatar"]:
                await avatar(message)
            if cmd == "bye":
                await bye(message)
            if cmd in ["join", "j", "joi"]:
                await message.channel.send("Sorry, this command is currently unavailable!")
            if cmd in ["leave", "leav", "l"]:
                await message.channel.send("Sorry, this command is currently unavailable!")
            if cmd in ["play", "p"]:
                await message.channel.send("Sorry, this command is currently unavailable!")
            if cmd == "urban":
                await message.channel.send("An error occurred! Please try again later")
            if cmd == "calc":
                await calc(message)
            if cmd == "coinflip":
                await coinflip(message)
            if cmd == "numguess":
                await message.channel.send("An error occurred! Please try again later")
            if cmd == "cuddle":
                await cuddle(message)
            if cmd == "qr":
                await qr(message)
            if cmd in ['convert', 'conv', 'con', 'c']:
                await convert(message)
            if cmd == "error":
                await error_log(message, "This is a test error!")
            # if cmd == "sauce":
            # await sauce(message)
            if cmd == "resize":
                await pillow.resize_img(message)
            if cmd == 'imgur':
                await pillow.imgur(message)
            if cmd in ['currencies', 'currency', 'cur', 'cu']:
                await currency_codes(message)
    except Exception as e:
        await error_log(message, e)


async def reload_modules():
    importlib.reload(encryption)
    importlib.reload(music)
    importlib.reload(reddit)
    importlib.reload(pillow)
    importlib.reload(tools)


def current_time():
    return int(time.time())


currencies = {
    'EUR': 'Euro', 'AED': 'Emirati Dirham', 'AUD': 'Australian Dollar', 'ARS': 'Argentine Peso',
    'BGN': 'Bulgarian lev', 'BRL': 'Brazilian Real', 'BSD': 'Bahamian Dollar', 'CAD': 'Canadian Dollar',
    'CHF': 'Swiss Franc', 'CLP': 'Chilean Peso', 'CNY': 'Chinese Yuan', 'COP': 'Colombian Peso',
    'CZK': 'Czech Koruna', 'DKK': 'Danish Krone', 'DOP': 'Dominican Peso', 'EGP': 'Egyptian Pound',
    'FJD': 'Fijian Dollar', 'GBP': 'Pound Sterling', 'GTQ': 'Guatemalan Quetzal', 'HKD': 'Hong Kong Dollar',
    'HRK': 'Croatian Kuna', 'HUF': 'Hungarian Forint', 'IDR': 'Indonesian Rupiah', 'ILS': 'Israeli Shekel',
    'INR': 'Indian Rupee', 'ISK': 'Icelandic Króna', 'JPY': 'Japanese Yen', 'KRW': 'South Korean Won',
    'KZT': 'Kazakhstani Tenge', 'MVR': 'Maldivian Rufiyaa', 'MXN': 'Mexican Peso', 'MYR': 'Malaysian Ringgit',
    'NOK': 'Norwegian Krone', 'NZD': 'New Zealand Dollar', 'PEN': 'Peruvian Sol', 'PHP': 'Philippine Peso',
    'PKR': 'Pakistani Rupee', 'PLN': 'Polish Złoty', 'PYG': 'Paraguayan Guaraní', 'RON': 'Romanian Leu',
    'RUB': 'Russian Rouble', 'SAR': 'Saudi Riyal', 'SEK': 'Swedish Krona', 'SGD': 'Singapore Dollar',
    'THB': 'Thai Baht', 'TRY': 'Turkish Lira', 'TWD': 'New Taiwan Dollar', 'UAH': 'Ukrainian Hryvnia',
    'USD': 'United States Dollar', 'UYU': 'Uruguayan Peso', 'ZAR': 'South African Rand'
}


async def convert(message):
    try:
        content = message.content.split()
        if len(content) == 1:
            await message.channel.send("You have to specify the amount of money you want to convert, as well as the "
                                       "currencies!")
            return

        val, cur1, cur2 = float(content[1]), content[2].upper(), content[3].upper()

        url = f'https://prime.exchangerate-api.com/v5/7113ac9174ade28a0e1e5eed/latest/{cur1}'
        response = requests.get(url)
        result = response.json()
        if result['result'] == 'error':
            if result['error'] == 'unknown-code':
                await message.channel.send(f"{cur1} is not a valid currency code!")
            else:
                await message.channel.send("An unknown error occurred! Please try again later!")
            return

        data = result['conversion_rates']

        if cur2 not in data:
            await message.channel.send(f"{cur2} is not a valid currency code!")
            return
        rslt = round(val * data[cur2], 2)
        desc = f"**{round(val)} {cur1} ≈ {rslt} {cur2}**\n\n" \
               f"Exchange rate:\n1 {cur1} ≈ {data[cur2]} {cur2}"

        embed = discord.Embed(description=desc, title=f"Converting {currencies[cur1]} into {currencies[cur2]}",
                              color=0xce3a9b)
        embed.set_footer(text=f"{dt.utcnow().strftime('%d/%m/%Y %H:%M:%S')} UTC\nUse the command h!currencies for a "
                              f"list of currencies available for conversion")
        await message.channel.send(embed=embed)

    except Exception as e:
        await error_log(message, e)


async def currency_codes(message):
    title = 'List of currencies available for conversion'
    columns = ["", "", ""]
    currency_keys = sorted(list(currencies))

    for i in range(len(currency_keys)):
        if i <= 16:
            columns[0] += str(f"**{currency_keys[i]}** - {currencies[str(currency_keys[i])]}\n")
        elif 17 <= i <= 33:
            columns[1] += str(f"**{currency_keys[i]}** - {currencies[str(currency_keys[i])]}\n")
        else:
            columns[2] += str(f"**{currency_keys[i]}** - {currencies[str(currency_keys[i])]}\n")

    embed = discord.Embed(title=title, color=0xce3a9b)
    for i in range(3):
        embed.add_field(name='\u200b', value=columns[i])
    await message.channel.send(embed=embed)


async def description():
    pass


async def sauce(message):
    sauce = SauceNao(api_key=None, testmode=0, dbmask=None, dbmaski=None,
                     db=DB.ALL, numres=6, hide=Hide.NONE, bgcolor=Bgcolor.NONE)

    url = message.content.split()[1]
    # url = "https://cdn.discordapp.com/attachments/551588329003548683/715332085572829184/73375795_p0_master1200.jpg"

    r = requests.get(
        url, stream=True, headers={
            'User-agent': 'Mozilla/5.0'})

    with open(f"files/test_sauce.png", 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

    results = sauce.from_url(url)

    if results[0].author is not None:
        desc = f"[Link to image by {results[0].author}]({results[0].url})"
    else:
        desc = None

    embed = discord.Embed(title=results[0].title, description=desc, colour=0xce3a9b)
    # embed.se
    embed.set_footer(text=f"Similarity: {results[0].similarity}%  ")

    await message.channel.send(embed=embed)


async def emoji(message):
    if message.author.guild_permissions.manage_emojis:
        try:
            content = message.content.split()
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
                with open(f"emojis/{name}.{img_type}", 'wb') as f:

                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    print("Successfully downloaded image!")
                print(Path(f"emojis/{name}.{img_type}").stat().st_size)
                print(img_type)

                if Path(f"emojis/{name}.{img_type}").stat().st_size > 256000 and img_type == "jpg" or img_type == "png":
                    basewidth = 128
                    img = Image.open(f"emojis/{name}.{img_type}")
                    wpercent = (basewidth / float(img.size[0]))
                    hsize = int((float(img.size[1]) * float(wpercent)))
                    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
                    img.save(f"emojis/{name}.{img_type}")

                elif Path(f"emojis/{name}.{img_type}").stat().st_size > 256000 and img_type == "gif":
                    await message.channel.send("This gif is too big to be uploaded! Try resizing it first.")
                    return

                with open(
                        f"emojis/{name}.{img_type}", "rb") as picture:

                    emoji = await message.guild.create_custom_emoji(
                        name=name, image=picture.read())

                if emoji and img_type != "gif":
                    msg = f'<:{emoji.name}:{emoji.id}>'
                elif emoji and img_type == "gif":
                    msg = f"<a:{emoji.name}:{emoji.id}>"
                else:
                    msg = 'Emoji object not retrieved!'
                await message.channel.send(msg)

            os.remove(f"emojis/{name}.{img_type}")

        except discord.errors.Forbidden:
            await message.channel.send("I don't have the permissions for this!")
        except Exception as e:
            await error_log(message, e)
    else:
        await message.channel.send("Insufficient Permissions!!")


def getsizes(url):
    file = urllib.request.urlopen(url)
    size = int(file.headers.get("content-length"))
    p = ImageFile.Parser()
    while True:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size
    file.close()
    return size


async def avatar(message):
    try:
        if len(message.content.split()) == 1:
            user = message.author
        elif message.mentions:
            user = message.mentions[0]
        else:
            user = await bot.fetch_user(int(message.content.split()[1]))
        pfp = str(user.avatar_url).replace(".webp", ".png")
        desc = f"*{user.name}'s avatar*"
        embed = discord.Embed(description=desc, color=0xce3a9b)
        embed.set_image(url=pfp)
        await message.channel.send(embed=embed)

    except ValueError:
        await message.channel.send("Invalid ID! Use numbers only please!")
    except IndexError:
        await message.channel.send("Seems like you didn't mention anyone!")
    except discord.errors.NotFound:
        await message.channel.send("That's not a valid ID!")
    except Exception as e:
        await error_log(message, e)


async def bye(message):
    try:
        if message.author.id == 258993932262834188:
            await message.channel.send("Bai baaaaaaaai!!")
            await bot.logout()
    except Exception as e:
        await error_log(message, e)


async def urban(message):
    try:
        client = UrbanClient()
        if message.content.split()[1] == "random":
            defs = client.get_random_definition()
        else:
            urban_word = " ".join(message.content.split()[1:])
            defs = client.get_definition(urban_word)

        defs_sliced = defs[:5]
        pages = []
        for i in range(5):
            desc = f"**Definition**:\n{str(defs_sliced[i].definition).replace('[', '').replace(']', '')}\n\n" \
                   f"**Example**:\n{defs_sliced[i].example.replace('[', '').replace(']', '')}"
            footer = f"Upvotes: {defs_sliced[i].upvotes}  Downvotes: {defs_sliced[i].downvotes}\nPage {i + 1}/5"

            page = discord.Embed(title=defs_sliced[i].word,
                                 description=desc,
                                 color=0xce3a9b)
            page.set_footer(text=footer)
            pages.append(page)

        message = await message.channel.send(embed=pages[0])

        await message.add_reaction("\u2B05")
        await message.add_reaction("\u27A1")
        i = 0
        emoji = ""
        while True:
            if emoji == "\u2B05" and i == 0:
                i += 4
                await message.edit(embed=pages[i])
            if emoji == "\u2B05" and i > 0:
                i -= 1
                await message.edit(embed=pages[i])
            if emoji == "\u27A1" and i == 4:
                i -= 4
                await message.edit(embed=pages[i])
            if emoji == "\u27A1" and i < 4:
                i += 1
                await message.edit(embed=pages[i])

            res = await bot.wait_for("reaction_add", timeout=60.0)
            if res is None:
                break
            if str(res[1].id) != 665224627353681921:
                emoji = str(res[0].emoji)
                await message.remove_reaction(res[0].emoji, res[1])
    except IndexError:
        await message.channel.send("Make sure you enter a valid word to search for!")
    except asyncio.TimeoutError:
        return
    except Exception as e:
        await error_log(message, e)


async def calc(message):
    try:
        num1 = message.content.split()[1]
        operation = message.content.split()[2]
        num2 = message.content.split()[3]

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
            await message.channel.send(operators[operation](int(num1), int(num2)))
    except Exception as e:
        await error_log(message, e)


async def coinflip(message):
    try:
        rand_num = random.randint(0, 1)
        if rand_num == 0:
            await message.channel.send("Tails!")
        else:
            await message.channel.send("Heads!")
    except Exception as e:
        await error_log(message, e)


async def qr(message):
    try:
        m = " ".join(message.content.split()[1:])

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=5,
            border=0,
        )
        qr.add_data(m)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        img.save('hifumi_qr_code/unknown.png')

        with open('hifumi_qr_code/unknown.png', 'rb') as picture:
            await message.channel.send(file=discord.File(picture, "unknown.png"))
        os.remove('hifumi_qr_code/unknown.png')

    except Exception as e:
        await error_log(message, e)


async def test(message):
    await message.channel.send('Learning Python is fun!!')


async def cuddle(message):
    try:
        target = message.mentions[0]
        await message.channel.send(
            f"*{message.author.mention} goes up to {target} and cuddles tightly, "
            "trying their best to comfort them*")
    except Exception as e:
        await error_log(message, e)


async def numguess(message):
    try:
        number = random.randint(1, 100)
        turns = 5
        await message.channel.send(
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
            await message.channel.send("Go try your luck and take a guess!")
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
    except asyncio.TimeoutError:
        return
    except Exception as e:
        await error_log(message, e)
