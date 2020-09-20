import operator
import random
import discord
import qrcode
from udpy import UrbanClient
import asyncio
from importlib import reload
from PIL import Image
import requests
import os
from pathlib import Path
from datetime import datetime as dt
from math import pi, sqrt, log, e
import reddit
import music
import encryption
import pillow
import tools
from tools import error_log, download_url, extract_emoji

bot = None


def passClientVar(client):
    global bot
    bot = client


BOT_OWNER = 258993932262834188


async def message_in(message):
    try:
        content = message.content.split()
        react_cmd = content[0][1:] if len(content) > 1 else None

        if message.content.startswith("h!"):
            cmd = content[0].strip("h!")
            sub_cmd = content[1] if len(content) >= 2 else None

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
                    await reddit.sub(message, content[1])

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
                if sub_cmd in ['server', 's', 'serve', 'serv']:
                    await server_icon(message)
                else:
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
                await message.channel.send("Sorry, this command is currently unavailable!")

            if cmd == "calc":
                await calc(message)

            if cmd == "coinflip":
                await coinflip(message)

            if cmd == "numguess":
                await numguess(message)

            if cmd == "cuddle":
                await cuddle(message)

            if cmd == "qr":
                await qr(message)

            if cmd in ['convert', 'conv', 'con', 'c']:
                await convert(message)

            if cmd == "error":
                await error_log(message, "This is a test error!")

            if cmd == "resize":
                await pillow.resize_img(message)

            if cmd == 'imgur':
                await pillow.imgur(message)

            if cmd == 'tess':
                await pillow.extract_string_image(message)

            if cmd in ['currencies', 'currency', 'cur', 'cu']:
                await currency_codes(message)

            if cmd in ['commands', 'command', 'comm', 'com']:
                await tools.help_cmd(message)

            if cmd == 'py':
                await py_eval(message)

            if cmd == 'ping':
                await ping(message)

            if cmd == "test":
                await test_cmd(message)

        elif message.content.startswith(f"${react_cmd} <@!641409330888835083>") or \
                message.content.startswith(f"${react_cmd} <@641409330888835083>"):

            print(react_cmd)
            for cmd_type in tools.emote_msg:
                if react_cmd in tools.emote_msg[cmd_type]:
                    msg = random.choice(tools.react_msg[cmd_type])
                    print(msg)
                    await asyncio.sleep(1)
                    await message.channel.send(msg.format(message.author.name))

    except Exception as e:
        await error_log(message, e)


async def reload_modules():
    reload(encryption)
    reload(music)
    reload(reddit)
    reload(pillow)
    reload(tools)


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


async def test_cmd(message):
    pass


async def ping(message):
    latency = round(bot.latency * 1000)
    await message.channel.send(f"Latency: **{latency}ms**")


async def py_eval(message):
    try:
        if message.author.id == BOT_OWNER:
            cmd = " ".join(x for x in message.content.split()[1:])
            rslt = eval(cmd)
            await message.channel.send(rslt)
        else:
            await message.channel.send("Insufficient permissions!")
    except Exception as e:
        await error_log(message, e)


async def convert(message):
    try:
        content = message.content.split()
        if len(content) == 1:
            await message.channel.send("You have to specify the amount of money you want to convert, as well as the "
                                       "currencies!")
            return

        val, cur1, cur2 = float(content[1]), content[2].upper(), content[3].upper()

        url = f'https://prime.exchangerate-api.com/v5/81f453a13268228658567d13/latest/{cur1}'
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
        desc = f"**{val} {cur1} ≈ {rslt} {cur2}**\n\n" \
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


