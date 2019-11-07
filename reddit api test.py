import discord
import praw
import random
from discord.ext import commands



client = commands.Bot(command_prefix='?')

reddit = praw.Reddit(client_id='ra7W9w_QZhwRaA',
                     client_secret='DFRuha1D_QLYm-AdCfQW54uiq1M',
                     user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36')

@client.command(pass_context=True)
async def wholesome(ctx):
    wholesome_submissions = reddit.subreddit('wholesomeanimemes').hot()
    post_to_pick = random.randint(1, 20)
    for i in range(0, post_to_pick):
        submission = next(x for x in wholesome_submissions if not x.stickied)

    await client.send_message(ctx.message.channel, submission.url)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run('NjQxNDA5MzMwODg4ODM1MDgz.XcLHRQ.PvhkvwlbL0ZNU_cCccDxaiOnlCA')
