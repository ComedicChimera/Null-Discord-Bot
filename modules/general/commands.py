import os

import discord
import psutil

from command import command
from util import client, set_server_prefix, theme_color, get_server_prefix, error_color
import modules.general.text as text
import modules.general.help as help


# general purpose commands
@command('ping')
async def ping(message):
    await client.send_message(message.channel, 'Pong!')


@command('prefix')
async def set_prefix(message, args):
    if args == '':
        await client.send_message(message.channel, '**Current server prefix: `%s`.**' % get_server_prefix(message.server))
        return
    set_server_prefix(message.server, args)
    await client.send_message(message.channel, '**Server Prefix successfully changed to `%s`.**' % args)


@command('about')
async def about(message):
    embed = discord.Embed(color=theme_color)
    app_info = await client.application_info()
    embed.add_field(name='Name', value='Null')
    embed.add_field(name='Developer', value=app_info.owner)
    embed.add_field(name='Framework', value='Discord.py')
    embed.add_field(name='Shards', value=client.shard_count)
    embed.add_field(name='CPU', value=str(psutil.cpu_percent()) + '%')
    pid = os.getpid()
    py = psutil.Process(pid)
    memory_use = float(py.memory_full_info().rss) / 1048576
    embed.add_field(name='Memory', value='%.2f mb' % memory_use)
    await client.send_message(message.channel, embed=embed)


@command('help')
async def display_help(message, args):
    prefix = get_server_prefix(message.server)
    try:
        if args != '':
            embed = help.get_help_message(prefix, args)
            await client.send_message(message.author, embed=embed)
        else:
            embed = help.get_help_message(prefix)
            await client.send_message(message.author, embed=embed)
    except Exception as e:
        await client.send_message(message.channel, embed=discord.Embed(
            color=error_color,
            description=str(e)
        ))


@command('emojify')
async def emojify(message, args):
    try:
        emojis = text.emojify(args)
    except ValueError:
        await client.send_message(message.channel, embed=discord.Embed(
            color=error_color,
            description=':sob: Sorry, I can\'t emojify special characters. :sob:'
        ))
        return
    await client.send_message(message.channel, emojis)


@command('nonsense')
async def nonsense(message, args):
    try:
        length = int(args)
    except ValueError:
        await client.send_message(message.channel, embed=discord.Embed(
            color=error_color,
            description='Length must be an integer.'
        ))
        return
    if length > 200 or length < 0:
        await client.send_message(message.channel, embed=discord.Embed(
            color=error_color,
            description='Invalid length value.'
        ))
        return
    await client.send_message(message.channel, text.get_random_text(length))


@command('copypasta')
async def copypasta(message, args):
    await client.send_message(message.channel, text.pastify(args))
