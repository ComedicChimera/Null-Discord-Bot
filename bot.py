import util
from command import process_command
import session as discord_session
import filters
from discord import Embed
from logger import log


@util.client.event
async def on_message(message):
    if message.author.bot:
        return

    try:
        await handle_message(message)
    except Exception as e:
        log(message.server.id, str(e))
        await util.client.send_message(message.channel, embed=Embed(color=util.error_color, description='An unknown error occurred.'))


@util.client.event
async def on_server_join(server):
    embed = Embed(color=util.theme_color, title='Null Bot')
    embed.description = 'Null is a fully featured, powerful, multipurpose Discord bot from easy use on any server.'
    embed.add_field(name='Get Started', value='Use `!help` to get list of command and how to use them.', inline=False)
    embed.add_field(name='Support', value='**Donate** donate_url\n**Source** github_url\n**Upvote** upvote_url', inline=False)
    embed.add_field(name='Join our Discord', value='discord_url', inline=False)
    icon_url = 'https://cdn.discordapp.com/avatars/226732838181928970/19562db0c14f445ac5a0bf8f605989c1.png?size=128'
    embed.set_footer(text='Developed by ComedicChimera#3451', icon_url=icon_url)
    await util.client.send_message(server.default_channel, embed=embed)


@util.client.event
async def on_member_join(member):
    print(util.servers[member.server].__dict__)
    if member.id in util.servers[member.server].hack_bans:
        await util.client.kick(member)
    else:
        await util.client.send_message(member.server.default_channel, 'Welcome `%s`!' % member.name)


async def handle_message(message):
    prefix = util.get_server_prefix(message.server)
    # use custom input handler if specified
    if discord_session.has_session(message.server, message.channel, message.author):
        await util.client.send_typing(message.channel)
        s = discord_session.get_session(message.server, message.channel, message.author)
        await s.handler(message, s.session_id)
    # else pass to command handler
    elif message.content.startswith(prefix):
        await process_command(message, prefix)
    # apply filters
    elif filters.match_filters(message):
        await util.client.delete_message(message)


if __name__ == '__main__':
    # imported command sets
    import modules.general.commands
    import modules.music.commands
    import modules.math.commands
    import modules.internet.commands
    import modules.money.commands
    import modules.games.commands
    import modules.admin.commands

    # start the bot
    util.client.run(util.token)
