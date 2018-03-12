from datetime import datetime


def log(server_id, message):
    string = '[%s]: %s - %s' % (datetime.now().strftime('%b %d %H:%M:%S'), server_id, message)
    print(string)

