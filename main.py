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
import prawcore
from math import pi, sqrt, log, e
from functools import reduce
import reddit
import music
import encryption
import pillow
import tools

bot = None


def init_vars(client):
    global bot
    bot = client
    music.get_client_var(client)
    pillow.get_client_var(client)
    tools.get_client_var(client)
    reddit.get_client_var(client)


BOT_OWNER = 258993932262834188
EMBED_COLOUR = 0xce3a9b
vote_running = False
vote_list = {}
vote_yes = 0
vote_no = 0
vote_candidate = []

file = open(r"files/credentials.txt", "r")
lines = file.readlines()
OXFORD_APP_ID = lines[3].split()[1]
OXFORD_APP_KEY = lines[4].split()[1]
file.close()


async def message_in(message):
    global vote_yes, vote_no
    try:
        content = message.content.split()
        react_cmd = content[0][1:] if len(content) > 1 else None

        if message.content.lower().startswith("h!"):
            cmd = content[0][2:].lower()
            sub_cmd = content[1] if len(content) >= 2 else None

            if cmd == "beautiful":
                await pillow.beautiful(message)

            if cmd == "redditor":
                await reddit.profile(message)

            if cmd == "kitsune":
                await reddit.sub(message, "kitsunemimi+touchfluffytail")

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
                if sub_cmd in ['add', 'ad']:
                    await add_emoji(message)
                elif sub_cmd in ['delete', 'delet', 'del', 'remove']:
                    await remove_emoji(message)

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
                await urban(message)

            if cmd == "calc":
                await message.channel.send("Sorry, this command is currently unavailable!")

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
                await tools.error_log(message, "This is a test error!")

            if cmd == "resize":
                await pillow.resize_img(message)

            if cmd == 'imgur':
                await pillow.imgur(message)

            if cmd == 'tess':
                await pillow.extract_string_image(message)

            if cmd in ['currencies', 'currency', 'cur', 'cu']:
                await currency_codes(message)

            if cmd in ['commands', 'command', 'comm', 'com', 'help']:
                await tools.help_cmd(message)

            if cmd == 'py':
                await py_eval(message)

            if cmd == 'ping':
                await ping(message)

            if cmd == 'invite':
                await invite(message)

            if message.author.id == BOT_OWNER and cmd == "test":
                pass

            if cmd == "open":
                await toggle_votes(message, "on")

            if cmd == "close":
                await toggle_votes(message, "off")

        # Reactions for Miku's emotes
        elif message.content.startswith(f"${react_cmd} <@!641409330888835083>") or \
                message.content.startswith(f"${react_cmd} <@641409330888835083>"):

            for cmd_type in tools.emote_msg:
                if react_cmd in tools.emote_msg[cmd_type]:
                    msg = random.choice(tools.react_msg[cmd_type])
                    await asyncio.sleep(1)
                    await message.channel.send(msg.format(message.author.name))

        # Elite Weebs voting
        elif vote_running:
            if message.channel.id == 785238165799567410 and not message.author.bot:
                if content[-1].lower() == "yes" and message.author.name not in vote_list:
                    vote_yes += 1
                    vote_list[message.author.name] = "Yes"
                elif content[-1].lower() == "no" and message.author.name not in vote_list:
                    vote_no += 1
                    vote_list[message.author.name] = "No"
                await message.delete()

    except Exception as e:
        await tools.error_log(message, e)


async def reload_modules():
    reload(encryption)
    reload(music)
    reload(reddit)
    reload(pillow)
    reload(tools)


