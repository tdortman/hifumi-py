from datetime import datetime as dt
import traceback
import discord
import requests
import shutil
import time
import threading
import _thread
from typing import Union

bot = None


def get_client_var(client):
    global bot
    bot = client


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
                 "into your eyes._"],

    'lick': ["_Looks at you in a shock_  S-senpai..! W-what are y-you doing..??",
             "H-huh..? W-what did you do..? Eww..!  _Blushes and turns away._",
             "H-hey..! D-don't lick me! _Pouts a little, being shy and cute_",
             "S-senpai..! W-why would you l-lick me..? That is a very l-l-lewd thing to do..!",
             "N-no..! D-don't do this a-again, s-senpai..! _Looks at you cutely, wiping off the place you licked._"],

    'tickle': ["Aaah..! Ahahahah..! S-senpai.. Hehh.. Y-you can't do t-this to.. Ahahahh.. to me..! _Laughs as "
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


async def error_log(message=None, error_msg=None, cmd=None):
    """
    Error Log to be able to monitor the bot's status within discord and
    to be notified as soon as something goes wrong wrong.

    :param message: standard discord message object, needed to gain access to a lot of data
    :param error_msg: optional error message that can be passed as an argument for debugging purposes
    :param cmd: the specific command that triggered the error
    :return: None
    """
    now = dt.now()
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
    elif message.channel.id in [655484859405303809, 551588329003548683, 506834186540154890]:
        channel = message.channel
    else:
        channel = bot.get_channel(655484804405657642)

    try:
        await channel.send(msg)
    except discord.errors.HTTPException:
        await channel.send(f"An Error occurred on {current_time}\nCheck console for full error (2000 character limit)\n"
                           f"<@258993932262834188>")
        print(msg)


async def help_cmd(message):
    with open("files/help.txt") as f:
        msgs = [x for x in f.read().split("\n\n")]

    titles = ["**Hifumi's commands**", "**Reddit commands**"]

    for i in range(2):
        embed = discord.Embed(title=f"{titles[i]}", description=f"{msgs[i]}", colour=0xce3a9b)
        await message.channel.send(embed=embed)


async def download_attachments(message):
    """
    Checks a specific message and downloads the attachment when someone
    uploads something before sending it in the same channel

    :param message: discord message object
    :return: None
    """
    if message.attachments and not message.author.bot:
        for item in message.attachments:
            attach = await item.to_file(use_cached=True)
            await message.channel.send(file=attach)


async def download_url(url: str, save_location: str):
    """
    Makes a request and downloads whatever url you are passing
    as an argument

    :param url: the direct link to the object you want to download
    :param save_location: path to the location where you want your file to be saved
    :return: None
    """
    if "pximg" in url:
        r = requests.get(
            url, stream=True, headers={
                'User-agent': 'Mozilla/5.0',
                'Referer': "https://www.pixiv.net/"})
    else:
        r = requests.get(
            url, stream=True, headers={
                'User-agent': 'Mozilla/5.0'})

    with open(save_location, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)


def current_time():
    return int(time.time())


async def extract_emoji(emoji_str: str, id: bool = False) -> Union[int, str]:
    """
    Extracts the url of a specific emoji through its ID

    :param id: Optional parameter to directly pass an emoji's ID
    :param emoji_str: the string that contains the emoji (usually a string from a split message)
    :return: CDN asset of the emoji (url)
    """

    emoji_id = emoji_str.split(":")[2][:-1]

    if id:
        return int(emoji_id)

    if emoji_str[1] == "a":
        emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.gif"
    else:
        emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.png"
    return emoji_url


class timeout:
    def __init__(self, time):
        self.time = time
        self.exit = False

    def __enter__(self):
        threading.Thread(target=self.callme).start()

    def callme(self):
        time.sleep(self.time)
        if not self.exit:
            _thread.interrupt_main()

    def __exit__(self, a, b, c):
        self.exit = True


async def get_img_type(url: str) -> str:
    """
    Returns the file extension based on the image url

    :param url: url to the direct image that's to be analysed
    :return: returns the corresponding file extension to the image
    """
    if '.png' in url:
        return "png"
    elif '.jpg' in url or '.jpeg' in url:
        return 'jpg'
    elif '.bmp' in url:
        return 'bmp'
    elif '.gif' in url:
        return 'gif'


def adv_round(x: Union[int, float]) -> Union[int, float]:
    """
    Returns either int or float of original number, depending if it
    contains floating-point part or not
    """
    return int(x) if x // 1 + x % 1 == int(x) else round(x, 8)
