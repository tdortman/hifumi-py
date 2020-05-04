import datetime
from discord.ext import commands
from importlib import reload
import discord
import main

bot = commands.Bot(command_prefix='h?')
now = datetime.datetime.now()

file = open(r'files/dev_token.txt', 'r')
TOKEN = file.readline()
file.close()


@bot.event
async def on_message(message):
    restart_shortcut = "hr~"
    if message.content.startswith(restart_shortcut):
        if message.author.id == 258993932262834188:
            try:
                reload(main)
                await main.reload_modules()
                msg = "Reload successful!"
            except Exception as e:
                msg = f"Reload failed!\n{e}"
            print(msg)
            await message.channel.send(msg)
        else:
            await message.channel.send("Insufficient Permissions!!")
    await bot.process_commands(message)


@bot.event
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    channel = await bot.fetch_channel(655484804405657642)
    time = now.strftime("%d/%m/%Y %H:%M:%S")
    # await channel.send(f"Logged in as:\n{bot.user.name}\nTime: {time}\n"
    # f"--------------------------")
    game = discord.Game("with best girl Annie!")
    await bot.change_presence(activity=game)

bot.run(TOKEN)
