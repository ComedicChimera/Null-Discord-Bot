from command import command
from util import client, theme_color, error_color
import modules.internet.apis as apis
import discord
import modules.internet.reddit as reddit
import re
from logger import log


URBAN_ICON = '''https://is3-ssl.mzstatic.com/image/thumb/
Purple111/v4/81/c8/5a/81c85a6c-9f9d-c895-7361-0b19b3e5422e/
mzl.gpzumtgx.png/246x0w.jpg'''


@command('joke')
async def tell_joke(message):
    joke = apis.get_joke()
    await client.send_message(message.channel, joke)


@command('urban')
async def urban_search(message, args):
    try:
        definition = apis.get_urban_definition(args)
        embed = discord.Embed(title=definition['word'], description=definition['definition'], color=theme_color)
        embed.set_footer(text='Powered by Urban Dictionary', icon_url=URBAN_ICON.replace('\n', ''))
        await client.send_message(message.channel, embed=embed)
    except Exception as e:
        log(message.server.id, str(e))
        await client.send_message(message.channel, embed=discord.Embed(
            color=error_color,
            description='Failed to get definition.'
        ))


@command('meme')
async def get_meme(message):
    try:
        img = reddit.get_image('dankmemes')
        await client.send_file(message.channel, img, filename='meme.png')
    except Exception as e:
        log(message.server.id, str(e))
        await client.send_message(message.channel, embed=discord.Embed(
            color=error_color,
            description='Failed to connect to reddit.'
        ))


@command('genmeme')
async def generate_meme(message, args):
    texts = re.findall(r'"(?:[^"\\]|\\.)*"', args)
    if len(texts) > 3:
        await client.send_message(message.channel, embed=discord.Embed(
            color=error_color,
            description='Too many parameters.'
        ))
    for i in range(len(texts)):
        texts[i] = texts[i][1:-1]
    try:
        len_text = len(texts)
        if len_text == 3:
            image = apis.get_custom_meme(texts[0], texts[1], texts[2])
        elif len_text == 2:
            image = apis.get_custom_meme(texts[0], texts[1])
        elif len_text == 1:
            image = apis.get_custom_meme(texts[0])
        else:
            raise ValueError('Too few parameters.')
        await client.send_file(message.channel, image, filename='custom_meme.png')
    except KeyError:
        await client.send_message(message.channel, embed=discord.Embed(
            color=error_color,
            description='Invalid template name.'
        ))
    except ValueError as ve:
        await client.send_message(message.channel, embed=discord.Embed(
            color=error_color,
            description=str(ve)
        ))
    except Exception as e:
        log(message.server.id, str(e))
        await client.send_message(message.channel, embed=discord.Embed(
            color=error_color,
            description='Failed to connect to ImageFlip Api.'
        ))


@command('reddit')
async def get_reddit(message, args):
    try:
        img = reddit.get_image(args)
        await client.send_file(message.channel, img, filename='reddit.png')
    except Exception as e:
        log(message.server.id, str(e))
        await client.send_message(message.channel, embed=discord.Embed(
            color=error_color,
            description='Failed to connect to reddit.'
        ))


@command('cat')
async def get_cat(message):
    try:
        img = reddit.get_image('cats')
        await client.send_file(message.channel, img, filename='cat.png')
    except Exception as e:
        log(message.server.id, str(e))
        await client.send_message(message.channel, embed=discord.Embed(
            color=error_color,
            description='Failed to connect to reddit.'
        ))


@command('catfact')
async def cat_fact(message):
    try:
        fact = apis.get_cat_fact()
        await client.send_message(message.channel, fact)
    except Exception as e:
        log(message.server.id, str(e))
        await client.send_message(message.channel, 'No cat fact for you.')
