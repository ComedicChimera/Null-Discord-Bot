import http.client
import re
import urllib.parse

import pafy

from modules.music.voice import connected_guilds
from util import client
from logger import log


class Song:
    def __init__(self, title, url):
        self.title = title
        self.url = url


async def play(msg, song_name):
    h1 = http.client.HTTPSConnection("www.youtube.com")
    try:
        h1.request("GET", "/results?search_query=" + urllib.parse.quote_plus(song_name))
    except Exception as e:
        log(msg.server.id, str(e))
    response = h1.getresponse()
    match = re.search(r"href=\"/watch[^\"]+", str(response.read()))
    vid_id = match.group(0)[15:]
    url = 'https://www.youtube.com/watch?v=' + vid_id
    song = Song(get_title(url), url)
    connected_guilds[msg.server].add_to_queue(song)
    if not connected_guilds[msg.server].check_instance():
        await connected_guilds[msg.server].play()
        await client.send_message(msg.channel, '**Now Playing: `%s`**' % connected_guilds[msg.server].player.title)
    elif not connected_guilds[msg.server].player.is_playing():
        await connected_guilds[msg.server].play()
        await client.send_message(msg.channel, '**Now Playing: `%s`**' % connected_guilds[msg.server].player.title)
    else:
        await client.send_message(msg.channel, '**Song `%s` added to queue.**' % song.title)


async def stop(msg):
    if connected_guilds[msg.server].check_instance():
        connected_guilds[msg.server].stop()
        await connected_guilds[msg.server].vc.disconnect()
    else:
        raise Exception('Unable to stop non-playing player.')


def pause(msg):
    if connected_guilds[msg.server].check_instance():
        connected_guilds[msg.server].pause()
    else:
        raise Exception('Unable to pause non-playing player.')


def resume(msg):
    if connected_guilds[msg.server].check_instance():
        connected_guilds[msg.server].resume()
    else:
        raise Exception('Unable to resume non-playing player.')


def skip(msg):
    if connected_guilds[msg.server].check_instance():
        if len(connected_guilds[msg.server].queue) > 0:
            connected_guilds[msg.server].player.stop()
        else:
            raise Exception('Unable to skip on an empty queue.')
    else:
        raise Exception('Unable to skip non-playing player.')


def set_volume(msg, vol):
    try:
        vol = float(vol)
    except ValueError:
        raise Exception('Invalid volume.')
    if vol > 100 or vol < 0:
        raise Exception('Invalid volume.')
    connected_guilds[msg.server].player.volume = vol / 100
    connected_guilds[msg.server].volume = vol / 100


def get_volume(msg):
    return connected_guilds[msg.server].volume * 100


def get_title(url):
    data = pafy.new(url)
    return data.title

