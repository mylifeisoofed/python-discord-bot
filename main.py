# python-discord-bot
import asyncio

import discord
import os
from discord.ext import commands, tasks
from pynput.keyboard import Key, Controller
from time import sleep
import random
from itertools import cycle
import youtube_dl
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system
import sys
from json import loads
import json
import shutil
import asyncio
import urllib.parse, urllib.request, re


TOKEN = ## find the token at discord dev hub

client = commands.Bot(command_prefix='.')
status = cycle(['Minecraft', 'Roblox', 'League of Legends', 'Brawlhalla', 'Red Dead Redemption 2', 'Grand Theft Auto V',
                'STAR WARS: BATTLEFRONT 2', 'Monster Hunter: World', 'Minecraft Pocket Edition',
                'Skyrim Special Edition', 'Fallout 4', "Garry's Mod", "Counter Strike: Global Offensive",
                'Among Us', 'Genshin Impact', 'VALORANT', 'Blue Protocol'])
keyboard = Controller()
client.remove_command('help')
players = {}


def convert(string):
    li = list(string.split(" "))
    return li
    # will break down individual words into lists for our bot to detect specific words without falsely detecting words.


@client.event  # Our Logs that keep track of comments and do some stuff
async def on_message(message):
    author = message.author
    log_contents = message.content # this is for our logs
    content = convert(message.content.lower()) # this is for the bot
    channel = message.channel
    #if message.author == client.user: #for if you don't want the code to check yourself
       # return
    if message.author.bot: #so that our bot doesn't reply and check itself
        return


    #print (content)
    print('{}: {}'.format(author, log_contents)) #profanity filter. Warns user of profanity.
    await client.process_commands(message)
    if "shit" in content or\
            "fuck" in content or\
            "nigger" in content or\
            "fuck you" in content or\
            "ass" in content or\
            "faggot" in content or\
            "fag" in content or\
            "dick" in content or\
            "pussy" in content or\
            "coon" in content or\
            "damn" in content or\
            "cunt" in content or\
            "bitch" in content or\
            "nigger" in content or\
            "dammit" in content or\
            "bullshit" in content:
        print("bad word detected")
        await channel.send(f"Oi! Watch your profanity, {author.mention}!")
@client.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
    if author.bot:
        return
    await channel.send('{}: {}'.format(author, content))
    await channel.send(f'You cannot erase history, {author.mention}')
    await client.process_commands(message)



@client.command(pass_context = True)
async def pog(ctx):
    await ctx.send("Pog!")

@client.event
async def on_ready():  # Should print bot is ready if its successful
    print("Bot is Ready")
    change_status.start()

    # await client.change_presence(status=discord.Status.idle, activity=discord.Game('Python'))

@client.event  # Will print out the member's name of the server
async def on_member_join(member):
    print(f'{member} has joined the server!')


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server!')


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


##@client.event
##async def on_error(ctx):
##    await ctx.send("Unknown Command")

@client.command(aliases=['pong'])  # returns the ping latency
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency * 1000)}ms')

@client.command(pass_context = True)
async def rps(ctx, *, playerChoice):
    gameAnnounce = "none"
    channel = ctx.channel
    weapon = ['rock', 'paper', 'scissors']
    await ctx.send(f'You picked {playerChoice} \nBot picked {random.choice(weapon)}')



@client.command(aliases=["8ball"])
async def _8ball(ctx, *, questions):
    responses = ["Yes", "No", "I don't know about that one", "Certainly", "Definitely", "I doubt so", "Improbable",
                 "Most Likely"]
    await ctx.send(f'Question: {questions} \nAnswer: {random.choice(responses)}')
@_8ball.error
async def _8ball(ctx, error):
    await ctx.send('Please try again and type in the question after the command. Ex: ".8ball Am I cool?".')

