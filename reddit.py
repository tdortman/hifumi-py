import discord
import asyncpraw
import asyncprawcore
import datetime
import random

from tools import *
from typing import *
import main

file = open(r"files/credentials.txt", "r")
lines = file.readlines()
REDDIT_CLIENT_ID = lines[5].split()[1]
REDDIT_CLIENT_SECRET = lines[6].split()[1]
file.close()

reddit = asyncpraw.Reddit(client_id=REDDIT_CLIENT_ID,
                          client_secret=REDDIT_CLIENT_SECRET,
                          user_agent='Mozilla/5.0')

# reddit caches & checks for fetch function
sub_cache_img = {}
sub_cache_text = {}
sub_running = False
self_posts_running = False
last_accessed = current_time()

bot = None


def get_client_var(client):
    global bot
    bot = client


async def profile(message):
    try:
        user = await reddit.redditor(message.content.split()[1], fetch=True)
        user_url = f"https://www.reddit.com/user/{user.name}"
        created_on = datetime.datetime.utcfromtimestamp(
            user.created_utc).strftime('%d/%m/%Y')

        desc = f"[Link to profile]({user_url})\n" \
               f"Post Karma: {user.link_karma}\n" \
               f"Comment Karma: {user.comment_karma}\n" \
               f"Created on: {created_on}\n"

        embed = discord.Embed(
            title=user.name,
            description=desc,
            color=main.EMBED_COLOUR)
        embed.set_thumbnail(url=user.icon_img)
        await message.channel.send(embed=embed)

    except AttributeError:
        await message.channel.send("Seems like this user is banned!")
    except asyncprawcore.exceptions.NotFound:
        await message.channel.send("Invalid user! Make sure you typed the name correctly!")
    except Exception as e:
        await error_log(message, e)


async def sub(message, subreddit: str = None):
    """
    Grabs image posts from a specified Subreddit and caches them for users to be able to
    Spam the command and look at what they want

    :param message: Default Discord Message Object (the Message that triggered the command)
    :param subreddit: Subreddit(s) to be accessed that allows for certain Subreddits to get their own "Command"
    :return: None
    """
    global sub_running, sub_cache_img, last_accessed
    try:
        sub_running = True
        sub_name = subreddit.lower()
        tmp_accessed = current_time()

        if last_accessed is not None:
            if tmp_accessed - last_accessed >= 3600:
                sub_cache_img = {}
                last_accessed = tmp_accessed

        if '+' in sub_name or len(message.content.split()) == 3:
            if '+' in sub_name:
                sub_name1 = sub_name.split('+')[0].lower()
                sub_name2 = sub_name.split('+')[1].lower()

                sub1 = await reddit.subreddit(sub_name1, fetch=True)
                sub2 = await reddit.subreddit(sub_name2, fetch=True)

            elif len(message.content.split()) == 3:
                sub_name1 = message.content.split()[1]
                sub_name2 = message.content.split()[2]

                sub1 = await reddit.subreddit(sub_name1, fetch=True)
                sub2 = await reddit.subreddit(sub_name2, fetch=True)

            if (sub1.over18 or sub2.over18) and not message.channel.is_nsfw():
                await message.channel.send("One of the subreddits you're trying to access contains NSFW material, "
                                           "please move into a NSFW channel!")
                return
            else:
                if len(sub_cache_img) == 10:
                    sub_cache_img = {}

                if sub_name1 not in sub_cache_img:
                    await fetch_submissions(sub_name1, limit=50)
                    await fetch_submissions(sub_name2, limit=50, name=sub_name1)
                    await message.channel.send(f'Results found: {len(sub_cache_img[sub_name1])}')

                picture, name = random.choice(sub_cache_img[sub_name1])

                try:
                    title, desc = name.split('[')
                    desc = '[' + desc
                except ValueError:
                    title = name
                    desc = None

                embed = discord.Embed(
                    title=title, description=desc, color=0xce3a9b)
                embed.set_image(url=picture)
                await message.channel.send(embed=embed)
        else:
            sub_img = await reddit.subreddit(sub_name, fetch=True)

            if sub_img.over18 and not message.channel.is_nsfw():
                await message.channel.send("You can't access NSFW subreddits outside of NSFW channels!")
                return
            else:
                if len(sub_cache_img) == 10:
                    sub_cache_img = {}

                if sub_name not in sub_cache_img:
                    await fetch_submissions(sub_name, 50)
                    await message.channel.send(f'Results found: {len(sub_cache_img[sub_name])}')

                picture, name = random.choice(sub_cache_img[sub_name])

                try:
                    title, desc = name.split('[')
                    desc = '[' + desc
                except ValueError:
                    title = name
                    desc = None

                embed = discord.Embed(
                    title=title, description=desc, color=main.EMBED_COLOUR)
                embed.set_image(url=picture)
                await message.channel.send(embed=embed)

            sub_running = False

    except asyncprawcore.exceptions.Redirect:
        await message.channel.send("That's not a valid subreddit!")
    except (asyncprawcore.exceptions.Forbidden, asyncprawcore.exceptions.NotFound):
        await message.channel.send("Seems like this subreddit is either set to private or has been suspended.")
    except (KeyError, IndexError):
        await message.channel.send("No images found")
    except Exception as e:
        await error_log(message, e)


