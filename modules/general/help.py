import json
import os
import discord
from util import theme_color


def get_help_message(prefix, command=None):
    if command:
        if command == '__std__':
            raise Exception('Command specified either does not exist or lacks help message.')
        jdata = load_message(command)
        return build_embed(jdata, prefix)
    else:
        jdata = load_message('__std__')
        return build_embed(jdata, prefix)


def load_message(cmd):
    if cmd == '__std__':
        return json.load(open('docs/_help.json'))
    # prevent users from exploiting command structure
    elif cmd == '_help':
        raise Exception('Command specified either does not exist or lacks help message.')
    elif os.path.isfile('docs/%s.json' % cmd):
        return json.load(open('docs/%s.json' % cmd))
    else:
        raise Exception('Command specified either does not exist or lacks help message.')


def build_embed(jdata, prefix):
    embed = discord.Embed(color=theme_color)
    if 'title' in jdata:
        embed.title = prefix + jdata['title']
    if 'body' in jdata:
        embed.description = jdata['body'].replace('#PREFIX', prefix)
    for item in jdata['fields']:
        embed.add_field(name=item['title'], value='\n'.join(item['content']).replace('#PREFIX', prefix), inline=False)
    return embed
