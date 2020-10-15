from PIL import Image
import requests
import shutil
import discord
import os
from imgurpython import ImgurClient
import pytesseract
import tools

bot = None


def get_client_var(client):
    global bot
    bot = client


CLIENT_ID = 'e6520e1c5f89fea'
CLIENT_SECRET = '38894f326220d5f45e6d7b2adea5635408e6fe71'


async def beautiful(message):
    try:
        content = message.content.split()
        background = Image.open('files/background.png', 'r')

        if len(content) == 1:
            await message.channel.send("Seems like you didn't mention anyone!")
            return
        elif not content[1].isdigit() and not message.mentions:
            await message.channel.send("Invalid ID! Use numbers only please")
            return

        if message.mentions:
            user = message.mentions[0]
        else:
            user = await bot.fetch_user(int(content[1]))

        user_avatar = str(user.avatar_url).replace("webp", "png")
        await tools.download_url(user_avatar, f"files/{user.id}.png")

        img = await resize(f"files/{user.id}.png", 180, f'files/{user.id}_resized.png')

        canvas = Image.new("RGBA", (640, 674))
        canvas.paste(img, (422, 35))
        canvas.paste(img, (430, 377))
        canvas.paste(background, None, background)
        canvas.save(f"files/beautiful.png")

        with open(f"files/beautiful.png", "rb") as g:
            picture = discord.File(g, "unknown.png")
            await message.channel.send(file=picture)

        os.remove(f"files/{user.id}.png")
        os.remove(f"files/{user.id}_resized.png")
        os.remove(f"files/beautiful.png")

    except discord.errors.NotFound:
        await message.channel.send("That's not a valid ID!")
    except Exception as e:
        await tools.error_log(message, e)


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


async def resize_img(message, url=None, img_width=None):
    try:
        content = message.content.split()

        if len(content) == 1:
            await message.channel.send("You specified neither the image nor the size you want to resize it to")
            return

        if not content[1].isdigit():
            await message.channel.send("You didn't specify a number!")
            return

        if img_width is not None:
            width = img_width
        else:
            width = int(content[1])

        if width >= 5000:
            await message.channel.send("Don't you think that's a bit too much?..")
            return

        if url is not None:
            img_url = url
        elif content[1].isdigit() and len(content) == 2:
            await message.channel.send("You also have to specify the image you want to resize!")
            return
        elif content[2].startswith("<:"):
            img_url = await tools.extract_emoji(content[2])
        elif "http" in content[2] and "<>" in content[2]:
            img_url = content[2][1:-1]
        else:
            img_url = content[2]

        img_type = await tools.get_img_type(img_url)

        await tools.download_url(img_url, f"files/unknown.{img_type}")

        image = Image.open(f"files/unknown.{img_type}")
        width_res, height_res = image.size

        if img_type != 'gif':
            await resize(f"files/unknown.{img_type}", width, f"files/unknown_resized.{img_type}")
        elif img_type == 'gif' and width >= width_res:
            await message.channel.send("Sorry, but you can't use this command for upscaling gifs")
            return
        else:
            await resize_gif(message, f"files/unknown.{img_type}", f"files/unknown_resized.{img_type}", (width, width))

        if 8000000 < os.stat(f"files/unknown_resized.{img_type}").st_size < 10000000:
            await imgur(message, img_url)
        elif os.stat(f"files/unknown_resized.{img_type}").st_size > 10000000:
            await message.channel.send("Your image is over 10MB big, try resizing it first.")
            return
        else:
            with open(f"files/unknown_resized.{img_type}", "rb") as g:
                picture = discord.File(g, filename=f'unknown_resized.{img_type}')
                await message.channel.send(file=picture)

        image.close()
        os.remove(f"files/unknown.{img_type}")
        os.remove(f"files/unknown_resized.{img_type}")
    except Exception as e:
        await tools.error_log(message, e)


async def resize_gif(message, path, save_as=None, resize_to=None):
    """
    Resizes the GIF to a given length:

    Args:
        path: the path to the GIF file
        save_as (optional): Path of the resized gif. If not set, the original gif will be overwritten.
        resize_to (optional): new size of the gif. Format: (int, int). If not set, the original GIF will be resized to
                              half of its size.
    """
    all_frames = extract_and_resize_frames(path, resize_to)

    if not save_as:
        save_as = path

    if len(all_frames) == 1:
        await message.channel.send("Warning: only 1 frame found")
        all_frames[0].save(save_as, optimize=True)
    else:
        all_frames[0].save(save_as, optimize=True, save_all=True, append_images=all_frames[1:], loop=1000)


def analyseImage(path):
    """
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.
    """
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results


def extract_and_resize_frames(path, resize_to=None):
    """
    Iterate the GIF, extracting each frame and resizing them

    Returns:
        An array of all frames
    """
    mode = analyseImage(path)['mode']

    im = Image.open(path)

    if not resize_to:
        resize_to = (im.size[0] // 2, im.size[1] // 2)

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')

    all_frames = []

    try:
        while True:
            # print("saving %s (%s) frame %d, %s %s" % (path, mode, i, im.size, im.tile))

            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)

            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(im, (0, 0), im.convert('RGBA'))

            new_frame.thumbnail(resize_to, Image.ANTIALIAS)
            all_frames.append(new_frame)

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass

    return all_frames


async def imgur(message, url=None):
    try:
        im = ImgurClient(CLIENT_ID, CLIENT_SECRET)

        if url:
            img_url = url
        else:
            img_url = message.content.split()[1]

        img_type = tools.get_img_type(img_url)

        await tools.download_url(img_url, f"files/imgur.{img_type}")

        if os.stat(f"files/imgur.{img_type}").st_size > 10000000:
            await message.channel.send("Your image is over 10MB big, try resizing it first.")
        else:
            img = im.upload_from_path(f"files/imgur.{img_type}")
            await message.channel.send(f"{img['link']}")

        os.remove(f"files/imgur.{img_type}")

    except Exception as e:
        await tools.error_log(message, e)


async def download_from_url(url):
    r = requests.get(
        url, stream=True, headers={
            'User-agent': 'Mozilla/5.0'})

    with open(f"files/attachment.png", 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)


async def extract_string_image(message):
    await message.channel.send(pytesseract.image_to_string(Image.open('files/test.png')))
