from discord.ext import commands
import discord
import praw
import random
import base64
import datetime
from PIL import Image, ImageDraw
import math

TOKEN = 'NjQxNDA5MzMwODg4ODM1MDgz.XcLHRQ.PvhkvwlbL0ZNU_cCccDxaiOnlCA'

bot = commands.Bot(command_prefix='h!')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    # await bot.change_presence("with Miku")

@bot.command()
async def cipher(ctx, message):
        source = str(message)[7:]
        now = datetime.datetime.now()
        current_time = now.strftime("%Y%m%d%H%M%S")

        debug = False

        change, caesar = 55, ''
        for i in range(len(source)):
            char = ord(source[i])
            if 65 <= char <= 90:
                char += change
                while char > 90:
                    char -= 26
                while char < 65:
                    char += 26
            elif 97 <= char <= 122:
                char += change
                while char > 122:
                    char -= 26
                while char < 97:
                    char += 26
            caesar += chr(char)

        base1 = base64.b64encode(caesar.encode('ascii')).decode('ascii')
        base2 = base64.b64encode(base1.encode('ascii')).decode('ascii')

        binary = ''.join('{0:08b}'.format(ord(x), 'b') for x in base2)

        a = binary

        count = int(math.sqrt(len(a))) + 1
        cl = len(a)
        much = (count ** 2) - cl
        a = a + '0' * much

        img = Image.new('RGB', (count, count), 'black')
        pixels = img.load()

        k = int(0)

        for i in range(count):
            for j in range(count):
                if str(a[k]) == '0':
                    pixels[j, i] = (0, 0, 0)
                else:
                    pixels[j, i] = (255, 255, 255)
                k += 1

        file_name = '{0}{1}_{2}.png'.format(current_time[2:], change % 26, count)


        img.save(r'C:\Users\timdo\Desktop\HifuBot\hifumi_cipher_images\{0}'.format(file_name))
        with open(r'C:\Users\timdo\Desktop\HifuBot\hifumi_cipher_images\{0}'.format(file_name), 'rb') as picture:
            await ctx.channel.send(file=discord.File(picture, "new_filename.png"))





@bot.command()
async def test(ctx):
    await ctx.channel.send('Learning Python is fun uwu')




@bot.command()
async def cuddle(ctx):
    await ctx.channel.send("*Timmy goes up to <@207505077013839883> and cuddles tightly, "
                           "trying his best to comfort her*")


reddit = praw.Reddit(client_id='ra7W9w_QZhwRaA',
                     client_secret='DFRuha1D_QLYm-AdCfQW54uiq1M',
                     user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/78.0.3904.87 Safari/537.36')

kitsune_cache = []


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

wholesome_cache = []
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


bunny_cache = []
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


neko_cache = []
@bot.command(pass_context=True)
async def neko(ctx):
    channel = bot.get_channel(478572251252391957)
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

        await channel.send('Results found: {}'.format(len(neko_cache)))

    picture, name = random.choice(neko_cache)
    try:
        title, desc = name.split('[')
        desc = '[' + desc
    except ValueError:
        title = name
        desc = None

    embed = discord.Embed(title=title, description=desc, color=0xce3a9b)
    embed.set_image(url=picture)
    await channel.send(embed=embed)


thighs_cache = []
@bot.command(pass_context=True)
async def thicc(ctx):
    channel = bot.get_channel(478572251252391957)
    if not thighs_cache:
        thighs_submissions = reddit.subreddit('thighdeology').hot()

        for i in range(50):
            submission = next(x for x in thighs_submissions)
            if submission.over_18:
                thighs_cache.append((submission.url, submission.title))

        thighs_submissions = reddit.subreddit("thighdeology").top("all")

        for i in range(100):
            submission = next(x for x in thighs_submissions)
            if not submission.over_18:
                thighs_cache.append((submission.url, submission.title))

        await channel.send('Results found: {}'.format(len(thighs_cache)))

    picture, name = random.choice(thighs_cache)

    try:
        title, desc = name.split('[')
        desc = '[' + desc
    except ValueError:
        title = name
        desc = None

    embed = discord.Embed(title=title, description=desc, color=0xce3a9b)
    embed.set_image(url=picture)
    await channel.send(embed=embed)


animegirl_cache = []
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
async def numguess(ctx):
    number = random.randint(1, 100)
    turns = 5
    await ctx.channel.send("Welcome! Time to guess some numbers! You have 5 tries. I'll think"
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
        await ctx.channel.send("Go try your luck and take a guess!")
        msg = await bot.wait_for("message", check=check, timeout=60)
        guess = int(msg.content)

        if guess > number and turns != 0:
            await ctx.channel.send(f"Woah there, this is way too high! Maybe try and guess a lower number next time."
                                   f" You still have {turns - 1} guesses left")
            turns -= 1
        elif guess < number and turns != 0:
            await ctx.channel.send(f"Awww, too bad! Might wanna go higher next time! You have {turns - 1} "
                                   f"guesses left!")
            turns -= 1
        if guess == number:
            await ctx.channel.send(f"Yes!! You guessed right! I'm so proud of you!!")
            break
        if guess == number and turns == 5:
            await ctx.channel.send("YOU'RE SO GOOD!!!! FIRST TRY!!")
            break
        if turns == 0 and guess != number:
            await ctx.channel.send(f"Maybe next time! In case you wondered, my number was {number}!")
            break


@bot.command()
async def test2(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await channel.send(output)


bot.run(TOKEN)