@client.command(pass_context=True)
async def help(ctx):  # help command
    author = ctx.message.author

    embed = discord.Embed(colour=discord.Colour.orange())
    embed.set_author(name='All Commands Currently Available')
    embed.add_field(name='.help', value='Self explanatory', inline=False)
    embed.add_field(name='.ping', value='Shows how fast your connection to Discord is', inline=False)
    embed.add_field(name='.8ball <question>', value='Ask me a question after the command for me to answer!', inline=False)
    embed.add_field(name='.join', value='Joins the Voice Channel that you are in', inline=False)
    embed.add_field(name='.leave', value='Leaves the Voice Channel that you are in', inline=False)
    embed.add_field(name='.play <youtube url>',
                    value='Plays any music you want. No Pause or Resume or Skip features currenty, so type ".leave" to stop the bot before choosing a next song.',
                    inline=False)
    embed.add_field(name='.pause', value='Pauses the currently played music', inline=False)
    embed.add_field(name='.resume', value='Resumes the paused music', inline=False)
    embed.add_field(name='.stop', value='Stops the currently played music and leaves the call', inline=False)
    embed.add_field(name='.queue', value='Add multiple music in the queue.', inline=False)
    embed.add_field(name='.pog', value='Poggers!', inline=False)
    embed.add_field(name='.rps <rock, papers, or scissors>', value='Play a game of Rock, Paper, Scissors with the bot!', inline=False)
    embed.add_field(name='.ZAWARUDO', value='ほう…向かってくるのか', inline=False)
    embed.add_field(name='.<your stand name>', value='Plays your desired Stand sound. Check the RBA chat to see stands. The bot must be in a voice channel for this to work.', inline=True)
    await ctx.send(author, embed=embed)





