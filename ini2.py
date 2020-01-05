import datetime
import operator
import os
import random
import urllib
import urllib.request
import json
import discord
import praw
import qrcode
import urbandict
import youtube_dl
from discord.ext import commands
from discord.utils import get
import http.client
import requests as req

TOKEN = 'NjQxNDA5MzMwODg4ODM1MDgz.XcLHRQ.PvhkvwlbL0ZNU_cCccDxaiOnlCA'

bot = commands.Bot(command_prefix='h!')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    # await bot.change_presence("with Miku")


# reddit caches
kitsune_cache = []
wholesome_cache = []
bunny_cache = []
neko_cache = []
thighs_cache = []
animegirl_cache = []
sub_cache = {}

reddit = praw.Reddit(client_id='ra7W9w_QZhwRaA',
                     client_secret='DFRuha1D_QLYm-AdCfQW54uiq1M',
                     user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/78.0.3904.87 Safari/537.36')


# twitch = twitch.TwitchClient(client_id='xl1zs0f0n5h17htlilk9piwitkqtaw', oauth_token='NjQxNDA5MzMwODg4ODM1MDgz.Xd8LMw'
# '.QJXSOJ4jYV2ESYg8st7CW82OQTw')

@bot.command()
async def test1(ctx):
    await ctx.channel.send("Love you <@207505077013839883> :heart:\nLove you <@!207505077013839883> :heart:")


@bot.command()
async def avatar(ctx, member: discord.Member):
    embed = discord.Embed(title="", description="", color=0xce3a9b)
    embed.set_image(url=f"{member.avatar_url}")
    await ctx.send(embed=embed)


@bot.command()
async def leaveserver(server_id):
    to_leave = bot.get_guild(server_id)
    await to_leave.leave()


@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.3

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")


@bot.command()
async def urban(ctx, message):
    try:
        urban_list = []
        term = message
        word = urbandict.define(term)
        urban_list.append(word[0])
        embed = discord.Embed(title=urban_list[0]["word"], description=urban_list[0]["def"], color=0xce3a9b)

        await ctx.channel.send(embed=embed)
    except urllib.error.HTTPError:
        await ctx.channel.send("I'm sorry, but the definition is either not existent, or the server"
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
        print(operators[operation](int(num1), int(num2)))


@bot.command()
async def coinflip(ctx):
    rand_num = random.randint(0, 1)
    if rand_num == 0:
        await ctx.channel.send("Tails!")
    else:
        await ctx.channel.send("Heads!")


@bot.command()
async def cipher(ctx, message, key):
    now = datetime.datetime.now()
    current_time = now.strftime("%Y%m%d%H%M%S")
    source = message
    caesar = ""
    num = int(key)
    for i in range(len(source)):
        if source[i].isupper():
            caesar += chr(((ord(source[i]) - 65 + num) % 26) + 65)
        elif source[i].islower():
            caesar += chr(((ord(source[i]) - 97 + num) % 26) + 97)
        else:
            caesar += source[i]
        caesar = caesar.replace("_", " ")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=5,
        border=0,
    )
    qr.add_data(caesar)
    qr.make(fit=True)

    file_name = '{0}.png'.format(current_time[2:])
    img = qr.make_image(fill_color="black", back_color="white")

    img.save(r'/home/ubuntu/Hifumi/hifumi_cipher_images\{0}'.format(file_name))
    with open(r'/home/ubuntu/Hifumi/hifumi_cipher_images\{0}'.format(file_name), 'rb') as picture:
        await ctx.channel.send(file=discord.File(picture, "new_filename.png"))


@bot.command()
async def qr(ctx, message):
    m = message
    now = datetime.datetime.now()
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

    img.save(r'/home/ubuntu/HifuBot/hifumi_qr_code\{0}'.format(file_name))
    with open(r'/home/ubuntu/HifuBot/hifumi_qr_code\{0}'.format(file_name), 'rb') as picture:
        await ctx.channel.send(file=discord.File(picture, "new_filename.png"))


@bot.command()
async def test(ctx):
    await ctx.channel.send('Learning Python is fun uwu')


@bot.command()
async def cuddle(ctx, message):
    await ctx.channel.send(f"*{ctx.message.author.mention} goes up to {message} and cuddles tightly, "
                           "trying their best to comfort them*")


@bot.command()
async def kitsune(ctx):
    if not kitsune_cache:
        kitsune_submissions = reddit.subreddit('kitsunemimi').hot()

        for i in range(50):
            submission = next(x for x in kitsune_submissions)
            if not submission.over_18:
                kitsune_cache.append((submission.url, submission.title))

        kitsune_submissions = reddit.subreddit("kitsunemimi").top("all")

        for i in range(100):
            submission = next(x for x in kitsune_submissions)
            if not submission.over_18:
                kitsune_cache.append((submission.url, submission.title))

        await ctx.channel.send('Results found: {}'.format(len(kitsune_cache)))

    picture, name = random.choice(kitsune_cache)

    try:
        title, desc = name.split('[')
        desc = '[' + desc
    except ValueError:
        title = name
        desc = None

    embed = discord.Embed(title=title, description=desc, color=0xce3a9b)
    embed.set_image(url=picture)
    await ctx.channel.send(embed=embed)


@bot.command()
async def sub(ctx, message):
    global submission
    name = message.split()[0]
    with urllib.request.urlopen(f"https://www.reddit.com/r/{name}/about.json") as url:
        data = json.loads(url.read().decode())
        if ("over18", True) in data.items() and ctx.channel.is_nsfw():
            if name not in sub_cache:
                sub_cache[name] = []
                submissions = reddit.subreddit(name).hot()

                for i in range(100):
                    submission = next(x for x in submissions)
                    sub_cache[name].append((submission.url, submission.title))

                submissions = reddit.subreddit(name).top('all')

                for i in range(100):
                    submission = next(x for x in submissions)
                    sub_cache[name].append((submission.url, submission.title))
                await ctx.channel.send('Results found: {}'.format(len(sub_cache[name])))

            picture, name = random.choice(sub_cache[name])

            try:
                title, desc = name.split('[')
                desc = '[' + desc
            except ValueError:
                title = name
                desc = None

            embed = discord.Embed(title=title, description=desc, color=0xce3a9b)
            embed.set_image(url=picture)
            await ctx.channel.send(embed=embed)


@bot.command()
async def wholesome(ctx):
    if not wholesome_cache:
        wholesome_submissions = reddit.subreddit('wholesomeanimemes').hot()

        for i in range(50):
            submission = next(x for x in wholesome_submissions)
            if not submission.over_18:
                wholesome_cache.append((submission.url, submission.title))

        wholesome_submissions = reddit.subreddit("wholesomeanimemes").top("all")

        for i in range(100):
            submission = next(x for x in wholesome_submissions)
            if not submission.over_18:
                wholesome_cache.append((submission.url, submission.title))

        await ctx.channel.send('Results found: {}'.format(len(wholesome_cache)))

    picture, name = random.choice(wholesome_cache)

    try:
        title, desc = name.split('[')
        desc = '[' + desc
    except ValueError:
        title = name
        desc = None

    embed = discord.Embed(title=title, description=desc, color=0xce3a9b)
    embed.set_image(url=picture)
    await ctx.channel.send(embed=embed)


@bot.command()
async def bunny(ctx):
    if not bunny_cache:
        bunny_submissions = reddit.subreddit('usagimimi').hot()

        for i in range(100):
            submission = next(x for x in bunny_submissions)
            if not submission.over_18:
                bunny_cache.append((submission.url, submission.title))

        bunny_submissions = reddit.subreddit("usagimimi").top("all")

        for i in range(100):
            submission = next(x for x in bunny_submissions)
            if not submission.over_18:
                animegirl_cache.append((submission.url, submission.title))

        await ctx.channel.send('Results found: {}'.format(len(bunny_cache)))

    picture, name = random.choice(bunny_cache)

    try:
        title, desc = name.split('[')
        desc = '[' + desc
    except ValueError:
        title = name
        desc = None

    embed = discord.Embed(title=title, description=desc, color=0xce3a9b)
    embed.set_image(url=picture)
    await ctx.channel.send(embed=embed)


@bot.command(pass_context=True)
async def neko(ctx):
    if ctx.channel.is_nsfw():
        if not neko_cache:
            neko_submissions = reddit.subreddit('nekomimi').hot()

            for i in range(50):
                submission = next(x for x in neko_submissions)
                if submission.over_18:
                    neko_cache.append((submission.url, submission.title))

            neko_submissions = reddit.subreddit("nekomimi").top("all")

            for i in range(100):
                submission = next(x for x in neko_submissions)
                if submission.over_18:
                    neko_cache.append((submission.url, submission.title))

            await ctx.channel.send('Results found: {}'.format(len(neko_cache)))

        picture, name = random.choice(neko_cache)
        try:
            title, desc = name.split('[')
            desc = '[' + desc
        except ValueError:
            title = name
            desc = None

        embed = discord.Embed(title=title, description=desc, color=0xce3a9b)
        embed.set_image(url=picture)
        await ctx.channel.send(embed=embed)


@bot.command(pass_context=True)
async def thicc(ctx):
    if ctx.channel.is_nsfw():
        if not thighs_cache:
            thighs_submissions = reddit.subreddit('thighdeology').hot()

            for i in range(50):
                submission = next(x for x in thighs_submissions)
                if submission.over_18:
                    thighs_cache.append((submission.url, submission.title))

            thighs_submissions = reddit.subreddit("thighdeology").top("all")

            for i in range(100):
                submission = next(x for x in thighs_submissions)
                if submission.over_18:
                    thighs_cache.append((submission.url, submission.title))

            await ctx.channel.send('Results found: {}'.format(len(thighs_cache)))

        picture, name = random.choice(thighs_cache)

        try:
            title, desc = name.split('[')
            desc = '[' + desc
        except ValueError:
            title = name
            desc = None

        embed = discord.Embed(title=title, description=desc, color=0xce3a9b)
        embed.set_image(url=picture)
        await ctx.channel.send(embed=embed)


@bot.command(pass_context=True)
async def animegirl(ctx):
    if not animegirl_cache:
        animegirl_submissions = reddit.subreddit('animegirls').hot()

        for i in range(50):
            submission = next(x for x in animegirl_submissions)
            if not submission.over_18:
                animegirl_cache.append((submission.url, submission.title))

        animegirl_submissions = reddit.subreddit("animegirls").top("all")

        for i in range(100):
            submission = next(x for x in animegirl_submissions)
            if not submission.over_18:
                animegirl_cache.append((submission.url, submission.title))

        await ctx.channel.send('Results found: {}'.format(len(animegirl_cache)))

    picture, name = random.choice(animegirl_cache)

    try:
        title, desc = name.split('[')
        desc = '[' + desc
    except ValueError:
        title = name
        desc = None

    embed = discord.Embed(title=title, description=desc, color=0xce3a9b)
    embed.set_image(url=picture)
    await ctx.channel.send(embed=embed)


@bot.command(name='numguess',
             brief='Guess a number between 1 and 100')
async def numguess(message):
    number = random.randint(1, 100)
    turns = 5
    await message.channel.send("Welcome! Time to guess some numbers! You have 5 tries. I'll think"
                               " of a number between 1 and 100.")

    def check(author):
        def inner_check(message):
            if message.author != author:
                return False
            try:
                int(message.content)
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
                f"Woah there, this is way too high! Maybe try and guess a lower number next time."
                f" You still have {turns - 1} guesses left")
            turns -= 1
        elif guess < number and turns != 0:
            await message.channel.send(f"Awww, too bad! Might wanna go higher next time! You have {turns - 1} "
                                       f"guesses left!")
            turns -= 1
        if guess == number:
            await message.channel.send(f"Yes!! You guessed right! I'm so proud of you!!")
            break
        if guess == number and turns == 5:
            await message.channel.send("YOU'RE SO GOOD!!!! FIRST TRY!!")
            break
        if turns == 0 and guess != number:
            await message.channel.send(f"Maybe next time! In case you wondered, my number was {number}!")
            break


@bot.command()
async def test2(ctx, *args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await ctx.channel.send(output)


bot.run(TOKEN)
