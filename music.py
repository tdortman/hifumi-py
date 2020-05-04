import discord
from discord.ext import commands
import os
import youtube_dl
from discord.utils import get

bot = commands.Bot(command_prefix="h?")


@bot.command(aliases=["j"])
async def join(ctx):
    global voice
    try:
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        print(f"The bot has connected to {channel}\n")

        await ctx.send(f"Joined {channel}!")
    except AttributeError:
        await ctx.send("You have to join a voice channel first!")


@bot.command(aliases=["l"])
async def leave(ctx):
    try:
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"The bot has left {channel}")
            await ctx.send(f"Left {channel}!")
        else:
            await ctx.send("Not currently in a voice channel!")
    except AttributeError:
        await ctx.send("We both have to be in the same voice channel "
                       "for this!")


@bot.command(aliases=["p"])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("Music is already playing!")
        return

    await ctx.send("Getting things ready now!")

    voice = get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"),
               after=lambda e: print(f"{name} has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1