@client.event  # emotes will print out
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    await channel.send('{} has added {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))


@client.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    await channel.send(
        '{} has removed {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))


# Music channel stuff
@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)


    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        await channel.connect()
    await ctx.send(f"Joined {channel}")


@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")


@client.command(aliases=["za warudo", "ZA WARUDO", "dio", "DIO"])
async def ZAWARUDO(ctx):
    channel = ctx.channel
    await channel.send('https://www.youtube.com/watch?v=7ePWNmLP0Z0&ab_channel=idiotindustries')

# old music Player
#@client.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['p'])
#async def play(ctx, url: str):
#    song_there = os.path.isfile("song.mp3")
#    try:
#        if song_there:
#            os.remove("song.mp3")
#    except PermissionError:
#        await ctx.send("Wait for the current playing music end or use the '.skip' command")
#        return
#    await ctx.send("Getting everything ready, playing audio soon")
#    print("Someone wants to play music let me get that ready for them...")
#    voice = get(client.voice_clients, guild=ctx.guild)
#    ydl_opts = {
#        'format': 'bestaudio/best',
#        'postprocessors': [{
#            'key': 'FFmpegExtractAudio',
#            'preferredcodec': 'mp3',
#            'preferredquality': '192',
#        }],
#    }
#    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#        ydl.download([url])
#    for file in os.listdir("./"):
#        if file.endswith(".mp3"):
#            os.rename(file, 'song.mp3')
#    voice.play(discord.FFmpegPCMAudio("song.mp3"))
#    voice.volume = 100
#    voice.is_playing()

@client.command(pass_context=True, aliases=['p', 'pla']) #reworked music bot
async def play(ctx, url:str):

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "song.mp3")

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 1

            else:
                queues.clear()
                return
        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")
        ## end of class

    voice = get(client.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel

    if voice and voice.is_connected():
        voice.move_to(channel)
    else:
        await channel.connect()

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("The Music is currently being played. If you want to queue in another music, use the .queue <youtube url> to add it into the queue.")
        return

    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old queue folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format' : 'bestaudio/best',
        'quiet' : True,
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing {nname[0]}")
    print("playing\n")





@client.command(pass_context=True, aliases=['theglobal', 'THEGLOBAL', 'zagurobo', 'ZAGUROBO'])
async def ZAGLOBAL(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    voice.play(discord.FFmpegPCMAudio("ZA_GLOBAL.wav"))
    voice.volume = 100
    voice.is_playing()

@client.command(pass_context=True, aliases=['dickbutt', 'DickButt', 'DIKUBUTTU'])
async def DICKBUTT(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    voice.play(discord.FFmpegPCMAudio("phil_stand_sound.wav"))
    voice.volume = 100
    voice.is_playing()

@client.command(pass_context=True, aliases=['Sped', 'sped', 'Speed', 'speed'])
async def SPED(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    voice.play(discord.FFmpegPCMAudio("Renees_stand_sound.wav"))
    voice.volume = 100
    voice.is_playing()

@client.command(pass_context=True, aliases=['hotshot', 'HotShot', 'Hotshot', 'HottuShottu'])
async def HOTSHOT(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    voice.play(discord.FFmpegPCMAudio("robert_stand.wav"))
    voice.volume = 100
    voice.is_playing()

@client.command(pass_context=True, aliases=['gambit', 'Gambit', 'GAMBITTU', 'GAMUBITTU'])
async def GAMBIT(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    voice.play(discord.FFmpegPCMAudio("vincent_stand_sound.wav"))
    voice.volume = 100
    voice.is_playing()

@client.command(pass_context=True, aliases=['damilkquu', 'DAMIRUKUU', 'DaMilkQuu'])
async def DAMILKQUU(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    voice.play(discord.FFmpegPCMAudio("tina_stand_sound.wav"))
    voice.volume = 100
    voice.is_playing()

@client.command(pass_context=True, aliases=['frostbite', 'FrostBite', 'FUROSUTUBAITU'])
async def FROSTBITE(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    voice.play(discord.FFmpegPCMAudio("jacobs_stand_sound_rework.wav"))
    voice.volume = 100
    voice.is_playing()

@client.command(pass_context=True, aliases=['conflaguratedbeam', 'ConflaguratedBeam', 'KONUFURAGURATEDUBIMU'])
async def CONFLAGURATEDBEAM(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    voice.play(discord.FFmpegPCMAudio("Khangs_Stand_Sound.wav"))
    voice.volume = 100
    voice.is_playing()

@play.error
async def play_error(ctx, error):
    await ctx.send('Please try again. I did not pick up the youtube link or you have not given me a youtube link. '
                   'Be sure to also use ".join" while in a voice channel before using this command. If you want to queue in some songs, use the '
                   '.queue <url link> command.')

# Bot commands for music player

@client.command(pass_context=True)
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.pause()
        await  ctx.send("Music paused")
@pause.error
async def pause_error(ctx, error):
    await ctx.send("I'm not in your voice channel or it's already paused! Use the '.join' command.")

@client.command(pass_context=True)
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        voice.resume()
        await ctx.send("Resumed Music")
    else:
        await ctx.send("Music not resumed")

@resume.error
async def resume_error(ctx, error):
    await ctx.send("I'm not in your voice channel or the music is already playing! Use the '.join' command.")

@client.command(pass_context=True)
async def stop(ctx):
    player = get(client.voice_clients, guild=ctx.guild)
    if player.is_playing():
        player.stop()

@client.command(pass_context=True)
async def skip(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()

    if voice and voice.is_playing():
        print("Music Skipped")
        voice.stop()
        await ctx.send("Music skipped")
    else:
        print("No music playing failed to skip")
        await ctx.send("No music is being played")

queues = {}

@client.command(pass_context=True, aliases=['q', 'que'])
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])
    await ctx.send("Adding the song " + str(q_num) + " to the queue")

    print ("Song added to the queue\n")



"""
# C:\ffmpeg\bin\ffmpeg.exe -codecs for the ffmpeg stuff

# Smash Flash 2 testing stuff
@client.command()
async def w(ctx):
    keyboard.press('w')
    sleep(.8)
    keyboard.release('w')

@client.command()
async def d(ctx):
    keyboard.press('d')
    sleep(.8)
    keyboard.release('d')

@client.command()
async def a(ctx):
    keyboard.press('a')
    sleep(.8)
    keyboard.release('a')

@client.command()
async def s(ctx):
    keyboard.press('s')
    sleep(.8)
    keyboard.release('s')

@client.command()
async def ls(ctx):
    keyboard.press('a')
    keyboard.press('p')
    sleep(.2)
    keyboard.release('a')
    keyboard.release('p')

@client.command()
async def rs(ctx):
    keyboard.press('d')
    keyboard.press('p')
    sleep(.2)
    keyboard.release('d')
    keyboard.release('p')

@client.command()
async def us(ctx):
    keyboard.press('w')
    keyboard.press('p')
    sleep(.2)
    keyboard.release('w')
    keyboard.release('p')

@client.command()
async def ds(ctx):
    keyboard.press('s')
    keyboard.press('p')
    sleep(.2)
    keyboard.release('s')
    keyboard.release('p')

@client.command()
async def o(ctx):
    keyboard.press('o')
    sleep(.5)
    keyboard.release('o')

@client.command()
async def i(ctx):
    keyboard.press('i')
    sleep(.5)
    keyboard.release('i')
"""

client.run(TOKEN)