async def emoji(message):
    if message.author.guild_permissions.manage_emojis:
        try:
            content = message.content.split()
            name = content[1]

            if content[1].startswith("<") or "http" in content[1]:
                await message.channel.send("You didn't specify a name for the emoji!")
                return

            if content[2].startswith("<"):
                url = await extract_emoji(message)
            else:
                url = content[2]

            if len(name) > 32:
                await message.channel.send("Don't you think that name is a bit too long?..")
                return
            elif len(name) < 2:
                await message.channel.send("That name is too short! Try again with a longer one")
                return

            if 'jpg' in url:
                img_type = 'jpg'
            elif 'png' in url:
                img_type = 'png'
            elif 'gif' in url:
                img_type = 'gif'

            await download_url(url, f"emojis/{name}.{img_type}")

            if Path(f"emojis/{name}.{img_type}").stat().st_size > 256000 and img_type == "jpg" or \
                    Path(f"emojis/{name}.{img_type}").stat().st_size > 256000 and img_type == "png":

                await pillow.resize(f"emojis/{name}.{img_type}", 128, f"emojis/{name}_resized.{img_type}")

                if Path(f"emojis/{name}_resized.{img_type}").stat().st_size > 256000:
                    await message.channel.send("Even after being resized to 128px your image is still too big.. ")
                    return
                else:
                    with open(f"emojis/{name}_resized.{img_type}", "rb") as picture:
                        emoji = await message.guild.create_custom_emoji(name=name, image=picture.read())

            elif Path(f"emojis/{name}.{img_type}").stat().st_size > 256000 and img_type == "gif":
                await pillow.resize_gif(message, f"emojis/{name}.{img_type}", f"emojis/{name}_resized.{img_type}",
                                        (128, 128))

                if Path(f"emojis/{name}_resized.{img_type}").stat().st_size > 256000:
                    await message.channel.send("Even after being resized to 128px your gif is still too big.. ")
                    return
                else:
                    with open(f"emojis/{name}_resized.{img_type}", "rb") as picture:
                        emoji = await message.guild.create_custom_emoji(name=name, image=picture.read())

            else:
                with open(f"emojis/{name}.{img_type}", "rb") as picture:
                    emoji = await message.guild.create_custom_emoji(name=name, image=picture.read())

            if emoji and img_type != "gif":
                msg = f'<:{emoji.name}:{emoji.id}>'
            elif emoji and img_type == "gif":
                msg = f"<a:{emoji.name}:{emoji.id}>"
            else:
                msg = 'Emoji object not retrieved!'
            await message.channel.send(msg)

            os.remove(f"emojis/{name}.{img_type}")
            if os.path.isfile(f"emojis/{name}_resized.{img_type}"):
                os.remove(f"emojis/{name}_resized.{img_type}")

        except discord.errors.Forbidden:
            await message.channel.send("I don't have the permissions for this!")
        except discord.errors.HTTPException:
            await message.channel.send("You've reached the maximum amount of emojis for this server!")
        except Exception as e:
            await error_log(message, e)
    else:
        await message.channel.send("Insufficient Permissions!!")


async def avatar(message):
    try:
        content = message.content.split()
        if len(content) == 1:
            user = message.author
        elif message.mentions:
            user = message.mentions[0]
        else:
            if not content[1].isdigit():
                await message.channel.send("Invalid ID! Use numbers only please")
                return
            elif len(str(content[1])) != 18:
                await message.channel.send("Invalid ID! It has to be exactly 18 digits long")
                return
            else:
                user = await bot.fetch_user(int(message.content.split()[1]))

        pfp = str(user.avatar_url).replace(".webp", ".png")
        desc = f"*{user.name}'s avatar*"
        embed = discord.Embed(description=desc, color=0xce3a9b)
        embed.set_image(url=pfp)
        await message.channel.send(embed=embed)

    except discord.errors.NotFound:
        await message.channel.send("That's not a valid ID!")
    except Exception as e:
        await error_log(message, e)


async def server_icon(message):
    try:
        server = message.guild
        icon = str(server.icon_url).replace(".webp", ".png")
        desc = f"*{server.name}'s icon*"

        await download_url(icon, f"files/{server.id}.png")

        img = Image.open(f"files/{server.id}.png")

        embed = discord.Embed(description=desc, color=0xce3a9b)

        if int(img.size[0]) <= 512:
            await pillow.resize(f"files/{server.id}.png", 1024, f"files/{server.id}_resized.png")
            file = discord.File(f"files/{server.id}_resized.png", filename="image.png")

            embed.set_image(url="attachment://image.png")
            await message.channel.send(file=file, embed=embed)
            file.close()

        else:
            embed.set_image(url=server.icon_url)
            await message.channel.send(embed=embed)

        img.close()
        os.remove(f"files/{server.id}.png")
        if os.path.isfile(f"files/{server.id}_resized.png"):
            os.remove(f"files/{server.id}_resized.png")

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

        if len(message.content.split()) == 1:
            await message.channel.send("Make sure you enter a valid word to search for!")
            return

        if message.content.split()[1] in ["random", 'rand', 'r']:
            defs = client.get_random_definition()
        else:
            urban_word = " ".join(message.content.split()[1:])
            defs = client.get_definition(urban_word)[:5]

        defs_sliced = list(reversed(sorted(defs, key=lambda x: x.upvotes)))

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
            if emoji == "\u2B05" and 0 < i <= 4:
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
    except asyncio.TimeoutError:
        return
    except Exception as e:
        await error_log(message, e)


async def calc(message):
    try:
        cmd = " ".join(x for x in message.content.split()[1:])
        if all(x in "0123456789+-*%/(). " for x in cmd):
            rslt = eval(cmd)
            await message.channel.send(round(rslt, 3))
        else:
            return
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
