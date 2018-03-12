import requests
from random import shuffle
import html
import discord
import session
from util import theme_color, client, get_server_prefix


API_URL = 'https://opentdb.com/api.php?amount=1&category=9&difficulty=hard&type=multiple'


class Question:
    def __init__(self, jdata):
        self.question = html.unescape(jdata['question'])
        self.answer = html.unescape(jdata['correct_answer'])
        answer_list = [html.unescape(x) for x in jdata['incorrect_answers']]
        answer_list.append(self.answer)
        shuffle(answer_list)
        self.options = dict(zip(['A', 'B', 'C', 'D'], answer_list))


def get_question():
    resp = requests.get(API_URL)
    resp.raise_for_status()
    jdata = resp.json()
    if jdata['response_code'] == 0:
        jdata = jdata['results'][0]
    else:
        raise Exception('Unable to connect to OpenTriviaDB.')
    return Question(jdata)


def get_callback(question):
    async def handler(message, sid):
        response = message.content.upper()
        if response in question.options:
            if question.options[response] == question.answer:
                embed = discord.Embed(color=theme_color, title=':white_check_mark: Correct! :white_check_mark:')
                embed.set_footer(text='Powered by OpenTriviaDB')
                await client.send_message(message.channel, embed=embed)
                session.remove_session(message.server.id, sid)
            else:
                embed = discord.Embed(color=theme_color, title=':x: Incorrect. :x:')
                embed.set_footer(text='Powered by OpenTriviaDB')
                await client.send_message(message.channel, embed=embed)
        elif message.content == get_server_prefix(message.server) + 'trivia answer':
            embed = discord.Embed(color=theme_color, title='Answer')
            embed.description = '**%s.** %s' % ([x for x in question.options if question.options[x] == question.answer][0], question.answer)
            embed.set_footer(text='Powered by OpenTriviaDB')
            await client.send_message(message.channel, embed=embed)
            session.remove_session(message.server.id, sid)
    return handler

