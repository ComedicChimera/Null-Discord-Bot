from command import command
from util import client, theme_color, error_color
import modules.money.slots as slots
import modules.money.balance as balance
import discord
import modules.money.work as work
import delays
from datetime import datetime, timedelta
from random import randint


@command('slots')
async def play_slots(message, args):
    try:
        result, rows = slots.play()
        bet = False
        if args != '':
            if not args.isdigit():
                raise Exception('Amount must be a number.')
            base = float(args)
            balance.remove_balance(message.server, message.author, base)
            if result:
                balance.add_balance(message.server, message.author, base * 2)
            bet = True
        text = ''
        for i in range(len(rows)):
            if i == 1:
                if result:
                    msg = 'moneybag: **You won!** :moneybag:'
                else:
                    msg = ':x: **You lost.** :x:'
                text += ':arrow_forward: %s :arrow_backward:   %s\n' % (rows[i], msg)
            else:
                text += ':black_large_square: %s :black_large_square:\n' % rows[i]
        embed = discord.Embed(color=theme_color, description=text)
        if bet:
            embed.set_footer(text='Balance: $%d' % balance.get_balance(message.server, message.author))
        await client.send_message(message.channel, embed=embed)
    except KeyError:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='Unable to deduct amount from balance.'))
    except Exception as e:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description=str(e)))


@command('work')
async def do_work(message):
    try:
        msg, val = work.get_rand_job(message)
    except Exception as e:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='You must wait until %s to work.' % e))
        return
    balance.add_balance(message.server, message.author, val)
    await client.send_message(message.channel, embed=discord.Embed(color=theme_color, description=msg))


@command('give')
async def give_money(message, args):
    try:
        split_args = args.split(' ')
        if len(split_args) != 2:
            raise ValueError('The give command accepts two arguments.')
        if len(message.mentions) != 1:
            raise ValueError('Only mention one user per give command.')
        if not split_args[-1].isdigit():
            raise ValueError('Invalid amount.')
        amount = float(split_args[-1])
        balance.remove_balance(message.server, message.author, amount)
        balance.add_balance(message.server, message.mentions[0], amount)
        await client.send_message(message.channel, '%s gave %s `$%d`.' % (message.author, str(message.mentions[0]), amount))
    except ValueError as ve:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description=str(ve)))
    except KeyError:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='User account doesn\'t exist.'))
    except Exception:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='Unable to perform operation.'))


@command('balance')
async def get_balance(message, args):
    try:
        if args != '':
            user = args
        else:
            user = message.author
        bal = balance.get_balance(message.server, user)
        embed = discord.Embed(color=theme_color, title='Balance', description='`$%d`' % bal)
        await client.send_message(message.channel, embed=embed)
    except KeyError:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='User doesn\'t have a balance or doesn\'t exist.'))


@command('dailies')
async def get_dailies(message):
    timer = delays.get_delay(message.server, message.author, 'dailies')
    if timer:
        if timer > datetime.now():
            time_diff = (timer - datetime.now())
            time_str = '%s hours and %s minutes' % (time_diff.seconds // 3600, (time_diff.seconds // 60) % 60)
            await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='You must wait %s before you can receive dailies.' % time_str))
            return
        else:
            delays.remove_delay(message.server, message.author, 'dailies')
    rand = randint(20, 80)
    balance.add_balance(message.server, message.author, rand)
    embed = discord.Embed(color=theme_color, description=':dollar: You got `$%d`! :dollar:' % rand)
    embed.set_footer(text='Balance: $%d' % balance.get_balance(message.server, message.author))
    await client.send_message(message.channel, embed=embed)
    delays.set_delay(message.server, message.author, 'dailies', datetime.now() + timedelta(days=1))


@command('steal')
async def steal(message, args):
    timer = delays.get_delay(message.server, message.author, 'steal')
    if timer:
        if timer > datetime.now():
            time_diff = (timer - datetime.now()).seconds // 60
            if time_diff > 59:
                time_diff = (timer - datetime.now())
                time_str = '%d days, %d hours, and %d minutes' % (time_diff.days, time_diff.seconds // 360 % 24, time_diff.seconds // 60 % 60)
                await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='Your remaining jail time is %s.' % time_str))
            else:
                await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='You must wait %d minutes before you can steal again.' % time_diff))
            return
        else:
            delays.remove_delay(message.server, message.author, 'steal')
    split_args = args.split(' ')
    if not split_args[-1].isdigit():
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='Invalid amount.'))
        return
    if len(message.mentions) != 1:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='Only one mention per theft.'))
        return
    try:
        victim_bal = balance.get_balance(message.server, message.mentions[0])
    except KeyError:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='Victim does not have enough money.'))
        return
    amount = float(split_args[-1])
    if victim_bal - amount < 0:
        await client.send_message(message.channel, embed=discord.Embed(color=error_color, description='Victim does not have enough money.'))
        return
    fine = randint(0, amount * 3)
    if fine == 0:
        balance.remove_balance(message.server, message.mentions[0], amount)
        balance.add_balance(message.server, message.author, amount)
        embed = discord.Embed(title='Theft Successful', description='You stole `$%d` from %s.' % (amount, message.mentions[0].name))
        embed.set_footer(text='Balance: $%d' % balance.get_balance(message.server, message.author))
        await client.send_message(message.channel, embed=embed)
    else:
        try:
            balance.remove_balance(message.server, message.author, fine)
            bal = balance.get_balance(message.server, message.author)
            embed = discord.Embed(title='Theft Failed.', description='You were fined $`%d`.' % fine, color=theme_color)
            embed.set_footer(text='Balance: $%d' % bal)
            await client.send_message(message.channel, embed=embed)
        except ValueError:
            bal = balance.get_balance(message.server, message.author)
            balance.remove_balance(message.server, message.author, bal)
            embed = discord.Embed(title='Theft Failed.', description='You were fined `$%d` and put in jail for 1 day.' % bal, color=theme_color)
            embed.set_footer(text='Balance: $0')
            await client.send_message(message.channel, embed=embed)
            delays.set_delay(message.server, message.author, 'steal', datetime.now() + timedelta(days=1))
            return
        except KeyError:
            await client.send_message(message.channel, discord.Embed(title='Theft Failed.',
                                                                     description='You were fined $0, but you were put in jail for 3 days.',
                                                                     color=theme_color
                                                                     ))
            delays.set_delay(message.server, message.author, 'steal', datetime.now() + timedelta(days=3))
            return
    delays.set_delay(message.server, message.author, 'steal', datetime.now() + timedelta(minutes=45))




