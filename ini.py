import discord

TOKEN = 'NjQxNDA5MzMwODg4ODM1MDgz.XcLHRQ.PvhkvwlbL0ZNU_cCccDxaiOnlCA'
BOT_PREFIX = "?"

client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('?hello'):
        msg = 'Hello {0.author.mention} !'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('who thinks annie is a great programmer?'):
        msg = 'I do! <@207505077013839883> is the **BEST** programmer!'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('?pat <@207505077013839883>'):
        msg = '*Timmy goes up to <@207505077013839883>, petting her and congratulating her on the test results*'.format(
            message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('?cuddle <@207505077013839883>'):
        msg = '*Timmy wraps his arms tightly around <@207505077013839883>, smiling as he feels her warm body*'.format(
            message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('hifumi?'):
        msg = 'Yes?'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('amirite hifumi?'):
        msg = "Yes, I'm just a prototype!".format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('do you like this place?'):
        msg = 'Absolutely! All these people here are amazing!'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('test'):
        msg = "Don't mind me, just trying out stuff <:slpylove:641673014030893069>".format(message)
        await client.send_message(message.channel, msg)

    await client.change_presence(game=discord.Game(name='with Sojiro'))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