currencies = {
    'EUR': 'Euro', 'AED': 'Emirati Dirham', 'AUD': 'Australian Dollar', 'ARS': 'Argentine Peso',
    'BGN': 'Bulgarian lev', 'BRL': 'Brazilian Real', 'BSD': 'Bahamian Dollar', 'CAD': 'Canadian Dollar',
    'CHF': 'Swiss Franc', 'CLP': 'Chilean Peso', 'CNY': 'Chinese Yuzan', 'COP': 'Colombian Peso',
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


async def toggle_votes(message, mode: str, vote_name: str = None):
    if message.author.guild_permissions.kick_members:
        global vote_running, vote_list, vote_no, vote_yes, vote_candidate
        if vote_running and mode == "off":
            vote_running = False
            await message.channel.send("Voting closed now!")
            await show_vote_result()

            vote_running = True
            vote_list = {}
            vote_no = 0
            vote_yes = 0

        elif not vote_running and mode == "on":
            try:
                if vote_name:
                    if vote_name.startswith("u/"):
                        user = reddit.reddit.redditor(vote_name[2:])
                    else:
                        user = reddit.reddit.redditor(vote_name)
                else:
                    if message.content.split()[1].startswith("u/"):
                        user = reddit.reddit.redditor(message.content.split()[1][2:])
                    else:
                        user = reddit.reddit.redditor(message.content.split()[1])

                vote_candidate, id = [user.name, user.icon_img], user.id

            except prawcore.exceptions.NotFound:
                await message.channel.send("User not found! Make sure you enter the name correctly!")
                return

            vote_running = True
            vote_list = {}
            vote_no = 0
            vote_yes = 0
            await message.channel.send("Voting open now!")

        elif vote_running and mode == "on":
            await message.channel.send("You have to close the running voting before opening another one!")
        elif not vote_running and mode == "off":
            await message.channel.send("You have to start a voting using `h!open` before you can close it")
    else:
        return


async def show_vote_result():
    global vote_candidate

    channel = bot.get_channel(785351105240236042)

    raw_columns = [f"{k} voted **{vote_list[k]}**" for k in vote_list]
    columns = ["\n".join(line for line in raw_columns[0:int(round(len(raw_columns) / 2))]),
               "\n".join(line for line in raw_columns[int(round(len(raw_columns) / 2)):])]

    if vote_yes > vote_no:
        footer = f"{vote_yes} / {vote_no} -> APPROVED"
    elif vote_yes < vote_no:
        footer = f"{vote_yes} / {vote_no} -> REJECTED"
    elif vote_yes == vote_no:
        footer = f"{vote_yes} / {vote_no} -> TIEBREAKER"

    embed = discord.Embed(title=f"Vote Results for Candidate {vote_candidate[0]}", color=EMBED_COLOUR)
    for column in columns:
        embed.add_field(name='\u200b', value=column)
    embed.set_thumbnail(url=vote_candidate[1])
    embed.set_footer(text=footer)

    await channel.send(embed=embed)


async def invite(message):
    await message.channel.send("You can invite me using this link:\nhttps://discord.com/api/oauth2/authorize?"
                               "client_id=641409330888835083&permissions=8&scope=bot")


async def test_cmd3(message):
    search_term = message.content.split()[1].lower()

    endpoint = "entries"
    language_code = "en-gb"
    fields = "definitions,examples"

    url = f"https://od-api.oxforddictionaries.com/api/v2/{endpoint}/{language_code}/{search_term}?fields={fields}"
    r = requests.get(url, headers={"app_id": OXFORD_APP_ID, "app_key": OXFORD_APP_KEY})

    if r.status_code == 404:
        url = f"https://od-api.oxforddictionaries.com/api/v2/lemmas/{language_code}/{search_term}?fields={fields}"
        r = requests.get(url, headers={"app_id": OXFORD_APP_ID, "app_key": OXFORD_APP_KEY})

        search_term = r.json()['results'][0]['lexicalEntries'][0]['inflectionOf'][0]['text']

        url = f"https://od-api.oxforddictionaries.com/api/v2/{endpoint}/{language_code}/{search_term}?fields={fields}"
        r = requests.get(url, headers={"app_id": OXFORD_APP_ID, "app_key": OXFORD_APP_KEY})

        print(r.json())
        await message.channel.send(r.json())
        definition = r.json()['results'][0]["lexicalEntries"][0]['entries'][0]['senses'][0]['definitions'][0]
        await message.channel.send(r.status_code)
        await message.channel.send(f"{definition}")
    else:
        definition = r.json()['results'][0]["lexicalEntries"][0]['entries'][0]['senses'][0]['definitions'][0]
        example = r.json()['results'][0]["lexicalEntries"][0]['entries'][0]['senses'][0]['examples'][0]['text']
        print(r.json())
        await message.channel.send(r.status_code)
        await message.channel.send(f"{definition}\n\n{example}")


async def ping(message):
    latency = round(bot.latency * 1000)
    await message.channel.send(f"Latency: **{latency}ms**")


async def leave(message):
    server = bot.get_guild(int(message.content.split()[1]))
    await server.delete()
    await message.channel.send("left")


async def py_eval(message):
    try:
        content = message.content.split()
        if len(content) == 1:
            await message.channel.send("You have to type **SOMETHING** at least")
            return

        if message.author.id == BOT_OWNER:
            cmd = " ".join(x for x in message.content.split()[1:])
            rslt = eval(cmd)

            if not rslt:
                await message.channel.send("Cannot send an empty message!")
                return
            await message.channel.send(rslt)

        else:
            await message.channel.send("Insufficient permissions!")
    except Exception as e:
        await tools.error_log(message, e)


async def convert(message):
    try:
        content = message.content.split()
        if len(content) == 1:
            await message.channel.send("Usage: `h!convert <amount of money> <cur1> <cur2>`")
            return

        if not (content[1].isdigit() and content[2].upper() in currencies and content[3].upper() in currencies):
            await message.channel.send("Invalid Syntax! Usage: `h!convert <amount of money> <cur1> <cur2>`")
            return

        val, cur1, cur2 = float(content[1]), content[2].upper(), content[3].upper()

        # Make a request to the api, handle possible errors, extracts and checks conversion rates for specific currency
        url = f'https://prime.exchangerate-api.com/v5/81f453a13268228658567d13/latest/{cur1}'
        response = requests.get(url)
        result = response.json()

        if result['result'] == 'error':
            if result['error'] == 'unknown-code':
                await message.channel.send(f"{cur1} is not a valid currency code! Check h!currencies for a list of "
                                           f"available currency codes")
            else:
                await message.channel.send("An unknown error occurred! Please try again later!")
            return

        data = result['conversion_rates']

        if cur2 not in data:
            await message.channel.send(f"{cur2} is not a valid currency code!")
            return

        # Rounds the amount after conversion to 2 digits, description set to avoid .0 at the end since it's a float
        rslt = round(val * data[cur2], 2)
        desc = f"**{tools.adv_round(val)} {cur1} ≈ {tools.adv_round(rslt)} {cur2}**\n\n" \
               f"Exchange rate:\n1 {cur1} ≈ {data[cur2]} {cur2}"

        # Created Embed and send it in the channel
        embed = discord.Embed(description=desc, title=f"Converting {currencies[cur1]} into {currencies[cur2]}",
                              color=EMBED_COLOUR)
        embed.set_footer(text=f"{dt.utcnow().strftime('%d/%m/%Y %H:%M:%S')} UTC\nUse the command h!currencies for a "
                              f"list of currencies available for conversion")
        await message.channel.send(embed=embed)

    except Exception as e:
        await tools.error_log(message, e)


async def currency_codes(message):
    title = 'List of currencies available for conversion'
    columns = ["", "", ""]
    currency_keys = sorted(list(currencies))

    # Splits the currencies into 3 different columns
    # that then get added to an Embed as individual fields
    # and sent into the channel
    for i in range(len(currency_keys)):
        if i <= 16:
            columns[0] += str(f"**{currency_keys[i]}** - {currencies[str(currency_keys[i])]}\n")
        elif 17 <= i <= 33:
            columns[1] += str(f"**{currency_keys[i]}** - {currencies[str(currency_keys[i])]}\n")
        else:
            columns[2] += str(f"**{currency_keys[i]}** - {currencies[str(currency_keys[i])]}\n")

    embed = discord.Embed(title=title, color=EMBED_COLOUR)
    for i in range(3):
        embed.add_field(name='\u200b', value=columns[i])
    await message.channel.send(embed=embed)


async def add_emoji(message):
    if message.author.guild_permissions.manage_emojis:
        try:
            content = message.content.split()

            # Checks for all the possible wrong inputs possible
            if len(content) == 2:
                await message.channel.send("Usage: `h!emoji add <name> <url/emoji>`")
                return

            name = content[2]

            if name.startswith("<") or "http" in name:
                await message.channel.send("You didn't specify a name for the emoji!")
                return

            # Extracting url for the emoji based on the url/emoji given
            if content[3].startswith("<") and "http" not in content[3]:
                url = await tools.extract_emoji(content[3])
            elif 'http' in content[3] and "<>" in content[3]:
                url = content[3][1:-1]
            elif 'http' in content[3]:
                url = content[3]
            else:
                await message.channel.send("You didn't specify a url or emoji!")
                return

            # Emoji names have to be between 2 and 32 characters long
            if len(name) > 32:
                await message.channel.send("Don't you think that name is a bit too long?..")
                return
            elif len(name) < 2:
                await message.channel.send("That name is too short! Try again with a longer one")
                return

            img_type = await tools.get_img_type(url)

            await tools.download_url(url, f"emojis/{name}.{img_type}")

            # Checks cases when the image is too big (256KB) and proceeds to resize them to 128x128 when needed
            # Creates custom emoji with either the initial image or a resized version
            if Path(f"emojis/{name}.{img_type}").stat().st_size > 256000 and (img_type == "jpg" or img_type == "png"):

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

            # Sending the newly created emoji as confirmation
            if emoji and img_type != "gif":
                msg = f'<:{emoji.name}:{emoji.id}>'
            elif emoji and img_type == "gif":
                msg = f"<a:{emoji.name}:{emoji.id}>"
            else:
                msg = 'Emoji object not retrieved!'
            await message.channel.send(msg)

            # Deletes any leftover files
            os.remove(f"emojis/{name}.{img_type}")
            if os.path.isfile(f"emojis/{name}_resized.{img_type}"):
                os.remove(f"emojis/{name}_resized.{img_type}")

        except discord.errors.Forbidden:
            await message.channel.send("I don't have the permissions for this!")
        except discord.errors.HTTPException:
            await message.channel.send("You've reached the maximum amount of emojis for this server!")
        except Exception as e:
            await tools.error_log(message, e)
    else:
        await message.channel.send("Insufficient permissions. Make sure you have the `manage emojis` permission")


async def remove_emoji(message):
    if message.author.guild_permissions.manage_emojis:
        try:
            content = message.content.split()
            server = message.guild

            id = await tools.extract_emoji(content[2], True)
            emoji = await server.fetch_emoji(id)

            await emoji.delete()
            await message.channel.send('Emoji successfully deleted!')

        except discord.errors.NotFound:
            await message.channel.send("That emoji is not in this server <:emiliaSMH:747132102645907587>")
    else:
        await message.channel.send("Insufficient permissions. Make sure you have the `manage emojis` permission")


async def avatar(message):
    try:
        content = message.content.split()

        # Fetches User Object based on different scenarios
        if len(content) == 1:
            user = message.author
        elif message.mentions:
            user = message.mentions[0]
        else:
            if not content[1].isdigit():
                await message.channel.send("Invalid ID! Use numbers only please")
                return
            else:
                user = await bot.fetch_user(int(message.content.split()[1]))

        # Converts avatar image into a PNG, creates an Embed and sends it
        pfp = str(user.avatar_url).replace(".webp", ".png")
        desc = f"*{user.name}'s avatar*"
        embed = discord.Embed(description=desc, color=EMBED_COLOUR)
        embed.set_image(url=pfp)
        await message.channel.send(embed=embed)

    except discord.errors.NotFound:
        await message.channel.send("That's not a valid ID!")
    except Exception as e:
        await tools.error_log(message, e)


async def server_icon(message):
    try:
        # Retrieves server icon, downloads it, opens it and creates am Embed Object
        server = message.guild
        icon = str(server.icon_url).replace(".webp", ".png")
        desc = f"*{server.name}'s icon*"

        await tools.download_url(icon, f"files/{server.id}.png")

        img = Image.open(f"files/{server.id}.png")

        embed = discord.Embed(description=desc, color=EMBED_COLOUR)

        # Checks the icon's width, if it's under 512px it gets resized to 1024px width
        # (Resized) image gets added to the Embed and sent
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
        await tools.error_log(message, e)


async def bye(message):
    try:
        if message.author.id == 258993932262834188:
            await message.channel.send("Bai baaaaaaaai!!")
            await bot.logout()
    except Exception as e:
        await tools.error_log(message, e)


async def urban(message):
    try:
        client = UrbanClient()
        content = message.content.split()
        if len(content) == 1:
            await message.channel.send("Make sure you enter a valid word to search for!")
            return

        # Keyword to trigger random definitions defined, else the api gets called for
        # the search-term specified
        if content[1] in ["random", 'rand', 'r']:
            defs = client.get_random_definition()
        else:
            urban_word = " ".join(content[1:])
            defs = client.get_definition(urban_word)[:5]

        # Definitions sorted by the amount of upvotes so the first page has the most
        defs_sliced = list(reversed(sorted(defs, key=lambda x: x.upvotes)))

        # Loop for creating Embeds for every individual definition
        pages = []
        for i in range(5):
            desc = f"**Definition**:\n{str(defs_sliced[i].definition).replace('[', '').replace(']', '')}\n\n" \
                   f"**Example**:\n{defs_sliced[i].example.replace('[', '').replace(']', '')}"
            footer = f"Upvotes: {defs_sliced[i].upvotes}  Downvotes: {defs_sliced[i].downvotes}\nPage {i + 1}/5"

            page = discord.Embed(title=defs_sliced[i].word,
                                 description=desc,
                                 color=EMBED_COLOUR)
            page.set_footer(text=footer)
            pages.append(page)

        message = await message.channel.send(embed=pages[0])

        # Reactions added, Left Arrow and Right Arrow
        await message.add_reaction("\u2B05")
        await message.add_reaction("\u27A1")

        # Emoji handler to change the pages upon reacting
        # Needs to be reworked
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
        await tools.error_log(message, e)


async def calc(message):
    try:
        # Function is getting terminated after a second to avoid killing the bot
        with tools.timeout(1):
            if len(message.content.split()) == 1:
                await message.channel.send("You have to add numbers and expressions if you want to calculate something")
                return

            # Checks if anything in the message apart from the first word (command)
            # Isn't allowed to be used (Had to restrict it because it uses a very powerful
            # Function that allows for the bot's deletion
            start_time = tools.current_time()
            cmd = " ".join(x for x in message.content.split()[1:])
            if all(x in "0123456789+-*%/(). " for x in cmd):
                rslt = eval(cmd)

                if not rslt:
                    await message.channel.send("Cannot send an empty message!")
                    return
                await message.channel.send(round(tools.adv_round(rslt), 3))
            else:
                await message.channel.send("invalid characters")
                return

    except discord.errors.HTTPException:
        await message.channel.send("Overflow Error!")
    except OverflowError:
        await message.channel.send("Overflow Error!")
    except KeyboardInterrupt:
        end_time = tools.current_time()
        await message.channel.send(f"killed in {end_time - start_time} seconds")
    except ZeroDivisionError:
        await message.channel.send("DO. NOT. EVER. DIVIDE. BY. ZERO. OR. THE. UNIVERSE. WILL. IMPLODE.")
    except Exception as e:
        await tools.error_log(message, e)


async def coinflip(message):
    try:
        rand_num = random.randint(0, 1)
        if rand_num == 0:
            await message.channel.send("Tails!")
        else:
            await message.channel.send("Heads!")
    except Exception as e:
        await tools.error_log(message, e)


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
        await tools.error_log(message, e)


async def cuddle(message):
    try:
        target = message.mentions[0]
        await message.channel.send(
            f"*{message.author.mention} goes up to {target} and cuddles tightly, "
            "trying their best to comfort them*")
    except Exception as e:
        await tools.error_log(message, e)


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
        await tools.error_log(message, e)
