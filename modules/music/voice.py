# player import
from modules.music.player import Player
from util import client


connected_guilds = {}


async def join(msg):
    ch = msg.author.voice.voice_channel
    if ch:
        connected_guilds[msg.server] = Player(ch, await client.join_voice_channel(ch))
        return True
    else:
        await client.send_message(msg.channel, 'User must be in a voice channel to use voice commands.')
        return False
