from command import command
from util import client, error_color, theme_color
import discord
import re
import pickle
import os


filters = {

}


@command('addfilter')
async def add_filter(message, args):
    if not message.author.server_permissions.manage_messages:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='Inadequate permissions.' % args))
        return
    if message.server.id in filters:
        if args in filters[message.server.id]:
            await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='Filter `%s` already exists.' % args))
            return
        else:
            filters[message.server.id].append(args)
    else:
        filters[message.server.id] = [args]
    await client.send_message(message.channel, 'Successfully added filter for term: `%s`.' % args)
    cache_filters()


@command('removefilter')
async def remove_filter(message, args):
    if not message.author.server_permissions.manage_messages:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='Inadequate permissions.' % args))
        return
    if message.server.id not in filters:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='Filter `%s` does not exist.' % args))
    elif args not in filters[message.server.id]:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='Filter `%s` does not exist.' % args))
    else:
        filters[message.server.id].pop(filters[message.server.id].index(args))
        await client.send_message(message.channel, 'Successfully removed filter for term: `%s`.' % args)
        cache_filters()


@command('showfilters')
async def show_filters(message, args):
    if message.server.id not in filters:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='Server has no active filters.' % args))
    elif len(filters[message.server.id]) == 0:
        await client.send_message(message.channel, 'Server has no filters.')
    else:
        embed = discord.Embed(color=theme_color, title='Filters')
        embed.description = '\n'.join(filters[message.server.id])
        await client.send_message(message.channel, embed=embed)


def match_filters(message):
    for item in filters[message.server.id]:
        if re.search(re.compile('\s*'.join(list(re.escape(item))), re.MULTILINE | re.IGNORECASE), message.content):
            return True
    return False


def cache_filters():
    with open('cache/filters.pickle', 'bw+') as file:
        pickle.dump(filters, file)


if os.path.isfile('cache/filters.pickle'):
    with open('cache/filters.pickle', 'rb') as p_file:
        filters = pickle.load(p_file)
