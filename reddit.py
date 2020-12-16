import praw
import datetime
import random
import prawcore
from tools import *
from typing import *

file = open(r"files/credentials.txt", "r")
lines = file.readlines()
REDDIT_CLIENT_ID = lines[5].split()[1]
REDDIT_CLIENT_SECRET = lines[6].split()[1]
file.close()

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent='Mozilla/5.0')

# reddit caches & checks for fetch function
sub_cache_img = {}
sub_cache_text = {}
sub_running = False
self_posts_running = False


async def profile(message):
    try:
        user = reddit.redditor(message.content.split()[1])
        user_url = f"https://www.reddit.com/user/{user.name}"
        created_on = datetime.datetime.utcfromtimestamp(user.created_utc).strftime('%d/%m/%Y')

        desc = f"[Link to profile]({user_url})\n" \
               f"Post Karma: {user.link_karma}\n" \
               f"Comment Karma: {user.comment_karma}\n" \
               f"Created on: {created_on}\n"

        embed = discord.Embed(
            title=user.name,
            description=desc,
            color=0xce3a9b)
        embed.set_thumbnail(url=user.icon_img)
        await message.channel.send(embed=embed)

    except AttributeError:
        await message.channel.send("Seems like this user is banned!")
    except prawcore.exceptions.NotFound:
        await message.channel.send("Invalid user! Make sure you typed the name correctly!")
    except Exception as e:
        await error_log(message, e)


async def sub(message, subreddit: str = None):
    """
    Grabs image posts from a specified Subreddit and caches them for users to be able to
    Spam the command and look at what they want

    :param message: Default Discord Message Object (the Message that triggered the command)
    :param subreddit: Subreddit to be accessed that allows for certain Subreddits to get their own "Command"
    :return: None
    """
    global sub_running
    try:
        sub_running = True
        if subreddit:
            sub_name = subreddit
        else:
            sub_name = message.content.split()[1].lower()

        if '+' in sub_name or len(message.content.split()) == 3:
            if '+' in sub_name:
                sub_name1 = sub_name.split('+')[0].lower()
                sub_name2 = sub_name.split('+')[1].lower()

            elif len(message.content.split()) == 3:
                sub_name1 = message.content.split()[1]
                sub_name2 = message.content.split()[2]

            if (reddit.subreddit(sub_name1).over18 or reddit.subreddit(sub_name2).over18) and \
                    not message.channel.is_nsfw():
                await message.channel.send("One of the subreddits you're trying to access contains NSFW material, "
                                           "please move into a NSFW channel!")
                return
            else:
                if sub_name1 not in sub_cache_img:
                    fetch_submissions(sub_name1, limit=50)
                    fetch_submissions(sub_name2, limit=50, name=sub_name1)
                    await message.channel.send(f'Results found: {len(sub_cache_img[sub_name1])}')

                    picture, name = random.choice(sub_cache_img[sub_name1])

                    try:
                        title, desc = name.split('[')
                        desc = '[' + desc
                    except ValueError:
                        title = name
                        desc = None

                    embed = discord.Embed(title=title, description=desc, color=0xce3a9b)
                    embed.set_image(url=picture)
                    await message.channel.send(embed=embed)
        else:
            if reddit.subreddit(sub_name).over18 and not message.channel.is_nsfw():
                await message.channel.send("You can't access NSFW subreddits outside of NSFW channels!")
                return
            else:
                if sub_name not in sub_cache_img:
                    fetch_submissions(sub_name, 50)
                    await message.channel.send(f'Results found: {len(sub_cache_img[sub_name])}')

                picture, name = random.choice(sub_cache_img[sub_name])

                try:
                    title, desc = name.split('[')
                    desc = '[' + desc
                except ValueError:
                    title = name
                    desc = None

                embed = discord.Embed(title=title, description=desc, color=0xce3a9b)
                embed.set_image(url=picture)
                await message.channel.send(embed=embed)

    except prawcore.exceptions.Redirect:
        await message.channel.send("That's not a valid subreddit!")
    except (prawcore.exceptions.Forbidden, prawcore.exceptions.NotFound):
        await message.channel.send("Seems like this subreddit is either set to private or has been suspended.")
    except (KeyError, IndexError):
        await message.channel.send("No images found.")
    except Exception as e:
        await error_log(message, e)


