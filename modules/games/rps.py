from util import client, theme_color
from random import randint
from discord import Embed
import session


moves = {
    'rock': 0,
    'paper': 1,
    'scissors': 2
}


def play(user_move):
    cmove = randint(0, 2)
    umove = moves[user_move]
    return compare(cmove, umove), [cmove, umove]


def compare(cmove, umove):
    if cmove == umove:
        return 1
    elif cmove - 1 == umove:
        return 0
    elif umove - 1 == cmove:
        return 2
    elif umove == 0 and cmove == 2:
        return 2
    else:
        return 0


class RPSGame:
    def __init__(self):
        self.user_score = 0
        self.cpu_score = 0


games = {

}


def get_handler():
    async def handler(message, sid):
        if sid not in games:
            games[sid] = RPSGame()
        if message.content.lower() in moves:
            result, mvs = play(message.content.lower())
            result_strings = {
                0: 'You lost.',
                1: 'You tied.',
                2: 'You won!'
            }
            embed = Embed(color=theme_color, title=result_strings[result])
            move_strings = {
                0: ':new_moon: **Rock** :new_moon:',
                1: ':page_facing_up: **Paper** :page_facing_up:',
                2: ':scissors: **Scissors** :scissors:'
            }
            embed.add_field(name='CPU', value=move_strings[mvs[0]])
            embed.add_field(name='Player', value=move_strings[mvs[1]])
            if result == 0:
                games[sid].cpu_score += 1
            elif result == 2:
                games[sid].user_score += 1
            embed.set_footer(text='Score: %d to %d' % (games[sid].user_score, games[sid].cpu_score))
            await client.send_message(message.channel, embed=embed)
        elif message.content == '!rps end':
            session.remove_session(message.server.id, sid)
            if sid not in games:
                await client.send_message(message.channel, 'No one played.')
                return
            embed = Embed(color=theme_color)
            if games[sid].user_score > games[sid].cpu_score:
                title = ':sunglasses: You won! :sunglasses:'
            elif games[sid].user_score < games[sid].cpu_score:
                title = ':sob: You lost. :sob:'
            else:
                title = 'It was a tie.'
            embed.title = title
            embed.description = 'Score: %d to %d' % (games[sid].user_score, games[sid].cpu_score)
            await client.send_message(message.channel, embed=embed)
            games.pop(sid)
    return handler
