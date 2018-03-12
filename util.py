import discord
import pickle
import os

client = discord.Client()

servers = {}


def get_server_prefix(server):
    if server in servers.keys():
        return servers[server].prefix
    else:
        servers[server] = DiscordServer()
        cache_data()
        return '!'


def set_server_prefix(server, prefix):
    servers[server].prefix = prefix
    cache_data()


def cache_data():
    with open('cache/servers.pickle', 'bw+') as file:
        pickle.dump(servers, file)


class DiscordServer:
    def __init__(self):
        self.prefix = '!'
        self.hack_bans = []


token = open('token.txt').read()

theme_color = 2927584

error_color = 12200474


if os.path.isfile('cache/servers.pickle'):
    with open('cache/servers.pickle', 'rb') as p_file:
        servers = pickle.load(p_file)


