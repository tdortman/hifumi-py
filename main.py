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


bot_owner = 258993932262834188


async def message_in(message):
    try:
        content = message.content
        react_cmd = message.content.split()[0][1:]

        if content.startswith("h!"):
            cmd = content.split()[0][2:].lower()

            try:
                sub_cmd = content.split()[1].lower()
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
            if cmd == 'tess':
                await pillow.extract_string_image(message)
            if cmd in ['currencies', 'currency', 'cur', 'cu']:
                await currency_codes(message)
            if cmd == 'test':
                pass

        elif content.startswith(f"${react_cmd} <@!641409330888835083>"):
            emote_msg = {
                'cuddle': ['cuddle', 'cuddles', 'cuddwe', 'cuddwes'],
                'hug': ['hug', 'hugs', 'hwug', 'hwugs'],
                'kiss': ['kiss', 'kisses', 'kwiss', 'kwisses'],
                'pat': ['pat', 'pet', 'pats', 'pets', 'pwat', 'pwet', 'pwats', 'pwets'],
                'snuggle': ['snuggle', 'snuggles', 'snuggwe', 'snuggwes'],
                'poke': ['poke', 'pokes', 'pwoke', 'pwokes'],
                'slap': ['slap', 'slaps'],
                'shy': ['shy', 'shies', 'shwy', 'shwies', 'shwiesh'],
                'handhold': ['handhold', 'handholds', 'handhowd', 'handhowds'],
                'lick': ['lick', 'licks', 'wick', 'wicks'],
                'tickle': ['tickle', 'tickles', 'tickwe', 'tickwes'],
                'cheekkiss': ['cheekkiss', 'kiss_cheek', 'kisscheek', 'kwisscheek', 'cheekkwiss', 'kwiss_cheek'],
                'boop': ['boop', 'boops', 'bwoop', 'bwoops'],
                'nuzzle': ['nuzzle', 'nuzzwe'],
                'huggle': ['huggle', 'huggles', 'huggwe', 'huggwes'],
                'smile': ['smile'],
                'hide': ['hide', 'hides', 'hwide', 'hwides'],
                'nibble': ['nibble', 'nibbles', 'nibbwe', 'nibbwes'],
                'flick': ["flick", "fwick"]
            }

            react_msg = {
                'cuddle': ['Ah, s-senpai, thank you for your c-cuddle..! _Smiles and  cuddles back._',
                           'Mmmm~ Senpai, thank chuu!~  _Smiles and cuddles {0} back._',
                           "_Rubs {0}'s back softly_  Your cuddles are always the b-best, senpai~",
                           "_Blushes and cuddles into {user} as well._ Cuddlesss for the best senpai!~ _Giggles._",
                           "_Cuddles back into {0}._ Mmm~  You must l-l-love m-me, s-senpai...!~"],

                'hug': ["Huggiess!~ _Giggles and hugs {0} back._",
                        "_Hugs and cuddles {0} back._  T-thank chu for a hug.. I needed it!~",
                        "_Smiles and nuzzle-hugs {0}._  Ah, I missed hugs from y-you, senpai!~",
                        "_Embraces {0} in a hug as well._  H-here, let m-me hug you b-back..!",
                        "H-huh..? Aaaah..!  S-senpai..! What an unexpected h-hug..! _Blushes._"],

                'kiss': ["_Blushes bright red._  S-senpai..! Y-you kissed me..!",
                         "_Blushes in a shock._  W-wha..? _Hides her face, shy._",
                         "S-senpai...! W-why you k-k-kiss... m-me..? _Looks away, embarrassed by your kiss._",
                         "H-huhh...? Aaaah~ S-senpai...! _Blushes and hides after {0}'s kiss._",
                         "_Blushes and kisses back, blushing afterwards._ D-don't tell anyone, o-okay..? _Smiles "
                         "cutely._"],

                'pat': ["_Looks at {0} confused._  W-what are you d-doing, s-senpai..?~",
                        "_Blushes and looks shily at {0}._  T-thank chu for a pat~",
                        "S-senpai~  _Giggles_  Thank you for a pat!!~",
                        "_Smiles at {0}._  Thank you~  _Giggles and smiles some more._",
                        "Ahhhh~ _Smiles happily,_  M-more, s-senpai...!~"],

                'snuggle': ["Snugglesss~  _Chuckles and snuggles back into {0}._",
                            "_Snuggles back into {0} with a blush and a smile_  Snuggles for my senpai!~",
                            "Awwh, senpai~  _Smiles and snuggles back._",
                            "T-thank you, senpai~  _Smiles and snuggles {0} softly._",
                            "Awwwwh, more, pwease..!~  _Snuggles softly into {0}._"],

                'poke': ["H-huh..? W-what do you n-need...? _Looks at you._",
                         "Oh, s-senpai..! Didn't notice you there..! Do you need anything? _Smiles at you._",
                         "Senpai..! _Smiles_  Do you need anything?~",
                         "_Jumps a little_  Y-yes..? W-what is it? Need something..? You could've just sent an E-Mail...",
                         "_Looks away for a moment before turning back to you_  Y-yes..? "],

                'slap': ["_Looks at you and runs away._",
                         "_Stares at you_  W-what did I do to y-you...  _Leaves._",
                         "W-what..? _Look at you confused about what just happened._ ",
                         "W-what...? W-why, s-senpai...? _Looks sad, tear rolling down her cheek._",
                         "Why would you...? _Looks at you through tear in her eyes._"],

                'shy': ["Ah, you cute little sweetheart~  _Smiles and huggles {0} softly._",
                        "_Wraps her arms around {0}_  Senpai~  What made you so shy?~",
                        "O-oh..? Is aught w-wrong, senpai..? _Smiles as you shy into her._",
                        "Hmm? What.. Oh, s-senpai..! _Looks a bit surprised and hugs you softly._",
                        "_Hugs you softly and shily._  S-senpai~ Why so shy?~ _Blushes._"],

                'handhold': ["_Holds your hand as well, blushing a little_.",
                             "Aaah, m-my hand..! _Blushes and looks away, shy._",
                             "S-senpai..? W-what are you doing? This is n-not really a-appropriate.. _Blushes._",
                             "_Smiles at you as you hold her hand_  S-senpai, we s-shouldn't...",
                             "_Jumps a little as you touched her hand_  H-huh.. oh.. you are... _Blushes and stares "
                             "into your "
                             "eyes._"],

                'lick': ["_Looks at you in a shock_  S-senpai..! W-what are y-you doing..??",
                         "H-huh..? W-what did you do..? Eww..!  _Blushes and turns away._",
                         "H-hey..! D-don't lick me! _Pouts a little, being shy and cute_",
                         "S-senpai..! W-why would you l-lick me..? That is a very l-l-lewd thing to do..!",
                         "N-no..! D-don't do this a-again, s-senpai..! _Looks at you cutely, wiping off the place you "
                         "licked._"],

                'tickle': [
                    "Aaah..! Ahahahah..! S-senpai.. Hehh.. Y-you can't do t-this to.. Ahahahh.. to me..! _Laughs as "
                    "you tickle her._",
                    "N-nooo..! _Giggles_  S-senpai..! T-that is e-enough.. Aahhhahahh.. S-stoop it..! _Squirms around "
                    "as you tickle her relentlessly._",
                    "H-huh..? N-noo..! Ahahahah s-senpai..! P-please stoooop..! _Laughs uncontrollably_",
                    "O-oh, s-senpai.. N-nuh uh.. Aahahhah.. Noo..! S-stop.. _Giggles_  S-stop pwease..! Ahahahah..!",
                    "_Laughs happily, squirming around as you tickle her._  S-senpai.. Ahahahah.. s-stop pwease..! "],

                'cheekkiss': ["_Smiles and blushes cutely as you kiss her cheek._",
                              "Oh s-senpai~  _Smiles at you cutely, hugging you afterwards._",
                              "_Blushes as you kiss her cheek, kissing your cheek as well._",
                              "Awwh, t-thank you, senpai~  _Smiles cutely at you._",
                              "_Quickly leans to {0} and kisses their cheek as well._  T-there you go, s-senpai!~ _Smiles._"],

                'boop': ["H-huh..? _Looks at you confused as you booped her nose._",
                         "Uwa... W-what..? W-why..?  _Looks at you confused and embarrassed._",
                         "_Looks shily away as you booped her nose, turning her cute and embarrassed._",
                         "Hyaaan.. W-what was that..? S-senpai..! _Looks away, shy._  M-my nose..",
                         "S-senpai..! W-why would you... _Cuts off the sentence, looking away shily._"],

                'smile': ["_Smiles back at you._  Your smile is very nice today, s-senpai~",
                          "_Smiles back at {0}, cheeks going slightly red._",
                          "Oh, s-senpai~ _Returns the smile._",
                          "_Returns the smile with a slight blush._",
                          "What a s-sweet senpai you are~ _Smiles at {0}, blushing slightly as well._"],

                'nuzzle': ["Ah, s-senpai..! D-don't embarrass m-me.. _Blushes and hugs you as you nuzzle into her._",
                           "H-huh..? What are you doing, s-senpai..? Oh well, c-come here~  _Wraps her arms around you as you "
                           "nuzzle into her._",
                           "Hehe, senpai~  _Nuzzles back into you as well._  You always k-know what I n-need~",
                           "_Smiles and snuggles into you as you nuzzle into her._  Mmmm~  Senpai~",
                           "W-what's w-wrong..? W-why are you s-smiling at me..? _Asks in an embarrassed tone._"],

                'huggle': ["Ah, s-senpai~  _Giggles and smiles a little as she returns the huggle._",
                           "_Huggles you back, blushing a little_  Huggwes anytime f-for my s-senpai~",
                           "Uh-uhhh? S-senpai, w-what are you doing? Oh.. I s-see.. _Huggles {0} back, cuddling a little as "
                           "well~_",
                           "_Giggles._  Ah, senpai~  You're like a big child sometimes, you know that?~  _Huggles back~_",
                           "Senpai~ A-again?~ Ah well, c-come here~ _Huggles into you softly, stroking your back a little._"],

                'flick': ["Awww aw oh.. oh.. s-senpai..! _Holds her forehead after the flick._",
                          "Awwhh...! _She looks shy and embarrassed after you flicked her forehead._",
                          "_Holds her forehead, looking down in an embarrassment._",
                          "_Gasps in a surprise as you flick her forehead._  S-senpai..!",
                          "_Blushes in an embarrassment after you flick her forehead_  Nawww~ d-don't do thaaat!~"],

                'hide': ["_Giggles as you hide behind her._  It's okay, you're safe with me~",
                         "_Blushes as you hide behind her, standing still._  H-huh..? W-what is going on h-here..?",
                         "H-huh..? S-senpai..?  _Looks at you as you were hiding behind her._ W-what's wrong..?",
                         "_Gasps as she suddenly finds you behind her._  W-what is going on..?",
                         "W-what happened..? D-did Hazuki-senpai try to dress y-you in some w-weird clothes again..?"],

                'nibble': ["_Stares at you with a scared expression._  W-what are you d-doing, s-senpai..??",
                           "N-no s-senpai..! N-not there..! _Squirms as you nibble on her, making her blush_",
                           "_Gasps at your action._  S-senpai..! W-w-what are you d-doing..! N-not here..! Noo..",
                           "S-senpai, s-stoop..! I'm n-not your f-food..! _Looks away embarrassed._",
                           "H-huh..? S-senpai n-noo..! S-sojiro, p-protect me..! _Blushes brighly red._"]
            }

            print(react_cmd)
            for cmd_type in emote_msg:
                if react_cmd in emote_msg[cmd_type]:
                    msg = random.choice(react_msg[cmd_type])
                    print(msg)
                    await asyncio.sleep(1)
                    await message.channel.send(msg.format(message.author.name))

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


