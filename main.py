from utils import flatten

import os
import discord
from dotenv import load_dotenv

import asyncio
from datetime import datetime, time, timedelta

from subject import Day, Semester, days, day_to_text, filter_subjects, get_semester, weekday_to_day
from timetable import get_timetable
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import io

from openai import OpenAI

mpl.rc('font', family='Noto Sans CJK JP')

load_dotenv()

token = os.getenv('TOKEN')

guild_id = int(os.getenv('GUILD_ID'))
notify_channel_id = int(os.getenv('CHANNEL_NOTIFY'))

current_years = int(os.getenv('CURRENT_YEARS'))
current_semester = get_semester(os.getenv('CURRENT_SEMESTER'))

times = [
    time(8, 40),
    time(9, 0),
    time(10, 20),
    time(10, 30),
    time(10, 40),
    time(12, 10),
    time(12, 40),
    time(13, 0),
    time(14, 30),
    time(14, 40),
    time(16, 0),
    time(16, 10),
    time(16, 20),
    time(17, 50),
]

async def action840():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('☀ おはようございます😀\n🎯 次の授業 1限 **9時00分**〜10時30分')

async def action900():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎬 1限 開始 **9時00分**〜10時30分')

    now = datetime.now()
    day = days[now.weekday()]
    await notify_tasks(current_years, current_semester, day, 1)

async def action1020():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎯 次の授業 2限 **10時40分**〜12時10分')

async def action1030():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('✅ 1限 終了 9時00分〜**10時30分**\n🎯 次の授業 2限 **10時40分**〜12時10分')

async def action1040():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎬 2限 開始 **10時40分**〜12時10分')

    now = datetime.now()
    day = days[now.weekday()]
    await notify_tasks(current_years, current_semester, day, 2)

async def action1210():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('✅ 2限 終了 10時40分〜**12時10分**\n🎯 次の授業 3限 **13時00分**〜14時30分')

async def action1240():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎯 次の授業 3限 **13時00分**〜14時30分')

async def action1300():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎬 3限 開始 **13時00分**〜14時30分')

    now = datetime.now()
    day = days[now.weekday()]
    await notify_tasks(current_years, current_semester, day, 3)

async def action1420():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎯 次の授業 4限 **14時40分**〜16時10分')

async def action1430():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('✅ 3限 終了 13時00分〜**14時30分**\n🎯 次の授業 4限 **14時40分**〜16時10分')

async def action1440():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎬 4限 開始 **14時40分**〜16時10分')

    now = datetime.now()
    day = days[now.weekday()]
    await notify_tasks(current_years, current_semester, day, 4)

async def action1600():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎯 次の授業 5限 **16時20分**〜17時50分')

async def action1610():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('✅ 4限 終了 14時40分〜**16時10分**\n🎯 次の授業 5限 **16時20分**〜17時50分')

async def action1620():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎬 5限 開始 **16時20分**〜17時50分')

    now = datetime.now()
    day = days[now.weekday()]
    await notify_tasks(current_years, current_semester, day, 5)

async def action1750():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('✅ 5限 終了 16時20分〜**17時50分**\n🎉 お疲れ様でした😊')

actions = {
    time(8, 40): action840,
    time(9, 0): action900,
    time(10, 20): action1020,
    time(10, 30): action1030,
    time(10, 40): action1040,
    time(12, 10): action1210,
    time(12, 40): action1240,
    time(13, 0): action1300,
    time(14, 20): action1420,
    time(14, 30): action1430,
    time(14, 40): action1440,
    time(16, 00): action1600,
    time(16, 10): action1610,
    time(16, 20): action1620,
    time(17, 50): action1750,
}

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

ai = OpenAI()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    bot.loop.create_task(loop())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    max_tokens = 1000

    if bot.user.mentioned_in(message):
        history = await get_message_history(message, [])
        print(history)

        content_types = [c['type'] for c in flatten(item['content'] for item in history)]
        to_use_gpt_4_vision_preview = 'image_url' in content_types
        model = 'gpt-4-vision-preview' if to_use_gpt_4_vision_preview else 'gpt-4-1106-preview'

        completion = ai.chat.completions.create(
            model=model,
            messages=history,
            max_tokens=max_tokens,
        )

        answer = completion.choices[0].message.content
        print(answer)

        await message.reply(answer)
    elif message.reference is not None:
        referenced_message = await message.channel.fetch_message(message.reference.message_id)

        if referenced_message.author == bot.user:
            history = await get_message_history(referenced_message, [])
            print(history)

            content_types = [c['type'] for c in flatten(item['content'] for item in history)]
            to_use_gpt_4_vision_preview = 'image_url' in content_types
            model = 'gpt-4-vision-preview' if to_use_gpt_4_vision_preview else 'gpt-4-1106-preview'

            completion = ai.chat.completions.create(
                model=model,
                messages=history,
                max_tokens=max_tokens,
            )

            answer = completion.choices[0].message.content
            print(answer)

