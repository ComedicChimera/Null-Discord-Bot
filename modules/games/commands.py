from command import command
from util import client, theme_color
import modules.games.trivia as trivia
import discord
import session
import modules.games.rps as rps
from random import randint


@command('trivia')
async def play_trivia(message):
    question = trivia.get_question()
    embed = discord.Embed(color=theme_color, title=question.question)
    desc = ' '.join(['%s. %s\t' % (key, question.options[key]) for key in question.options])
    embed.description = desc
    embed.set_footer(text='Powered by OpenTriviaDB')
    await client.send_message(message.channel, embed=embed)
    session.create_session(message.server.id, message.channel, [str(message.author)], trivia.get_callback(question))


@command('rps')
async def play_rps(message):
    session.create_session(message.server.id, message.channel, [str(message.author)], rps.get_handler())
    await client.send_message(message.channel, '**Started match!**')


@command('coinflip')
async def flip_coin(message):
    rand = randint(0, 1)
    if rand == 0:
        await client.send_message(message.channel, 'Heads.')
    else:
        await client.send_message(message.channel, 'Tails.')


@command('diceroll')
async def roll_dice(message):
    rand = randint(0, 5)
    await client.send_message(message.channel, ':game_die: **You rolled a `%d`.** :game_die:' % (rand + 1))


@command('drawcard')
async def draw_card(message):
    num = randint(0, 12)
    suit = randint(0, 3)
    suits = {
        0: ':clubs:',
        1: ':spades:',
        2: ':diamonds:',
        3: ':hearts:'
    }
    if num > 9:
        face_cards = {
            10: 'Jack',
            11: 'Queen',
            12: 'King'
        }
        num = face_cards[num]
    elif num == 0:
        num = 'Ace'
    else:
        num += 1
    suit = suits[suit]
    await client.send_message(message.channel, '%s **%s** %s' % (suit, num, suit))
