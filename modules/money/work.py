import json
from random import randint
import delays
from datetime import datetime, timedelta


def get_rand_job(channel_message):
    timer = delays.get_delay(channel_message.server, channel_message.author, 'work')
    if timer:
        if datetime.now() < timer:
            raise Exception(str((timer - datetime.now()).seconds // 60) + ' minutes')
        else:
            delays.remove_delay(channel_message.server, channel_message.author, 'work')
    with open('modules/money/jobs.json') as file:
        jdata = json.load(file)
        file.close()
    job = jdata['jobs'][randint(0, len(jdata['jobs']) - 1)]
    msg = 'You work as a %s. You earn `$%d`.' % (job['name'], job['salary'])
    delays.set_delay(channel_message.server, channel_message.author, 'work', datetime.now() + timedelta(minutes=30))
    return msg, job['salary']
