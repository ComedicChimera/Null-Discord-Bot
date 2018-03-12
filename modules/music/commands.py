from random import shuffle

import discord
import modules.music.voice as voice

import modules.music.audio as audio
from command import command
from util import client, theme_color


@command('play')
async def play(message, args):
    is_ready = True
    if not client.is_voice_connected(message.server):
        is_ready = await voice.join(message)
    if is_ready:
        await audio.play(message, args)


@command('stop')
async def stop(message):
    try:
        await audio.stop(message)
        await client.send_message(message.channel, 'Music successfully stopped.')
    except Exception as e:
        await client.send_message(message.channel, e)


@command('pause')
async def pause(message):
    try:
        audio.pause(message)
        await client.send_message(message.channel, 'Music successfully paused.')
    except Exception as e:
        await client.send_message(message.channel, e)


@command('resume')
async def resume(message):
    try:
        audio.resume(message)
        await client.send_message(message.channel, 'Music successfully resumed.')
    except Exception as e:
        await client.send_message(message.channel, e)


@command('skip')
async def skip(message):
    try:
        audio.skip(message)
        await client.send_message(message.channel, 'Song successfully skipped.')
    except Exception as e:
        await client.send_message(message.channel, e)


@command('volume')
async def volume(message, args):
    try:
        if args == '':
            await client.send_message(message.channel, 'Volume currently set to: `%s`.' % audio.get_volume(message))
        else:
            audio.set_volume(message, args)
            await client.send_message(message.channel, 'Player volume set to `%s`.' % args)
    except Exception as e:
        await client.send_message(message.channel, e)


@command('queue')
async def show_queue(message):
    if message.server not in voice.connected_guilds:
        await client.send_message(message.channel, 'Queue is empty.')
        return
    queue = voice.connected_guilds[message.server].queue
    if len(queue) > 0:
        embed = discord.Embed(color=theme_color)
        embed.add_field(name='Now Playing', value=queue[0].title)
        if len(queue) > 1:
            up_next = '\n'.join([x.title for x in queue[1:]])
            embed.add_field(name='Up Next', value=up_next, inline=False)
        await client.send_message(message.channel, embed=embed)
    else:
        await client.send_message(message.channel, 'Queue is empty.')


def check_queue_positions(message, * pos):
    int_positions = []
    for item in pos:
        try:
            int_positions.append(int(item))
        except ValueError:
            raise Exception('Invalid position `%s`.' % item)
    for item in int_positions:
        if item < 1 or item > len(voice.connected_guilds[message.server].queue) - 1:
            raise Exception('Invalid position `%d`.' % item)
    return int_positions


@command('swap')
async def swap_queue_items(message, args):
    if message.server not in voice.connected_guilds:
        await client.send_message(message.channel, 'Queue is empty.')
        return
    ndxs = args.split(' ')
    if len(ndxs) != 2:
        await client.send_message(message.channel, 'Invalid positions.')
        return
    try:
        int_positions = check_queue_positions(message, ndxs[0], ndxs[1])
    except Exception as e:
        await client.send_message(message.channel, e)
        return
    i, j = int_positions[0], int_positions[1]
    voice.connected_guilds[message.server].queue[i], voice.connected_guilds[message.server].queue[j] = voice.connected_guilds[message.server].queue[j], voice.connected_guilds[message.server].queue[i]
    title1 = voice.connected_guilds[message.server].queue[i].title
    title2 = voice.connected_guilds[message.server].queue[j].title
    await client.send_message(message.channel, 'Swapped `%s` and `%s`.' % (title1, title2))


@command('remove')
async def remove_queue_item(message, args):
    if message.server not in voice.connected_guilds:
        await client.send_message(message.channel, 'Queue is empty.')
        return
    try:
        ndx = check_queue_positions(message, args)[0]
    except Exception as e:
        await client.send_message(message.channel, e)
        return
    song = voice.connected_guilds[message.server].queue.pop(ndx)
    await client.send_message(message.channel, 'Removed song `%s` from the queue.' % song.title)


@command('move')
async def move_queue_item(message, args):
    if message.server not in voice.connected_guilds:
        await client.send_message(message.channel, 'Queue is empty.')
        return
    ndxs = args.split(' ')
    if len(ndxs) != 2:
        await client.send_message(message.channel, 'Invalid positions.')
        return
    try:
        int_positions = check_queue_positions(message, ndxs[0], ndxs[1])
    except Exception as e:
        await client.send_message(message.channel, e)
        return
    i, j = int_positions[0], int_positions[1]
    song_name = voice.connected_guilds[message.server].queue[i].title
    voice.connected_guilds[message.server].queue.insert(j - 1, voice.connected_guilds[message.server].queue.pop(i))
    await client.send_message(message.channel, 'Moved `%s` to queue position `%d.`' % (song_name, j))


@command('clearqueue')
async def clear_queue(message):
    if message.server not in voice.connected_guilds:
        await client.send_message(message.channel, 'Queue is empty.')
        return
    elif len(voice.connected_guilds[message.server].queue) < 2:
        await client.send_message(message.channel, 'Queue is empty.')
        return
    voice.connected_guilds[message.server].queue = voice.connected_guilds[message.server].queue[:1]
    await client.send_message(message.channel, 'Cleared the song queue.')


@command('shufflequeue')
async def shuffle_queue(message):
    if message.server not in voice.connected_guilds:
        await client.send_message(message.channel, 'Queue is empty.')
        return
    queue = voice.connected_guilds[message.server].queue
    if len(queue) < 2:
        await client.send_message(message.channel, 'Queue is empty.')
        return
    nums = range(1, len(queue))
    new_queue = [queue[x] for x in nums]
    shuffle(new_queue)
    voice.connected_guilds[message.server].queue = queue[:1] + new_queue
    await client.send_message(message.channel, 'Shuffled the song queue.')


@command('loopqueue')
async def loop_queue(message):
    if message.server not in voice.connected_guilds:
        await client.send_message(message.channel, 'Queue is empty.')
        return
    state = not voice.connected_guilds[message.server].loop_queue
    voice.connected_guilds[message.server].loop_queue = state
    await client.send_message(message.channel, '**Loop-queue set to `%s`.**' % {True: 'On', False: 'Off'}[state])

