import discord
from discord.ext import commands
import praw
import datetime
import random

bot = commands.Bot(command_prefix='h?')

reddit = praw.Reddit(client_id='ra7W9w_QZhwRaA',
                     client_secret='DFRuha1D_QLYm-AdCfQW54uiq1M',
                     user_agent='Mozilla/5.0')

# reddit caches
kitsune_cache = []
wholesome_cache = []
bunny_cache = []
neko_cache = []
thighs_cache = []
animegirl_cache = []
sub_cache_img = {}
sub_cache_text = {}


@bot.command()
async def profile(ctx):
    try:
        user = reddit.redditor(ctx.message.content.split()[1])
        user_url = f"https://www.reddit.com/user/{user.name}"
        created_on = datetime.datetime.utcfromtimestamp(
            user.created_utc).strftime('%d/%m/%y')
        desc = f"[Link to profile]({user_url})\n" \
               f"Post Karma: {user.link_karma}\n" \
               f"Comment Karma: {user.comment_karma}\n" \
               f"Created on: {created_on}\n"

        embed = discord.Embed(
            title=user.name,
            description=desc,
            color=0xce3a9b)
        embed.set_thumbnail(url=user.icon_img)
        await ctx.send(embed=embed)
    except AttributeError:
        await ctx.send("Seems like this user is banned!")
    except Exception:
        await ctx.send("Invalid user! Make sure you typed the name correctly!")


@bot.command()
async def kitsune(ctx):
    if not kitsune_cache:
        kitsune_submissions = reddit.subreddit('kitsunemimi').hot()

        for i in range(50):
            submission = next(x for x in kitsune_submissions)
            if not submission.over_18 and submission.url.split(
                    "/")[2] == "i.redd.it":
                kitsune_cache.append((submission.url, submission.title))

        kitsune_submissions = reddit.subreddit("kitsunemimi").top("all")

        for i in range(100):
            submission = next(x for x in kitsune_submissions)
            if not submission.over_18 and submission.url.split(
                    "/")[2] == "i.redd.it":
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
async def sub(ctx):
    try:
        if ctx.message.content.split()[1] == "text":
            await self_posts(ctx)
        else:
            name = ctx.message.content.split()[1]
            if reddit.subreddit(name).over18 and not ctx.channel.is_nsfw():
                await ctx.send("You can't access NSFW subreddits outside of NSFW channels!")
                return
            else:
                if name not in sub_cache_img:
                    sub_cache_img[name] = []
                    submissions = reddit.subreddit(name).hot()

                    for i in range(100):
                        submission = next(x for x in submissions)
                        if submission.url.split("/")[2] == "i.redd.it":
                            sub_cache_img[name].append((submission.url, submission.title))

                    submissions = reddit.subreddit(name).top('all')

                    for i in range(100):
                        submission = next(x for x in submissions)
                        if submission.url.split("/")[2] == "i.redd.it":
                            sub_cache_img[name].append((submission.url, submission.title))
                    await ctx.channel.send(
                        'Results found: {}'.format(len(sub_cache_img[name])))

                picture, name = random.choice(sub_cache_img[name])

                try:
                    title, desc = name.split('[')
                    desc = '[' + desc
                except ValueError:
                    title = name
                    desc = None

                embed = discord.Embed(title=title, description=desc, color=0xce3a9b)
                embed.set_image(url=picture)
                await ctx.channel.send(embed=embed)
    except IndexError:
        await ctx.send("You didn't specify a subreddit!")


