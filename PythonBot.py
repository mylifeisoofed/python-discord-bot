# python-discord-bot
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



TOKEN = // Find it on discord.gg hub

client = commands.Bot(command_prefix = '.')
status = cycle(['Minecraft','Roblox','League of Legends','Brawlhalla','Red Dead Redemption 2','Grand Theft Auto V','STAR WARS: BATTLEFRONT 2','Monster Hunter: World','Minecraft Pocket Edition','Skyrim Special Edition', 'Fallout 4', "Garry's Mod","Counter Strike: GLobal Offensive",])
keyboard = Controller()
client.remove_command('help')
players = {}

@client.event
async def on_message(message):
    author = message.author
    content = message.content
    print('{}: {}'.format(author, content))
    await client.process_commands(message)
@client.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
    await channel.send('{}: {}'.format(author, content))
    await channel.send(f'You cannot erase history, {author}'.format(author))
    await client.process_commands(message)
@client.event
async def on_ready():
    print("Bot is Ready")
    change_status.start()
    #await client.change_presence(status=discord.Status.idle, activity=discord.Game('Python'))
@client.event
async def on_member_join(member):
    print(f'{member} has joined the server!')
@client.event
async def on_member_remove(member):
    print(f'{member} has left the server!')
@tasks.loop(seconds = 10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))
##@client.event
##async def on_error(ctx):
##    await ctx.send("Unknown Command")

@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency*1000)}ms')

@client.command(aliases = ["8ball"])
async def _8ball(ctx, *, questions):
    responses = ["Yes", "No", "I don't know about that one", "Certainly", "Definitley", "I doubt so", "Improbable", "Most Likely"]
    await ctx.send(f'Question: {questions} \nAnswer: {random.choice(responses)}')
@client.command(pass_context = True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.orange()
    )

    embed.set_author(name='All Commands Currently Available')
    embed.add_field(name='.help', value='Self explanatory', inline=False)
    embed.add_field(name='.ping', value='Shows how fast your connection to Discord is', inline=False)
    embed.add_field(name='.8ball', value='Ask me a question after the command for me to answer!', inline=False)
    embed.add_field(name='.join', value='Joins the Voice Channel that you are in', inline=False)
    embed.add_field(name='.leave', value='Leaves the Voice Channel that you are in', inline=False)
    embed.add_field(name='.play [youtube url]', value='Plays any music you want. No Pause or Resume or Skip features currenty, so type ".leave" to stop the bot before choosing a next song.', inline=False)
    await ctx.send(author, embed=embed)

@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    await channel.send('{} has added {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))
@client.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    await channel.send('{} has removed {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))

# Music channel stuff
@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command()
async def leave(ctx):
  await ctx.voice_client.disconnect()


@client.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music end or use the 'stop' command")
        return
    await ctx.send("Getting everything ready, playing audio soon")
    print("Someone wants to play music let me get that ready for them...")
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.volume = 100
    voice.is_playing()

@client.command(pass_context=True)
async def pause(ctx):
    player = get(client.voice_clients, guild=ctx.guild)
    if player.is_playing():
        player.pause()

@client.command(pass_context=True)
async def resume(ctx):
    player = get(client.voice_clients, guild=ctx.guild)
    if player.is_paused():
        player.resume()

@client.command(pass_context = True)
async def stop(ctx):
    player = get(client.voice_clients, guild=ctx.guild)
    player.stop()
    await ctx.voice_client.disconnect()


    
# C:\ffmpeg\bin\ffmpeg.exe -codecs for the ffmpeg stuff
    
#Smash Flash 2 stuff
##@client.command()
##async def w(ctx):
##    keyboard.press('w')
##    sleep(.8)
##    keyboard.release('w')
##
##@client.command()
##async def d(ctx):
##    keyboard.press('d')
##    sleep(.8)
##    keyboard.release('d')
##
##@client.command()
##async def a(ctx):
##    keyboard.press('a')
##    sleep(.8)
##    keyboard.release('a')
##
##@client.command()
##async def s(ctx):
##    keyboard.press('s')
##    sleep(.8)
##    keyboard.release('s')
##
##@client.command()
##async def ls(ctx):
##    keyboard.press('a')
##    keyboard.press('p')
##    sleep(.2)
##    keyboard.release('a')
##    keyboard.release('p')
##
##@client.command()
##async def rs(ctx):
##    keyboard.press('d')
##    keyboard.press('p')
##    sleep(.2)
##    keyboard.release('d')
##    keyboard.release('p')
##
##@client.command()
##async def us(ctx):
##    keyboard.press('w')
##    keyboard.press('p')
##    sleep(.2)
##    keyboard.release('w')
##    keyboard.release('p')
##
##@client.command()
##async def ds(ctx):
##    keyboard.press('s')
##    keyboard.press('p')
##    sleep(.2)
##    keyboard.release('s')
##    keyboard.release('p')
##
##@client.command()
##async def o(ctx):
##    keyboard.press('o')
##    sleep(.5)
##    keyboard.release('o')



client.run(TOKEN)