@bot.slash_command(name = "timetable", description = "Generate timetable")
async def timetable(ctx, years: discord.Option(description='年'), semester: discord.Option(description='学期')):
    await ctx.defer()

    author = ctx.author
    roles = [role.name for role in author.roles]
    subjects = filter_subjects(roles)
    text_to_semester = {
        '前学期': Semester.FIRST,
        '後学期': Semester.SECOND,
    }
    timetable = get_timetable(subjects, int(years), text_to_semester[semester])

    df = pd.DataFrame(timetable)

    fig, ax = plt.subplots()

    ax.axis('off')

    table = ax.table(cellText=df.values, cellLoc='center', colLabels=df.columns, bbox=[0, 0, 1, 1])

    table.auto_set_font_size(False)
    table.set_fontsize(8)

    with io.BytesIO() as stream:
        plt.savefig(stream, format='png')
        stream.seek(0)
        await ctx.respond(file=discord.File(stream, 'image.png'))

async def loop():
    while True:
        next_notify_time, next_notify_datetime = get_next_notify_time()
        now = datetime.now()
        delay = (next_notify_datetime - now).total_seconds()

        print(f'Run after {delay} seconds...')
        await asyncio.sleep(delay)
        await actions[next_notify_time]()

def get_current_subject_roles(years: int, semester: Semester, day: Day, index: int):
    guild = get_guild()
    roles = [role.name for role in guild.roles]

    subjects = []
    for subject in filter_subjects(roles):
        if subject.years == years and subject.semester == semester and subject.day == day and index in subject.indexes:
            subjects.append(subject)

    subject_roles = [discord.utils.get(guild.roles, name=subject.role_name()) for subject in subjects]
    return subject_roles

def get_guild():
    guild = discord.utils.get(bot.guilds, id=guild_id)
    return guild

async def get_message_history(message, history, i=0):
    supported_exts = [
        '.gif',
        '.jpeg',
        '.jpg',
        '.png',
    ]
    if len(history) == 0:
        history.insert(0, {'role': 'user', 'content': [{'type': 'text', 'text': message.content}]})
        for attachment in message.attachments:
            for supported_ext in supported_exts:
                if attachment.filename.endswith(supported_ext):
                    history[0]['content'].append({'type': 'image_url', 'image_url': attachment.url})
                    break
        print(i, history)

        return await get_message_history(message, history, i + 1)
    elif message.reference is not None:
        referenced_message = await message.channel.fetch_message(message.reference.message_id)

        role = 'assistant' if referenced_message.author == bot.user else 'user'
        history.insert(0, {'role': role, 'content': [{'type': 'text', 'text': referenced_message.content}]})
        if role == 'user':
            for attachment in message.attachments:
                for supported_ext in supported_exts:
                    if attachment.filename.endswith(supported_ext):
                        history[0]['content'].append({'type': 'image_url', 'image_url': attachment.url})
                        break
        print(i, history)

        return await get_message_history(referenced_message, history, i + 1)
    else:
        history.insert(0, {'role': 'system', 'content': [{'type': 'text', 'text': 'あなたはアシスタントです。'}]})
        print(i, history)

        return history

def get_next_notify_time():
    now = datetime.now()

    is_saturday = now.weekday() == 5
    is_sunday = now.weekday() == 6

    if is_saturday:
        monday = now + timedelta(days=2)
        return times[0], datetime(monday.year, monday.month, monday.day, times[0].hour, times[0].minute)

    if is_sunday:
        monday = now + timedelta(days=1)
        return times[0], datetime(monday.year, monday.month, monday.day, times[0].hour, times[0].minute)

    for notify_time in times:
        notify_datetime = datetime(now.year, now.month, now.day, notify_time.hour, notify_time.minute)
        if notify_datetime > now:
            return notify_time, notify_datetime

    tomorrow = now + timedelta(days=1)
    return times[0], datetime(tomorrow.year, tomorrow.month, tomorrow.day, times[0].hour, times[0].minute)

async def notify_tasks(years: int, semester: Semester, day: Day, index: int):
    subject_roles = get_current_subject_roles(years, semester, day, index)

    now = datetime.now()
    formatted_date = now.strftime('%Y年%m月%d日')
    day_text = day_to_text[weekday_to_day[now.weekday()]]

    indexes_text = f'{index}限'

    mentions = ' '.join([subject_role.mention for subject_role in subject_roles])
    mentions_text = mentions if mentions else '(なし)'

    reactions = {'出席': '👋', '課題': '✍️'}

    message_text  = f'''## 🗒️ {formatted_date}{day_text}{indexes_text}のタスク
**授業**: {mentions_text}
**リアクション**:
- 出席: {reactions['出席']}
- 課題: {reactions['課題']}'''
    print(message_text)

    channel = bot.get_channel(notify_channel_id)
    message = await channel.send(message_text)

    for reaction in reactions.values():
        await message.add_reaction(reaction)

bot.run(token)