async def emoji(message):
    if message.author.guild_permissions.manage_emojis:
        try:
            content = message.content.split()
            name, url = content[1], content[2]
            print(len(name))
            if len(name) > 32:
                await message.channel.send("Don't you think that name is a bit too long?..")
                return
            elif len(name) < 2:
                await message.channel.send("That name is too short! Try again with a longer one")
                return

            print("Got past the check!")
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
                    img.save(f"emojis/{name}_resized.{img_type}")

                elif Path(f"emojis/{name}.{img_type}").stat().st_size > 256000 and img_type == "gif":
                    await pillow.resize_gif(message, f"emojis/{name}.{img_type}", f"emojis/{name}_resized.{img_type}",
                                            (128, 128))
                print("Successfully resized gif!")

                if Path(f"emojis/{name}_resized.{img_type}").stat().st_size > 256000 and img_type == "gif":
                    await message.channel.send("Even after being resized to 128px your gif is still too big.. ")
                    print(Path(f"emojis/{name}_resized.{img_type}").stat().st_size)

                with open(
                        f"emojis/{name}_resized.{img_type}", "rb") as picture:

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
            os.remove(f"emojis/{name}_resized.{img_type}")

        except discord.errors.Forbidden:
            await message.channel.send("I don't have the permissions for this!")
        except IndexError:
            await message.channel.send("You didn't specify a name for the emoji!")
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
