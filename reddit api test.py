import discord
import praw
import random
from discord.ext import commands



client = commands.Bot(command_prefix='?')
reddit = praw.Reddit(client_id='ra7W9w_QZhwRaA',
                     client_secret='DFRuha1D_QLYm-AdCfQW54uiq1M',
                     user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36')

@client.command
async def cmd_test(cmd, message):
    if not indev_bool:
        return

    try:
        print('Im in!')
        neko_submissions = reddit.subreddit('Usagimimi').hot()
        print('Got bunny_submissions')
        counter = 0
        print('Getting first submission')
        submission = next(x for x in neko_submissions if not x.stickied)
        results = []

        while counter < 98:
            print('Inside while {}'.format(counter))
            submission = next(x for x in neko_submissions if not x.stickied)
            print('Got submission {}'.format(counter+1))
            counter += 1
            if not submission.over_18:
                print('PASSED IF')
                results.append(submission.url)
            print()
        if results:
            await client.send_message(message.channel, random.choice(results))
        else:
            await client.send_message(message.channel, 'No results found within the itteration limit!')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run('NjQxNDA5MzMwODg4ODM1MDgz.XcLHRQ.PvhkvwlbL0ZNU_cCccDxaiOnlCA')
