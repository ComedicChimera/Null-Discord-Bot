import pickle
import os


delays = {

}

if os.path.isfile('cache/delays.pickle'):
    with open('cache/delays.pickle', 'rb') as p_file:
        delays = pickle.load(p_file)


def set_delay(server, user, command, time):
    if hasattr(user, 'name'):
        user = str(user)
    server = server.id
    if server not in delays:
        delays[server] = {user: {command: time}}
    elif user not in delays[server]:
        delays[server][user] = {command: time}
    else:
        delays[server][user][command] = time
    cache_delays()


def remove_delay(server, user, command):
    delays[server.id][str(user)].pop(command, None)


def get_delay(server, user, command):
    try:
        return delays[server.id][str(user)][command]
    except KeyError:
        return


def cache_delays():
    with open('cache/delays.pickle', 'bw+') as file:
        pickle.dump(delays, file)
