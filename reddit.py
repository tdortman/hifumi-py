import discord
import praw
import datetime
import random
import prawcore
from tools import error_log

reddit = praw.Reddit(client_id='ra7W9w_QZhwRaA',
                     client_secret='DFRuha1D_QLYm-AdCfQW54uiq1M',
                     user_agent='Mozilla/5.0')

# reddit caches
sub_cache_img = {}
sub_cache_text = {}


async def profile(message):
    try:
        user = reddit.redditor(message.content.split()[1])
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
        await message.channel.send(embed=embed)
    except AttributeError:
        await message.channel.send("Seems like this user is banned!")
    except prawcore.exceptions.NotFound:
        await message.channel.send("Invalid user! Make sure you typed the name correctly!")
    except Exception as e:
        await error_log(message, e)


async def sub(message, subreddit: str = None):
    try:
        name = subreddit
        if reddit.subreddit(name).over18 and not message.channel.is_nsfw():
            await message.channel.send("You can't access NSFW subreddits outside of NSFW channels!")
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
                await message.channel.send(
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
            await message.channel.send(embed=embed)
    except prawcore.exceptions.Redirect:
        await message.channel.send("That's not a valid subreddit!")
    except Exception as e:
        await error_log(message, e)


async def self_posts(message):
    try:
        name = message.content.split()[-1]
        if reddit.subreddit(name).over18 and not message.channel.is_nsfw():
            await message.channel.send("You can't access NSFW subreddits outside of NSFW channels!")
            return
        else:
            if name not in sub_cache_text:
                sub_cache_text[name] = []
                submissions = reddit.subreddit(name).hot()

                for i in range(100):
                    submission = next(x for x in submissions)
                    if submission.is_self and len(submission.selftext) <= 2048:
                        sub_cache_text[name].append((submission.url, submission.title, submission.selftext,
                                                     submission.score, submission.upvote_ratio, submission.author.name))

                submissions = reddit.subreddit(name).top('all')

                for i in range(100):
                    submission = next(x for x in submissions)
                    if submission.is_self and len(submission.selftext) <= 2048:
                        sub_cache_text[name].append((submission.url, submission.title, submission.selftext,
                                                     submission.score, submission.upvote_ratio, submission.author.name))
                await message.channel.send(f"Results found: {len(sub_cache_text[name])}")

            url, title, selftext, upvotes, ratio, author = random.choice(sub_cache_text[name])

            embed = discord.Embed(title=title, description=f"[Link to post by u/{author}]({url})\n\n{selftext}",
                                  color=0xce3a9b)
            embed.set_footer(text=f"Upvotes: {upvotes}  Ratio: {ratio * 100}%")
            await message.channel.send(embed=embed)
    except AttributeError:
        await self_posts(message)
    except Exception as e:
        await error_log(message, e)



