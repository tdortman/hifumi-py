from datetime import datetime as dt
from importlib import reload
import discord
import main
import tools
import pillow

bot = discord.Client()

start_time = main.current_time()
main.passClientVar(bot)
tools.passClientVar(bot)
pillow.passClientVar(bot)


file = open(r"files/token.txt", "r")
TOKEN = file.readline()
file.close()


@bot.event
async def on_message(message):
    restart_shortcut = "hr~~~"
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
            await message.channel.send("Insufficient Permissions!")
    else:
        await main.message_in(message)


@bot.event
async def on_ready():
    time = dt.utcnow().strftime("%d/%m/%Y %H:%M:%S UTC")
    done_loading_time = main.current_time()

    print(f'Started up in {done_loading_time - start_time} seconds on {time} UTC')
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    channel = bot.get_channel(655484804405657642)
    await channel.send(f"Logged in as:\n{bot.user.name}\nTime: {time}\n"
                       f"--------------------------")
    game = discord.Game("with best girl Annie!")
    await bot.change_presence(activity=game)

bot.run(TOKEN)