async def self_posts(message, subreddit: str = None):
    global self_posts_running, sub_cache_text, last_accessed
    self_posts_running = True
    try:
        sub_name = subreddit.lower()
        tmp_accessed = current_time()

        if last_accessed is not None:
            if tmp_accessed - last_accessed >= 3600:
                sub_cache_text = {}
                last_accessed = tmp_accessed

        sub_txt = await reddit.subreddit(sub_name, fetch=True)

        if sub_txt.over18 and not message.channel.is_nsfw():
            await message.channel.send("You can't access NSFW subreddits outside of NSFW channels!")
            return
        else:
            if len(sub_cache_text) == 10:
                sub_cache_text = {}

            if sub_name not in sub_cache_text:
                await fetch_submissions(sub_name)
                await message.channel.send(f"Results found: {len(sub_cache_text[sub_name])}")

            url, title, selftext, upvotes, ratio, author = random.choice(
                sub_cache_text[sub_name])

            embed = discord.Embed(title=title, description=f"[Link to post by u/{author}]({url})\n\n{selftext}",
                                  color=main.EMBED_COLOUR)
            embed.set_footer(
                text=f"Upvotes: {upvotes}  Ratio: {adv_round(ratio * 100)}%")
            await message.channel.send(embed=embed)

        self_posts_running = False

    except AttributeError:
        await self_posts(message)
    except asyncprawcore.exceptions.Redirect:
        await message.channel.send("That's not a valid subreddit!")
    except asyncprawcore.exceptions.Forbidden:
        await message.channel.send("Seems like this subreddit is set to private.")
    except Exception as e:
        await error_log(message, e)


async def fetch_submissions(subreddit: str, limit: int = 100, name: Optional[str] = None):
    """
    Fetches Reddit posts from a specific subreddit into a dictionary
    So they can later be used for other commands

    :param subreddit: The name of the Subreddit that you want to fetch submissions from (new, hot and top of all time)
    :param limit: How many submissions should be fetched, defaults to 100 (300 total)
    :param name: Optional, in case you want to merge the submissions from two Subreddits into one list
    :return: None
    """
    global sub_running, self_posts_running

    sub_name = subreddit.lower()
    subreddit_obj = await reddit.subreddit(sub_name, fetch=True)

    if sub_running:
        sub_cache_img[sub_name] = []

        submissions = await reddit.subreddit(sub_name, fetch=True)
        submissions_list = submissions.new(limit=limit)

        async for submission in submissions_list:
            if submission.over_18 and not subreddit_obj.over18:
                continue
            elif submission.url.split("/")[2] in ["i.redd.it", "i.imgur.com"]:
                if name:
                    sub_cache_img[name].append(
                        (submission.url, submission.title))
                else:
                    sub_cache_img[sub_name].append(
                        (submission.url, submission.title))

        submissions = await reddit.subreddit(sub_name, fetch=True)
        submissions_list = submissions.hot(limit=limit)

        async for submission in submissions_list:
            if submission.over_18 and not subreddit_obj.over18:
                continue
            elif submission.url.split("/")[2] in ["i.redd.it", "i.imgur.com"]:
                if name:
                    sub_cache_img[name].append(
                        (submission.url, submission.title))
                else:
                    sub_cache_img[sub_name].append(
                        (submission.url, submission.title))

        submissions = await reddit.subreddit(sub_name, fetch=True)
        submissions_list = submissions.top('all', limit=limit)

        async for submission in submissions_list:
            if submission.over_18 and not subreddit_obj.over18:
                continue
            elif submission.url.split("/")[2] in ["i.redd.it", "i.imgur.com"]:
                if name:
                    sub_cache_img[name].append(
                        (submission.url, submission.title))
                else:
                    sub_cache_img[sub_name].append(
                        (submission.url, submission.title))

    elif self_posts_running:
        sub_cache_text[sub_name] = []

        submissions = await reddit.subreddit(sub_name, fetch=True)
        submissions_list = submissions.new(limit=limit)

        async for submission in submissions_list:
            if submission.over_18 and not subreddit_obj.over18:
                continue
            elif submission.is_self and len(submission.selftext) <= 2048:
                if name:
                    sub_cache_text[name].append((submission.url, submission.title, submission.selftext,
                                                 submission.score, submission.upvote_ratio, submission.author.name))
                else:
                    sub_cache_text[sub_name].append((submission.url, submission.title, submission.selftext,
                                                     submission.score, submission.upvote_ratio, submission.author.name))

        submissions = await reddit.subreddit(sub_name, fetch=True)
        submissions_list = submissions.hot(limit=limit)

        async for submission in submissions_list:
            if submission.over_18 and not subreddit_obj.over18:
                continue
            elif submission.is_self and len(submission.selftext) <= 2048:
                if name:
                    sub_cache_text[name].append((submission.url, submission.title, submission.selftext,
                                                 submission.score, submission.upvote_ratio, submission.author.name))
                else:
                    sub_cache_text[sub_name].append((submission.url, submission.title, submission.selftext,
                                                     submission.score, submission.upvote_ratio, submission.author.name))

        submissions = await reddit.subreddit(sub_name, fetch=True)
        submissions_list = submissions.top("all", limit=limit)

        async for submission in submissions_list:
            if submission.over_18 and not subreddit_obj.over18:
                continue
            elif submission.is_self and len(submission.selftext) <= 2048:
                if name:
                    sub_cache_text[name].append((submission.url, submission.title, submission.selftext,
                                                 submission.score, submission.upvote_ratio, submission.author.name))
                else:
                    sub_cache_text[sub_name].append((submission.url, submission.title, submission.selftext,
                                                     submission.score, submission.upvote_ratio, submission.author.name))
