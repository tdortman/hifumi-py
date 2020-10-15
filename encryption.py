from tools import error_log


async def caeser_cipher(message):
    try:
        content = message.content.split()
        sliced_msg = ' '.join(x for x in content[1:-1])
        num = int(content[-1])
        caesar = "".join(encrypt_letter(x, num) for x in sliced_msg)

        await message.channel.send(caesar)
    except Exception as e:
        await error_log(message, e)


def encrypt_letter(letter, num):
    if letter.isupper():
        return chr(((ord(letter) - 65 + num) % 26) + 65)
    elif letter.islower():
        return chr(((ord(letter) - 97 + num) % 26) + 97)
    else:
        return letter




@bot.event
async def on_ready():
    time = dt.utcnow().strftime("%d/%m/%Y %H:%M:%S")
    done_loading_time = tools.current_time()

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