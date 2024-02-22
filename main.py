import discord
from discord.ext import commands
from datetime import timedelta
from discord.utils import get
import nacl
import traceback
import time
import random


ch = 1  # Счет обычных голосовых каналов
pr_ch = 0  # Счет приватных голосовых каналов
pr_cat_ch = 0  # Для предотвращения создания 2 категорий приватных каналов
id_voice_channel = []


intents = discord.Intents.all()
intents.typing = False
intents.presences = False
intents.members = True
permissions = discord.Permissions()
bot = commands.Bot(command_prefix='!', intents = intents)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('-' * 100)


@bot.event
async def on_guild_join(guild):                                                                                         # Начальная настройка на сервере
    emb = discord.Embed(color = 0x22ff00, title = f"Привет всему серверу {guild.name}")
    await guild.text_channels[1].send(embed=emb)

    role_eo = discord.utils.get(guild.roles, name='@everyone')
    permissions.update(create_instant_invite=False, kick_members=False, ban_members=False,
                       administrator=False, manage_channels=False, manage_guild=False,
                       add_reactions=False, view_audit_log=False, priority_speaker=False,
                       stream=False,
                       read_messages=False, view_channel=True, send_messages=False,
                       send_tts_messages=False, manage_messages=False,
                       embed_links=False, attach_files=False, read_message_history=False, mention_everyone=False,
                       external_emojis=False,
                       use_external_emojis=False, view_guild_insights=False, connect=False, speak=False,
                       mute_members=False, deafen_members=False,
                       move_members=False, use_voice_activation=False, change_nickname=False,
                       manage_nicknames=False,
                       manage_roles=False,
                       manage_permissions=False, manage_webhooks=False, manage_emojis=False,
                       manage_emojis_and_stickers=False,
                       use_application_commands=False, request_to_speak=False, manage_events=False,
                       manage_threads=False, create_public_threads=False,
                       create_private_threads=False, external_stickers=False, use_external_stickers=False,
                       send_messages_in_threads=False,
                       use_embedded_activities=False, moderate_members=False)
    await role_eo.edit(reason=None, permissions=permissions)


    role = await guild.create_role(name="В ожидании тиммейтов", hoist=True, color = 0xff0000)
    permissions.update(create_instant_invite=True, kick_members=False, ban_members=False,
                       administrator=False, manage_channels=False, manage_guild=False,
                       add_reactions=True, view_audit_log=False, priority_speaker=False,
                       stream=True,
                       read_messages=True, view_channel=True, send_messages=True,
                       send_tts_messages=True, manage_messages=False,
                       embed_links=True, attach_files=True, read_message_history=True, mention_everyone=True,
                       external_emojis=True,
                       use_external_emojis=True, view_guild_insights=True, connect=True, speak=True,
                       mute_members=False, deafen_members=False,
                       move_members=False, use_voice_activation=True, change_nickname=False,
                       manage_nicknames=False,
                       manage_roles=False,
                       manage_permissions=False, manage_webhooks=False, manage_emojis=False,
                       manage_emojis_and_stickers=True,
                       use_application_commands=True, request_to_speak=True, manage_events=True,
                       manage_threads=True, create_public_threads=False,
                       create_private_threads=True, external_stickers=True, use_external_stickers=True,
                       send_messages_in_threads=True,
                       use_embedded_activities=True, moderate_members=False)
    await role.edit(reason=None, permissions=permissions)


    role = await guild.create_role(name = "Регистрация", hoist=True)
    permissions.update(create_instant_invite=False, kick_members=False, ban_members=False,
                       administrator=False, manage_channels=False, manage_guild=False,
                       add_reactions=False, view_audit_log=False, priority_speaker=False,
                       stream=False,
                       read_messages=False, view_channel=False, send_messages=False,
                       send_tts_messages=False, manage_messages=False,
                       embed_links=False, attach_files=False, read_message_history=False, mention_everyone=False,
                       external_emojis=False,
                       use_external_emojis=False, view_guild_insights=False, connect=False, speak=False,
                       mute_members=False, deafen_members=False,
                       move_members=False, use_voice_activation=False, change_nickname=False,
                       manage_nicknames=False,
                       manage_roles=False,
                       manage_permissions=False, manage_webhooks=False, manage_emojis=False,
                       manage_emojis_and_stickers=False,
                       use_application_commands=False, request_to_speak=False, manage_events=False,
                       manage_threads=False, create_public_threads=False,
                       create_private_threads=False, external_stickers=False, use_external_stickers=False,
                       send_messages_in_threads=False,
                       use_embedded_activities=False, moderate_members=False)
    await role.edit(reason=None, permissions=permissions)




