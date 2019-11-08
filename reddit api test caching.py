from functools import lru_cache
import discord
import praw
import random
from discord.ext import commands
from cachetools import cached, TTLCache
import requests
import requests_cache
requests_cache.install_cache('demo_cache')

client = commands.Bot(command_prefix='?')

reddit = praw.Reddit(client_id='ra7W9w_QZhwRaA',
                     client_secret='DFRuha1D_QLYm-AdCfQW54uiq1M',
                     user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36')


@client.command(pass_context=True)
async def wholesome(ctx):
    wholesome_submissions = reddit.subreddit('wholesomeanimemes').hot()
    post_to_pick = range(100)
    for i in range(100):
        submission = next(x for x in wholesome_submissions if not x.stickied)

    requests.get(submission.url)



print(client.cache_auth)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run('NjQxNDA5MzMwODg4ODM1MDgz.XcLHRQ.PvhkvwlbL0ZNU_cCccDxaiOnlCA')
