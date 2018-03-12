from inspect import signature
from util import client


# dictionary used to hold active commands
commands = {

}


# used to map commands
def command(name):
    # decorator never actually applied
    def decorator(func):
        commands[name] = func

        # empty wrapper
        def wrapper():
            pass
        return wrapper
    return decorator


# used to activate command
async def process_command(msg, prefix):
    cmd = msg.content.split(' ')[0][len(prefix):]
    if cmd in commands.keys():
        await client.send_typing(msg.channel)
        if len(signature(commands[cmd]).parameters) > 1:
            await commands[cmd](msg, msg.content[len(prefix) + len(cmd) + 1:])
        else:
            await commands[cmd](msg)
