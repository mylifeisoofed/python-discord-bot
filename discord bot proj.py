import discord
from discord.ext import commands
from pynput.keyboard import Key, Controller
from time import sleep

client = commands.Bot(command_prefix = '.')
keyboard = Controller()


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
@client.event
async def on_member_join(member):
    print(f'{member} has joined the server!')
@client.event
async def on_member_remove(member):
    print(f'{member} has left the server!')

@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency*1000)}ms')

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

client.run('NjUwNDMxMDk4MjExNTMyODAx.XfFs6g.kk-sDd6Lze3qTILudYgT3qUYawE')
