from discord.ext import commands

bot = commands.Bot(command_prefix="h?")


@bot.command()
async def caeser_cipher(ctx):
    content = ctx.message.content.split()
    sliced_msg = ' '.join(x for x in content[1:-1])
    num = int(content[-1])
    caesar = "".join(encrypt_letter(x, num) for x in sliced_msg)

    await ctx.channel.send(caesar)


def encrypt_letter(letter, num):
    if letter.isupper():
        return chr(((ord(letter) - 65 + num) % 26) + 65)
    elif letter.islower():
        return chr(((ord(letter) - 97 + num) % 26) + 97)
    else:
        return letter