from datetime import datetime
import traceback
import discord

bot = None


def passClientVar(client):
    global bot
    bot = client


async def error_log(message=None, error_msg=None, cmd=None):
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")

    if cmd is None and message is not None:
        cmd = message.content.split()[0][2:]
    elif cmd is None:
        cmd = 'unknown, message missing'
    else:
        cmd = 'unknown'

    tb = str(traceback.format_exc())

    if message is None:
        msg = f"An Error occurred on {current_time}\n" \
              f"**Command used**: {cmd}\n" \
              f"Message data unavailable due to the error not being client-side!\n" \
              f"Error:\n{error_msg}\n\n**{tb}**\n<@258993932262834188>"
    else:
        msg = f"An Error occurred on {current_time}\n" \
              f'**Server:** {message.guild} - {message.guild.id}\n' \
              f'**Room:** {message.channel} - {message.channel.id}\n' \
              f'**User:** {message.author} - {message.author.id}\n' \
              f"**Command used**: {message.content}\n" \
              f"**Error**:\n{error_msg}\n\n**{tb}**\n<@258993932262834188>"

    if message is None:
        channel = bot.get_channel(655484804405657642)
    elif message.channel.id in [655484859405303809, 551588329003548683]:
        channel = message.channel
    else:
        channel = bot.get_channel(655484804405657642)

    try:
        await channel.send(msg)
    except discord.errors.HTTPException:
        await channel.send(f"An Error occurred on {current_time}\nCheck console for full error (2000 character limit)\n"
                           f"<@258993932262834188>")
        print(msg)


async def download_attachments(message):
    if message.attachments and not message.author.bot:
        for item in message.attachments:
            attach = await item.to_file(use_cached=True)
            await message.channel.send(file=attach)