@bot.event
async def on_member_join(member):                                                                                       # Присвоение роли регистрация
    global role_reg, role_wait

    guild = bot.get_guild(member.mutual_guilds[0].id)
    role_reg = discord.utils.get(member.guild.roles, name = 'Регистрация')
    role_wait = discord.utils.get(member.guild.roles, name = 'В ожидании тиммейтов')
    await member.add_roles(role_reg)
    emb = discord.Embed(title=f"Привет {member.name}, добро пожаловать на наш сервер",
                            description="1: На сервере есть твоя команда\n2: Если тут у тебя еще нет команды\n3: Если ты ищешь команду",
                        color=0x22ff00)
    # emb.set_footer(text = 'йцу')
    await member.send(embed=emb)


@bot.event
async def on_message(message):                                                                                          # Функция обрабатывающаяя сообщения
    global role_reg, role_wait

    type_chat = str(message.channel.type)
    member = bot.get_user(message.author.id)
    guild = bot.get_guild(member.mutual_guilds[0].id)
    member_guild = guild.get_member(member.id)
    msg = message.content
    having_command = having_choice_command = 0
    roles = []
    for i in guild.roles:
        roles.append(i)

    emb_hi = discord.Embed(
        title=f"1: Если здесь тебя кто-то ждет\n2: Если тут у тебя еще нет команды\n3: Если ты хочешь к кому-то в команду",
        description='',
        color=0x22ff00)


    if type_chat == "private" and member_guild.roles[1].name == "Регистрация":                                          # Регистрация пользователя
        def check(message):
            return message.author.id == member.id


        def check_3(message):
            if message.author.id == member.id:
                message.content = int(message.content) + 10
                return message.content

        if msg == '1':                                                                                                  # Если ответ положительный
            emb = discord.Embed(title="Напиши название команды из предложенного списка", color = 0x64e2e4)
            for i in guild.roles:
                a = i.name.split()
                if a[0] == "Команда:":
                    ch = 0
                    for j in i.members:
                        ch += 1
                    emb.add_field(name=str(i.name), value=f"Количество: {ch}")
            await member.send(embed=emb)

            choice_command = await bot.wait_for('message', check = check)
            choice_command = choice_command.content
            for role in enumerate(roles):
                if choice_command in str(role[1]):
                    a = str(role[1]).split(' ', 1)
                    if a[1] == choice_command or choice_command == str(role[1]):
                        await member_guild.add_roles(role[1])
                        await member.send(f'Теперь ты в команде "{choice_command}"!')
                        await member_guild.remove_roles(role_reg)
                        having_choice_command = 1
                        break

            if having_choice_command == 0:
                await member.send(f'Такой команды нет, создай свою или попробуй снова!')
                time.sleep(2)
                await member.send(embed=emb_hi)


        if msg == '2':                                                                                                  # Если ответ отрицательный
            await member.send(f'Придумай название своей команды')
            command_name = await bot.wait_for('message', check = check)
            command_name = command_name.content

            if len(command_name) <= 1:                                                                                  # Проверка на минимальный размер названия команды
                await member.send('Название команды не должно быть коротким или пустым')
                time.sleep(2)
                await member.send(embed=emb_hi)

            elif len(command_name) > 1:                                                                                 # Создание роли и присвоение её
                for role in enumerate(roles):
                    if command_name in str(role[1]):
                        await member.send(f'Команда "{command_name}" уже есть')
                        time.sleep(2)
                        await member.send(embed=emb_hi)
                        having_command = 1
                if having_command == 0:
                    await member_guild.edit(nick = member.name + " 👑")
                    rgb = random.randint(0, 16777215)
                    role = await guild.create_role(name="Команда: " + command_name, hoist=True, colour = discord.Colour(rgb))
                    permissions.update(create_instant_invite=True, kick_members=False, ban_members=False,
                                       administrator=False, manage_channels=False, manage_guild=False,
                                       add_reactions=True, view_audit_log=False, priority_speaker=False,
                                       stream=True,
                                       read_messages=True, view_channel=True, send_messages=True,
                                       send_tts_messages=True, manage_messages=False,
                                       embed_links=True, attach_files=True, read_message_history=True, mention_everyone=True,
                                       external_emojis=True,
                                       use_external_emojis=True, view_guild_insights=True, connect=True, speak=True,
                                       mute_members=False, deafen_members=False,
                                       move_members=False, use_voice_activation=True, change_nickname=False,
                                       manage_nicknames=False,
                                       manage_roles=False,
                                       manage_permissions=False, manage_webhooks=False, manage_emojis=False,
                                       manage_emojis_and_stickers=True,
                                       use_application_commands=True, request_to_speak=True, manage_events=True,
                                       manage_threads=True, create_public_threads=False,
                                       create_private_threads=True, external_stickers=True, use_external_stickers=True,
                                       send_messages_in_threads=True,
                                       use_embedded_activities=True, moderate_members=False)

                    await role.edit(reason=None, permissions=permissions)
                    await member_guild.add_roles(role)
                    await member_guild.send(f'Поздравляю теперь ты капитан команды "{command_name}"')
                    await member_guild.remove_roles(role_reg)
        if msg == '3':                                                                                                  #Поиск группы
            await member.send(f'Напиши среднее количество ммр')
            mmr = await bot.wait_for('message', check = check)
            mmr = int(mmr.content)

            await member.send('На какой позиции играешь?')
            position = await bot.wait_for('message', check=check_3)
            position = int(position.content)
            if position - 10 > 15 or position - 10 <= 0:
                await member.send('Ты же понимаешь что нет такой роли...')
                time.sleep(2)
                await member.send(embed = emb_hi)
            else:
                permissions.update(create_instant_invite=False, kick_members=False, ban_members=False,
                                   administrator=False, manage_channels=False, manage_guild=False,
                                   add_reactions=False, view_audit_log=False, priority_speaker=False,
                                   stream=False,
                                   read_messages=False, view_channel=False, send_messages=False,
                                   send_tts_messages=False, manage_messages=False,
                                   embed_links=False, attach_files=False, read_message_history=False,
                                   mention_everyone=False,
                                   external_emojis=False,
                                   use_external_emojis=False, view_guild_insights=False, connect=False, speak=False,
                                   mute_members=False, deafen_members=False,
                                   move_members=False, use_voice_activation=False, change_nickname=False,
                                   manage_nicknames=False,
                                   manage_roles=False,
                                   manage_permissions=False, manage_webhooks=False, manage_emojis=False,
                                   manage_emojis_and_stickers=False,
                                   use_application_commands=False, request_to_speak=False, manage_events=False,
                                   manage_threads=False, create_public_threads=False,
                                   create_private_threads=False, external_stickers=False,
                                   use_external_stickers=False,
                                   send_messages_in_threads=False,
                                   use_embedded_activities=False, moderate_members=False)
                role_mmr = discord.utils.get(member_guild.guild.roles, name = "ПТС: " + str(mmr))
                role_position = discord.utils.get(member_guild.guild.roles, name = "Поз: " + str(position - 10))

                if role_mmr == None:
                    role_mmr = await guild.create_role(name="ПТС: " + str(mmr), color = 0xff0000)
                    await role_mmr.edit(reason=None, permissions=permissions)
                    await member_guild.add_roles(role_mmr)
                else:
                    await member_guild.add_roles(role_mmr)

                if role_position == None:
                    role_mmr = await guild.create_role(name="Поз: " + str(position - 10), color = 0xff0000)
                    await role_mmr.edit(reason=None, permissions=permissions)
                    await member_guild.add_roles(role_mmr)
                else:
                    await member_guild.add_roles(role_position)

                await member_guild.add_roles(role_wait)
                await member_guild.remove_roles(role_reg)
                await member.send("Успех, ожидай свою команду!")
    await bot.process_commands(message)


