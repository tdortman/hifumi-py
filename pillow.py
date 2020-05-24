from PIL import Image
import requests
import shutil
import discord
import os
from tools import error_log

bot = discord.Client()


async def beautiful(message):
    try:
        beautiful_img = Image.open('files/background.png', 'r')
        if message.mentions:
            user = message.mentions[0]
        else:
            user = await bot.fetch_user(int(message.content.split()[1]))

        user_avatar = str(user.avatar_url).replace("webp", "png")
        r = requests.get(
            user_avatar, stream=True, headers={
                'User-agent': 'Mozilla/5.0'})
        with open(f"files/{user.id}.png", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

        basewidth = 180
        img = Image.open(f"files/{user.id}.png")
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save(f'files/{user.id}_resized.png')

        canvas = Image.new("RGBA", (640, 674))
        canvas.paste(img, (422, 35))
        canvas.paste(img, (430, 377))
        canvas.paste(beautiful_img, None, beautiful_img)
        canvas.save(f"files/beautiful.png")

        with open(f"files/beautiful.png", "rb") as g:
            picture = discord.File(g)
            await message.channel.send(file=picture)

        os.remove(f"files/{user.id}.png")
        os.remove(f"files/{user.id}_resized.png")
        os.remove(f"files/beautiful.png")
    except ValueError:
        await message.channel.send("Invalid ID! Use numbers only please!")
    except IndexError:
        await message.channel.send("Seems like you didn't mention anyone!")
    except discord.errors.NotFound:
        await message.channel.send("That's not a valid ID!")
    except Exception as e:
        await error_log(message, e)

