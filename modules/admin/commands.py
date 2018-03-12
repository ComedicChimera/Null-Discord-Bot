from command import command
from util import client, error_color, servers
from discord import Embed
from inspect import signature


def admin_command(coro):
    async def wrapper(message, args):
        try:
            if len(signature(coro).parameters) > 1:
                await coro(message, args)
            else:
                await coro(message)
        except AssertionError:
            await client.send_message(message.channel, embed=Embed(color=error_color, description='You do not have permission to use this command.'))
    return wrapper


@command('purge')
@admin_command
async def purge_message(message, args):
    assert message.author.server_permissions.manage_messages
    if not args.isdigit():
        await client.send_message(message.channel, embed=Embed(color=error_color, description='Message count must be an integer.'))
        return
    count = int(args)
    if count > 20:
        await client.send_message(message.channel, embed=Embed(color=error_color, description='You may not remove more than 20 messages at a time.'))
    elif count < 1:
        await client.send_message(message.channel, embed=Embed(color=error_color, description='You must purge at least 1 message.'))
    await client.purge_from(message.channel, limit=count + 1)


@command('kick')
@admin_command
async def kick(message):
    assert message.author.server_permissions.kick_members
    if len(message.mentions) != 1:
        await client.send_message(message.channel, embed=Embed(color=error_color, description='You may only kick exactly 1 member.'))
    await client.kick(message.mentions[0])
    await client.send_message(message.channel, 'Kicked `%s`.' % message.mentions[0])


@command('ban')
@admin_command
async def ban(message):
    assert message.author.server_permissions.ban_members
    if len(message.mentions) != 1:
        await client.send_message(message.channel, embed=Embed(color=error_color, description='You may only ban exactly 1 member.'))
    await client.ban(message.mentions[0])
    await client.send_message(message.channel, 'Banned `%s`.' % message.mentions[0])


@command('hackban')
@admin_command
async def hack_ban(message):
    assert message.author.server_permissions.ban_members
    if len(message.mentions) != 1:
        await client.send_message(message.channel, embed=Embed(color=error_color, description='You may only hack ban exactly 1 member.'))
    await client.ban(message.mentions[0])
    servers[message.server].hack_bans.append(message.mentions[0].id)
    await client.send_message(message.channel, 'Hack banned `%s`.' % message.mentions[0])


@command('unban')
@admin_command
async def unban(message, args):
    assert message.author.server_permissions.ban_members
    bans = await client.get_bans(message.server)
    for item in bans:
        if str(item) == args:
            await client.unban(item)
            if item.id in servers[message.server].hack_bans:
                servers[message.server].pop(servers[message.server].index(item.id))
            await client.send_message('Unbanned `%s`.' % item)
            break
    else:
        await client.send_message(message.channel, embed=Embed(color=error_color, description='Unable to find banned member by name `%s`.' % args))



