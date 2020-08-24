from PIL import Image
import requests
import shutil
import discord
import os
from imgurpython import ImgurClient
from tools import error_log
import pytesseract


bot = discord.Client()

client_id = 'e6520e1c5f89fea'
client_secret = '38894f326220d5f45e6d7b2adea5635408e6fe71'

im = ImgurClient(client_id, client_secret)


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

        img = await resize(f"files/{user.id}.png", 180, f'files/{user.id}_resized.png')

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


async def resize(file_location: str, width: int, save_location: str = None):
    img = Image.open(file_location)
    wpercent = (width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((width, hsize), Image.ANTIALIAS)

    if save_location:
        img.save(save_location)
    else:
        img.save(file_location)
    return img


async def resize_img(message):
    try:
        img_url = message.content.split()[1]
        width = int(message.content.split()[-1])

        r = requests.get(
            img_url, stream=True, headers={
                'User-agent': 'Mozilla/5.0'})

        with open(f"files/unknown.png", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

        await resize(f"files/unknown.png", width, f"files/unknown_resized.png")

        if os.stat("files/unknown_resized.png").st_size > 8000000:
            await message.channel.send("Your image is over 8MB big, try resizing it first.")
        else:
            with open(f"files/unknown_resized.png", "rb") as g:
                picture = discord.File(g)
                await message.channel.send(file=picture)

        os.remove("files/unknown.png")
        os.remove("files/unknown_resized.png")
    except Exception as e:
        await error_log(message, e)


async def imgur(message):
    img_url = message.content.split()[1]

    if 'jpg' in img_url:
        img_type = 'jpg'
    elif 'png' in img_url:
        img_type = 'png'
    elif 'gif' in img_url:
        img_type = 'gif'

    r = requests.get(
        img_url, stream=True, headers={
            'User-agent': 'Mozilla/5.0'})

    with open(f"files/imgur.{img_type}", 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

    if os.stat(f"files/imgur.{img_type}").st_size > 10000000:
        await message.channel.send("Your image is over 10MB big, try resizing it first.")
    else:
        img = im.upload_from_path(f"files/imgur.{img_type}")
        await message.channel.send(f"{img['link']}")

    os.remove(f"files/imgur.{img_type}")


async def download_from_url(url):
    r = requests.get(
        url, stream=True, headers={
            'User-agent': 'Mozilla/5.0'})

    with open(f"files/attachment.png", 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)


async def extract_string_image(message):
    await message.channel.send(pytesseract.image_to_string(Image.open('files/test.png')))


