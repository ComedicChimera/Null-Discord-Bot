import asyncio
from util import client


class Player:
    def __init__(self, channel, vc):
        self.queue = []
        self.channel = channel
        self.vc = vc
        self.player = None
        self.volume = 0.5
        self.loop_queue = False

    async def play(self):
        def after():
            if self.loop_queue:
                ending = self.queue.pop(0)
                self.queue.append(ending)
            else:
                self.queue.pop(0)
            if len(self.queue) > 0:
                self.next_song()
            else:
                fut = asyncio.run_coroutine_threadsafe(self.vc.disconnect(), client.loop)
                fut.result()
        self.player = await self.vc.create_ytdl_player(self.queue[0].url, ytdl_options={'quiet': True}, after=after)
        self.player.start()
        self.player.volume = self.volume

    def add_to_queue(self, song):
        self.queue.append(song)

    def pause(self):
        if not self.check_instance():
            raise Exception('Unable to pause non-playing player.')
        if not self.player.is_playing():
            raise Exception('Unable to pause non-playing player.')
        self.player.pause()

    def resume(self):
        if not self.check_instance():
            raise Exception('Unable to resume non-playing player.')
        self.player.resume()

    def stop(self):
        if not self.check_instance():
            raise Exception('Unable to stop non-playing player.')
        if not self.player.is_playing():
            raise Exception('Unable to stop non-playing player.')
        self.queue = []
        self.player.stop()

    def check_instance(self):
        if not self.player:
            return False
        return True

    def next_song(self):
        fut = asyncio.run_coroutine_threadsafe(self.play(), client.loop)
        fut.result()

