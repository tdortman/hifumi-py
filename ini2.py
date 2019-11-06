from discord.ext import commands
import discord


TOKEN = 'NjQxNDA5MzMwODg4ODM1MDgz.XcLHRQ.PvhkvwlbL0ZNU_cCccDxaiOnlCA'

client = commands.Bot(command_prefix='?')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.command()
async def test():
    await client.say('Learning Python is fun uwu')


@client.command()
async def test2(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)

@client.event
async def on_message(message):
    author = message.author
    content = message.content
    print('{}: {}'.format(author, content))

client.run(TOKEN)
