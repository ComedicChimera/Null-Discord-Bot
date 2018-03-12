import pickle
import os


balances = {

}

if os.path.isfile('cache/balances.pickle'):
    with open('cache/balances.pickle', 'rb') as b_file:
        balances = pickle.load(b_file)
        b_file.close()


def add_balance(server, user, amount):
    if hasattr(user, 'name'):
        user = str(user)
    if amount < 0:
        raise ValueError('Cannot add negative value to balance.')
    if server.id not in balances:
        balances[server.id] = {user: amount}
    elif user not in balances[server.id]:
        balances[server.id][user] = amount
    else:
        balances[server.id][user] += amount
    cache_balances()


def remove_balance(server, user, amount):
    if hasattr(user, 'name'):
        user = str(user)
    if amount < 0:
        raise ValueError('Cannot remove negative value from balance.')
    bal = balances[server.id][user]
    if bal - amount < 0:
        raise ValueError('Unable to deduct amount from balance.')
    balances[server.id][user] -= amount
    cache_balances()


def cache_balances():
    with open('cache/balances.pickle', 'bw+') as file:
        pickle.dump(balances, file)
        file.close()


def get_balance(server, user):
    if hasattr(user, 'name'):
        user = str(user)
    return balances[server.id][user]