async def self_posts(message, subreddit: str = None):
    global self_posts_running
    self_posts_running = True
    try:
        if subreddit:
            sub_name = subreddit
        else:
            sub_name = message.content.split()[2].lower()

        if reddit.subreddit(sub_name).over18 and not message.channel.is_nsfw():
            await message.channel.send("You can't access NSFW subreddits outside of NSFW channels!")
            return
        else:
            if sub_name not in sub_cache_text:
                fetch_submissions(sub_name)
                await message.channel.send(f"Results found: {len(sub_cache_text[sub_name])}")

            url, title, selftext, upvotes, ratio, author = random.choice(sub_cache_text[sub_name])

            embed = discord.Embed(title=title, description=f"[Link to post by u/{author}]({url})\n\n{selftext}",
                                  color=0xce3a9b)
            embed.set_footer(text=f"Upvotes: {upvotes}  Ratio: {adv_round(ratio * 100)}%")
            await message.channel.send(embed=embed)

    except AttributeError:
        await self_posts(message)
    except prawcore.exceptions.Redirect:
        await message.channel.send("That's not a valid subreddit!")
    except prawcore.exceptions.Forbidden:
        await message.channel.send("Seems like this subreddit is set to private.")
    except Exception as e:
        await error_log(message, e)


def fetch_submissions(subreddit: str, limit: int = 100, name: Optional[str] = None):
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

    if sub_running:
        sub_cache_img[sub_name] = []

        submissions = list(reddit.subreddit(sub_name).new(limit=limit))

        for submission in submissions:
            if submission.over_18 and not reddit.subreddit(sub_name).over18:
                continue
            elif submission.url.split("/")[2] in ["i.redd.it", "i.imgur.com"]:
                if name:
                    sub_cache_img[name].append((submission.url, submission.title))
                else:
                    sub_cache_img[sub_name].append((submission.url, submission.title))

        submissions = list(reddit.subreddit(sub_name).hot(limit=limit))

        for submission in submissions:
            if submission.over_18 and not reddit.subreddit(sub_name).over18:
                continue
            elif submission.url.split("/")[2] in ["i.redd.it", "i.imgur.com"]:
                if name:
                    sub_cache_img[name].append((submission.url, submission.title))
                else:
                    sub_cache_img[sub_name].append((submission.url, submission.title))

        submissions = list(reddit.subreddit(sub_name).top('all', limit=limit))

        for submission in submissions:
            if submission.over_18 and not reddit.subreddit(sub_name).over18:
                continue
            elif submission.url.split("/")[2] in ["i.redd.it", "i.imgur.com"]:
                if name:
                    sub_cache_img[name].append((submission.url, submission.title))
                else:
                    sub_cache_img[sub_name].append((submission.url, submission.title))

    elif self_posts_running:
        sub_cache_text[sub_name] = []

        submissions = list(reddit.subreddit(sub_name).new(limit=limit))

        for submission in submissions:
            if submission.over_18 and not reddit.subreddit(sub_name).over18:
                continue
            elif submission.is_self and len(submission.selftext) <= 2048:
                if name:
                    sub_cache_text[name].append((submission.url, submission.title, submission.selftext,
                                                 submission.score, submission.upvote_ratio, submission.author.name))
                else:
                    sub_cache_text[sub_name].append((submission.url, submission.title, submission.selftext,
                                                     submission.score, submission.upvote_ratio, submission.author.name))

        submissions = list(reddit.subreddit(sub_name).hot(limit=limit))

        for submission in submissions:
            if submission.over_18 and not reddit.subreddit(sub_name).over18:
                continue
            elif submission.is_self and len(submission.selftext) <= 2048:
                if name:
                    sub_cache_text[name].append((submission.url, submission.title, submission.selftext,
                                                 submission.score, submission.upvote_ratio, submission.author.name))
                else:
                    sub_cache_text[sub_name].append((submission.url, submission.title, submission.selftext,
                                                     submission.score, submission.upvote_ratio, submission.author.name))

        submissions = list(reddit.subreddit(sub_name).top("all", limit=limit))

        for submission in submissions:
            if submission.over_18 and not reddit.subreddit(sub_name).over18:
                continue
            elif submission.is_self and len(submission.selftext) <= 2048:
                if name:
                    sub_cache_text[name].append((submission.url, submission.title, submission.selftext,
                                                 submission.score, submission.upvote_ratio, submission.author.name))
                else:
                    sub_cache_text[sub_name].append((submission.url, submission.title, submission.selftext,
                                                     submission.score, submission.upvote_ratio, submission.author.name))
