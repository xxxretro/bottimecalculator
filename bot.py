from discord.ext import commands
import os

bot = commands.Bot(command_prefix='>>')


def instr(n):
    if len(str(n)) == 1:
        return f'0{n}'
    else:
        return f'{n}'


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(pass_context=True)
async def calctime(ctx, *arg):
    arg = list(arg)
    if arg[0] == '-nights':
        if len(arg) == 3:
            time_on_server = [int(arg[1].split(':')[0]), int(arg[1].split(':')[1])]
            time_in_msc = [int(arg[2].split(':')[0]), int(arg[2].split(':')[1])]
            if time_on_server[1] != 0:
                time_in_msc[1] += int(0.6 * (60 - time_on_server[1]) * 0.8)
                time_on_server[1] = 0
            time_table = []
            for i in range(180):
                if time_on_server[0] == 23:
                    time_table.append(
                        f'{instr(time_on_server[0])}:{instr(time_on_server[1])}'
                        f' - '
                        f'{instr(time_in_msc[0])}:{instr(time_in_msc[1])}'
                    )
                if time_in_msc[1] + 8 >= 60:
                    time_in_msc[1] = (time_in_msc[1] + 8) - 60
                    if time_in_msc[0] + 1 == 24:
                        time_in_msc[0] = 0
                    else:
                        time_in_msc[0] += 1
                else:
                    time_in_msc[1] += 8

                if time_on_server[0] + 1 == 24:
                    time_on_server[0] = 0
                else:
                    time_on_server[0] += 1

            for i in time_table:
                await ctx.send(i)
        else:
            await ctx.send('Что-то не то :thinking:\nДля получения справки о командах введите: >>showhelp')

    if arg[0] == '-exp':
        if len(arg) == 2:
            time = [int(arg[1].split(':')[0]), int(arg[1].split(':')[1])]
            time_table = []
            for i in range(8):
                time_table.append(f'{instr(time[0])}:{instr(time[1])}')
                if time[1] + 24 >= 60:
                    if time[0] + 4 >= 24:
                        time[0] = time[0] + 4 - 24
                    else:
                        time[0] += 4
                        time[1] = time[1] + 24 - 60
                else:
                    time[1] += 24
                    if time[0] + 3 >= 24:
                        time[0] = time[0] + 3 - 24
                    else:
                        time[0] += 3
            for i in time_table:
                await ctx.send(i)
        else:
            await ctx.send('Что-то не то :thinking:\nДля получения справки о командах введите: >>showhelp')


@bot.command()
async def showhelp(ctx):
    await ctx.send('Команды:'
                   '\n    >>showhelp - справка'
                   '\n    >>calctime - расчёт времени'
                   '\n        Вариации:'
                   '\n            -nights [время на сервере] [время в Москве]'
                   '\n            -exp [время запуска сервера(по МСК)]'
                   '\n            Примичание:'
                   '\n            Время на сервере желательно брать время формата: час:00, например 09:00, 17:00,'
                   ' иначе возникнет погрешность.'
                   ' Всё время указывается без квадратных скобок и в формате: "часы:минуты".')


bot.run(os.environ.get('BOT_TOKEN'))
