from random import randint


# sessions organized by guild
sessions = {

}


# input session
class Session:
    def __init__(self, users, channel, handler):
        self.session_id = self._generate_id()
        self.users = users
        self.channel = channel
        self.handler = handler

    @staticmethod
    def _generate_id():
        sid = ''
        for _ in range(0, 20):
            c = randint(33, 126)
            sid += chr(c)
        return sid


# create a new input session
def create_session(server, channel, users, handler):
    session = Session(users, channel, handler)
    if server in sessions:
        sessions[server].append(session)
    else:
        sessions[server] = [session]


# remove a session from the sessions
def remove_session(server, sid):
    if server in sessions:
        for session in sessions[server]:
            if session.session_id == sid:
                sessions[server].pop(sessions[server].index(session))
                break
        else:
            raise KeyError('Invalid session id.')
    else:
        raise KeyError('Invalid server.')


# if session exists
def has_session(server, ch, user):
    if server.id in sessions:
        for session in sessions[server.id]:
            if str(user) in session.users and session.channel == ch:
                return True
    return False


# get session
def get_session(server, ch, user):
    for session in sessions[server.id]:
        if str(user) in session.users and session.channel == ch:
            return session