@bot.command()
async def help(ctx):                                                                                                    # Список команд
    await ctx.channel.purge(limit = 1)
    PREFIX = "!"
    emb = discord.Embed(title= "Навигация по командам")
    emb.add_field(name ='{}clear'.format(PREFIX), value = 'Очистить чат:\n !clear: <кол-во>')
    emb.add_field(name='{}new_capitan'.format(PREFIX), value='Поменять капитана: !new_capitan <@ник>')
    emb.add_field(name='{}mute'.format(PREFIX), value='Замьютить игрока своей команды: !mute <@ник> <секунды> <Причина>')
    emb.add_field(name='{}change_name_team'.format(PREFIX), value='Поменять название команды:\n !change_name_team <Название>')
    emb.add_field(name='{}new_nick'.format(PREFIX), value='Поменять ник участника:\n !new_nick <@ник> <ник>')
    emb.add_field(name='{}invite'.format(PREFIX), value='Пригласить участника:\n !invite <@ник>')
    await ctx.send(embed=emb)


@bot.command()                                                                                                          # Смена капитана
async def invite(ctx, wait_member: discord.Member):
    cap = ctx.author
    new_invite_team = ''
    def check(message):
        return message.author.id == wait_member.id

    if ctx.author.nick[-1] == '👑':
        for i in cap.roles:
            a = i.name.split()
            if a[0] == "Команда:":
                await ctx.send(f'{wait_member.mention}, Вам пришло приглашение об встулении в группу {a[1]}, вы согласны?')
                new_invite_team = i
                break

        arg_n = await bot.wait_for('message', check=check)
        arg = arg_n.content
        if arg == 'Да':
            for i in wait_member.roles:
                if i.name != '@everyone':
                    await wait_member.remove_roles(i)
            await wait_member.add_roles(new_invite_team)
            await ctx.send("Поздравляю теперь ты в команде!")
        elif arg == 'Нет':
            await ctx.send(f'Отмена команды')
        else:
            await ctx.send(f'Ответ неясен, попробуй снова')
    else:
        await ctx.send(f'Ты не капитан какой либо команды')




