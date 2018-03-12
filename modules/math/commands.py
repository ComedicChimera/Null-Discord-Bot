from random import randint, shuffle

import discord
import modules.math.strmath as strmath
import modules.math.wolfram as wolfram

import modules.math.latex as latex
from command import command
from util import client, theme_color, error_color
from logger import log


# import urllib.parse


@command('math')
async def math(message, args):
    result = strmath.evaluate(args)
    if result.type == 'error':
        if result.data.traceback != '':
            embed = discord.Embed(color=error_color, title=result.data.message, description='```\n%s```' % result.data.traceback)
        else:
            embed = discord.Embed(color=error_color, title=result.data.message)
    else:
        embed = discord.Embed(color=theme_color, title='Result', description=result.data)
    await client.send_message(message.channel, embed=embed)


@command('rand')
async def rand(message, args):
    try:
        if ',' in args:
            split_args = args.split(',')
            a, b = int(split_args[0].strip()), int(split_args[1].strip())
            await client.send_message(message.channel, str(randint(a, b)))
        else:
            await client.send_message(message.channel, str(randint(1, int(args))))
    except (TypeError, ValueError):
        await client.send_message(message.channel, '**Invalid position(s).**')


@command('shuffle')
async def shuffle_text(message, args):
    lst = [x.strip(',') for x in args.split(' ')]
    shuffle(lst)
    await client.send_message(message.channel, ', '.join(lst))


@command('tex')
async def generate_latex(message, args):
    code = args.strip('`')
    try:
        image = latex.generate(code)
    except Exception as e:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description=str(e)))
        return
    await client.send_file(message.channel, image, filename='latex.png')


@command('wolfram')
async def wolfram_alpha(message, args):
    try:
        result = wolfram.query(args)
        image = wolfram.join_images(result)
        await client.send_file(message.channel, image, filename='wolfram.png')
        icon_url = 'https://cdn.iconscout.com/public/images/icon/free/png-512/wolfram-alpha-logo-3225dad81e65984f-512x512.png'
        embed = discord.Embed(color=16039746)
        embed.set_footer(text='Powered by Wolfram | Alpha Computational Knowledge Engine', icon_url=icon_url)
        await client.send_message(message.channel, embed=embed)
    except Exception as e:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description=str(e)))


@command('equation')
async def generate_equation(message, args):
    try:
        image = latex.generate_eqn(args)
        await client.send_file(message.channel, image, filename='equation.png')
    except Exception as e:
        log(message.server.id, str(e))
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='Failed to generate equation.'))
