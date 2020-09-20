import discord
import os
import youtube_dl
from discord.utils import get
from tools import error_log
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

file = open(r"files/spotipy.txt", "r")
lines = file.readlines()
SPOTIPY_CLIENT_ID = lines[0]
SPOTIPY_CLIENT_SECRET = lines[1]
SPOTIPY_REDIRECT_URI = lines[2]
file.close()

bot = None


def passClientVar(client):
    global bot
    bot = client


async def join(message):
    try:
        global voice
        try:
            channel = message.author.voice.channel
            voice = get(bot.voice_clients, guild=message.guild)

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()

            print(f"The bot has connected to {channel}\n")

            await message.channel.send(f"Joined {channel}!")
        except AttributeError:
            await message.channel.send("You have to join a voice channel first!")
    except Exception as e:
        await error_log(message, e)


async def leave(message):
    try:
        channel = message.author.voice.channel
        voice = get(bot.voice_clients, guild=message.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"The bot has left {channel}")
            await message.channel.send(f"Left {channel}!")
        else:
            await message.channel.send("Not currently in a voice channel!")
    except AttributeError:
        await message.channel.send("We both have to be in the same voice channel "
                                   "for this!")
    except Exception as e:
        await error_log(message, e)


async def play(message, url: str):
    try:
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file, but it's being played")
            await message.channel.send("Music is already playing!")
            return

        await message.channel.send("Getting things ready now!")

        voice = get(bot.voice_clients, guild=message.guild)
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
    except Exception as e:
        await error_log(message, e)


async def spotify(message):
    scope = "user-library-read"

    auth_manager = SpotifyOAuth(scope=scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                                redirect_uri=SPOTIPY_REDIRECT_URI)
    auth_manager.get_access_token(-1)

    sp = spotipy.Spotify(auth=auth_manager)

    artist = sp.artist("spotify:artist:0bAsR2unSRpn6BQPEnNlZm")
    await message.channel.send(artist)