@commands.has_permissions(administrator = True)
@bot.command()                                                                                                          # Очистка чата
async def clear(ctx, amount=1000):
    await ctx.channel.purge(limit = amount)


@bot.command()                                                                                                          # Смена капитана
async def new_capitan(ctx, new_capitan: discord.Member):
    old_capitan = ctx.author
    def check(user):
        return user.author.id == old_capitan.id

    for i, j in zip(old_capitan.roles, new_capitan.roles):
        if "Команда:" in i.name and "Команда:" in j.name:
            rol, rol1 = i.id, j.id
            break
    if old_capitan.nick[-1] == "👑" and rol == rol1:
        await ctx.send("Ты уверен что хочешь передать роль капитана?")
        arg = await bot.wait_for('message', check=check)
        arg = arg.content
        if arg == "Да":
            await old_capitan.edit(nick=old_capitan.name)
            await new_capitan.edit(nick=new_capitan.name + " 👑")
            await ctx.send("Успех!")
        elif arg == "Нет":
            await ctx.send("Ну ок")
        else:
            await ctx.send(f'Ответ неясен, попробуй снова')
    else:
        await ctx.send("Ты не капитан какой либо команды, либо не в той команде")


@bot.command()
async def mute(ctx, member: discord.Member, time: int, reason = 'отдых'):                                               # Мут участника команды
    if time < 86400:
        for i, j in zip(ctx.author.roles, member.roles):
            if "Команда:" in i.name and "Команда:" in j.name:
                rol, rol1 = i.id, j.id
                break
        if ctx.author.nick[-1] == '👑' and rol == rol1:
            duration = timedelta(seconds=time)
            await member.timeout(duration)
            await ctx.send(f'Участник {member.mention} был замьючен.\nПричина: {reason}')
        else:
            await ctx.send(f'Ошибка!')
    else:
        await ctx.send(f'Отказ!\nНе более одного дня')