async def self_posts(ctx):
    name = ctx.message.content.split()[-1]
    if reddit.subreddit(name).over18 and not ctx.channel.is_nsfw():
        await ctx.send("You can't access NSFW subreddits outside of NSFW channels!")
        return
    else:
        if name not in sub_cache_text:
            sub_cache_text[name] = []
            submissions = reddit.subreddit(name).hot()

            for i in range(100):
                submission = next(x for x in submissions)
                if submission.is_self:
                    sub_cache_text[name].append((submission.url, submission.title, submission.selftext,
                                                 submission.score, submission.upvote_ratio, submission.author.name))

            submissions = reddit.subreddit(name).top('all')

            for i in range(100):
                submission = next(x for x in submissions)
                if submission.is_self:
                    sub_cache_text[name].append((submission.url, submission.title, submission.selftext,
                                                 submission.score, submission.upvote_ratio, submission.author.name))
            await ctx.channel.send(f"Results found: {len(sub_cache_text[name])}")

        url, title, selftext, upvotes, ratio, author = random.choice(sub_cache_text[name])

        embed = discord.Embed(title=title, description=f"[Link to post by u/{author}]({url})\n\n{selftext}", color=0xce3a9b)
        embed.set_footer(text=f"Upvotes: {upvotes}  Ratio: {ratio * 100}%")
        await ctx.send(embed=embed)


@bot.command()
async def wholesome(ctx):
    if not wholesome_cache:
        wholesome_submissions = reddit.subreddit('wholesomeanimemes').hot()

        for i in range(50):
            submission = next(x for x in wholesome_submissions)
            if not submission.over_18 and submission.url.split(
                    "/")[2] == "i.redd.it":
                wholesome_cache.append((submission.url, submission.title))

        wholesome_submissions = reddit.subreddit("wholesomeanimemes").top(
            "all")

        for i in range(100):
            submission = next(x for x in wholesome_submissions)
            if not submission.over_18 and submission.url.split(
                    "/")[2] == "i.redd.it":
                wholesome_cache.append((submission.url, submission.title))

        await ctx.channel.send(
            'Results found: {}'.format(len(wholesome_cache)))

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
            if not submission.over_18 and submission.url.split(
                    "/")[2] == "i.redd.it":
                bunny_cache.append((submission.url, submission.title))

        bunny_submissions = reddit.subreddit("usagimimi").top("all")

        for i in range(100):
            submission = next(x for x in bunny_submissions)
            if not submission.over_18 and submission.url.split(
                    "/")[2] == "i.redd.it":
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
                if submission.over_18 and submission.url.split(
                        "/")[2] == "i.redd.it":
                    neko_cache.append((submission.url, submission.title))

            neko_submissions = reddit.subreddit("nekomimi").top("all")

            for i in range(100):
                submission = next(x for x in neko_submissions)
                if submission.over_18 and submission.url.split(
                        "/")[2] == "i.redd.it":
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

    else:
        await ctx.channel.send(
            "You may not use this command outside of NSFW channels!")


@bot.command(pass_context=True)
async def thicc(ctx):
    if ctx.channel.is_nsfw():
        if not thighs_cache:
            thighs_submissions = reddit.subreddit('thighdeology').hot()

            for i in range(50):
                submission = next(x for x in thighs_submissions)
                if submission.over_18 and submission.url.split(
                        "/")[2] == "i.redd.it":
                    thighs_cache.append((submission.url, submission.title))

            thighs_submissions = reddit.subreddit("thighdeology").top("all")

            for i in range(100):
                submission = next(x for x in thighs_submissions)
                if submission.over_18 and submission.url.split(
                        "/")[2] == "i.redd.it":
                    thighs_cache.append((submission.url, submission.title))

            await ctx.channel.send(
                'Results found: {}'.format(len(thighs_cache)))

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

    else:
        await ctx.channel.send(
            "You may not use this command outside of NSFW channels!")


@bot.command(pass_context=True)
async def animegirl(ctx):
    if not animegirl_cache:
        animegirl_submissions = reddit.subreddit('animegirls').hot()

        for i in range(50):
            submission = next(x for x in animegirl_submissions)
            if not submission.over_18 and submission.url.split(
                    "/")[2] == "i.redd.it":
                animegirl_cache.append((submission.url, submission.title))

        animegirl_submissions = reddit.subreddit("animegirls").top("all")

        for i in range(100):
            submission = next(x for x in animegirl_submissions)
            if not submission.over_18 and submission.url.split(
                    "/")[2] == "i.redd.it":
                animegirl_cache.append((submission.url, submission.title))

        await ctx.channel.send(
            'Results found: {}'.format(len(animegirl_cache)))

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
