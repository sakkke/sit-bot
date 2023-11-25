import os
import discord
from dotenv import load_dotenv

import asyncio
from datetime import datetime, time, timedelta

from subject import Semester, filter_subjects
from timetable import get_timetable
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import io

mpl.rc('font', family='Noto Sans CJK JP')

load_dotenv()

token = os.getenv('TOKEN')

notify_channel_id = int(os.getenv('CHANNEL_NOTIFY'))

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

async def action1020():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎯 次の授業 2限 **10時40分**〜12時10分')

async def action1030():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('✅ 1限 終了 9時00分〜**10時30分**\n🎯 次の授業 2限 **10時40分**〜12時10分')

async def action1040():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎬 2限 開始 **10時40分**〜12時10分')

async def action1210():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('✅ 2限 終了 10時40分〜**12時10分**\n🎯 次の授業 3限 **13時00分**〜14時30分')

async def action1240():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎯 次の授業 3限 **13時00分**〜14時30分')

async def action1300():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎬 3限 開始 **13時00分**〜14時30分')

async def action1420():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎯 次の授業 4限 **14時40分**〜16時10分')

async def action1430():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('✅ 3限 終了 13時00分〜**14時30分**\n🎯 次の授業 4限 **14時40分**〜16時10分')

async def action1440():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎬 4限 開始 **14時40分**〜16時10分')

async def action1600():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎯 次の授業 5限 **16時20分**〜17時50分')

async def action1610():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('✅ 4限 終了 14時40分〜**16時10分**\n🎯 次の授業 5限 **16時20分**〜17時50分')

async def action1620():
    channel = bot.get_channel(notify_channel_id)
    await channel.send('🎬 5限 開始 **16時20分**〜17時50分')

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

    ax.table(cellText=df.values, colLabels=df.columns, bbox=[0, 0, 1, 1])

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

bot.run(token)