@bot.command(pass_context=True)                                                                                         # Смена названия команды
async def change_name_team(ctx, arg):
    new_name = arg
    def check(user):
        return user.author.id == ctx.message.author.id

    if ctx.author.nick[-1] == '👑':
        await ctx.send(f'Вы действительно хотите изменить название команды на {arg} ?')
        arg = await bot.wait_for('message', check = check)
        arg = arg.content
        if arg == 'Да':
            for i in ctx.author.roles:
                if "Команда: " in i.name:
                    await i.edit(name = 'Команда: ' + new_name)
                    await ctx.send(f'Успех!')
                    break
        elif arg == 'Нет':
            await ctx.send(f'Тогда в следующий раз')
        else:
            await ctx.send(f'Ответ неясен, попробуй снова')
    else:
        await ctx.send(f'Ты не капитан какой либо команды')


@bot.command()                                                                                                          # Смена капитана
async def new_nick(ctx, member: discord.Member, nick: str):
    cap = ctx.author
    def check(message):
        return message.author.id == member.id

    if ctx.author.nick[-1] == '👑':
        await ctx.send(f'{member.mention}, вы действительно хотите изменить ник на "{nick}"?')
        arg_n = await bot.wait_for('message', check = check)
        arg = arg_n.content
        if '👑' not in nick:
            if arg == 'Да':
                if cap.id == arg_n.author.id:
                    await member.edit(nick=nick + " 👑")
                    await ctx.send("Успех!")
                else:
                    for i, j in zip(ctx.author.roles, member.roles):
                        if "Команда:" in i.name and "Команда:" in j.name:
                            await member.edit(nick = nick)
                            await ctx.send("Успех!")
            elif arg == 'Нет':
                await ctx.send(f'Отмена команды')
            else:
                await ctx.send(f'Ответ неясен, попробуй снова')
        else:
            await ctx.send(f'Ты не можешь сделать такой ник')
    else:
        await ctx.send(f'Ты не капитан какой либо команды')


@bot.event
async def on_voice_state_update(member, before, after):                                                                 # Создание и удаление голосовых каналов
    global id_voice_channel
    if after.channel and after.channel != before.channel:
        channel = after.channel
        guild = member.guild
        category = channel.category

        if len(channel.members) != 0 and channel.name == "Создать канал":
            for member in after.channel.members:
                for i in member.roles:
                    a = i.name.split()
                    if a[0] == "Команда:":
                        time.sleep(0.2)
                        new_channel = await guild.create_voice_channel(f"{a[1]}", category = category)
                        id_voice_channel.append(new_channel.id)
                        await member.move_to(new_channel)
                        break

    if before.channel and after.channel != before.channel:
        del_channel = before.channel
        if del_channel.name != "Создать канал" and len(del_channel.members) == 0:
            for i in id_voice_channel:
                if i == del_channel.id:
                    id_voice_channel.remove(i)
            await del_channel.delete()



# @bot.event
# async def on_guild_remove(guild):
#     role_reg = discord.utils.get(guild.roles, name = 'Регистрация')
#     await role_reg.delete()





bot.run('')


