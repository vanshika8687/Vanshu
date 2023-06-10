import asyncio
import math
import os
import time
from .. import bot
from telethon import events
from telethon.tl.types import DocumentAttributeAudio
from yt_dlp import YoutubeDL
from yt_dlp.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

# Initialize the bot
# Replace `bot` with your actual bot instance
#bot = ...


@bot.on(events.NewMessage(incoming=True, pattern=r"yt(a|v) (.*)"))
async def download_media(event):
    url = event.pattern_match.group(2)
    media_type = event.pattern_match.group(1).lower()

    vtx = await event.reply("`Preparing to download...`")

    opts = {
        "format": "bestaudio/best" if media_type == "a" else "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": media_type == "a",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "480"}
        ] if media_type == "a" else [
            {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
        ],
        "outtmpl": "%(id)s.mp3" if media_type == "a" else "%(id)s.mp4",
        "quiet": True,
        "logtostderr": False,
    }
    audio = media_type == "a"
    video = not audio

    try:
        await vtx.edit("Fetching data, please wait...")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)

    except (
        DownloadError,
        ContentTooShortError,
        GeoRestrictedError,
        MaxDownloadsReached,
        PostProcessingError,
        UnavailableVideoError,
        XAttrMetadataError,
        ExtractorError,
        Exception,
    ) as e:
        await vtx.edit(f"Error: {str(e)}")
        return

    c_time = time.time()
    media_file = f"{ytdl_data['id']}.mp3" if audio else f"{ytdl_data['id']}.mp4"
    media_title = ytdl_data['title']
    media_uploader = ytdl_data['uploader']

    try:
        await vtx.edit(f"Preparing to upload {media_type}: '{media_title}' by '{media_uploader}'")
        await bot.send_file(
            event.chat_id,
            media_file,
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(ytdl_data['duration']) if audio else 0,
                    title=str(media_title),
                    performer=str(media_uploader),
                )
            ] if audio else None,
            caption=media_title if video else None,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "Uploading...", media_title)
            ),
        )
    except Exception as e:
        await vtx.edit(f"Error uploading {media_type}: {str(e)}")
    finally:
        os.remove(media_file)
        await vtx.delete()


async def progress(current, total, event, start, type_of_ps, file_name=None):
    """Generic progress_callback for uploads and downloads."""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join(["▰" for _ in range(math.floor(percentage / 10))]),
            "".join(["▱" for _ in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            await event.edit(
                "{}\nFile Name: `{}`\n{}".format(type_of_ps, file_name, tmp)
            )
        else:
            await event.edit("{}\n{}".format(type_of_ps, tmp))


def humanbytes(size):
    """Input size in bytes,
    outputs in a human-readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
        + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]import asyncio
import math
import os
import time
from .. import bot
from telethon import events
from telethon.tl.types import DocumentAttributeAudio
from yt_dlp import YoutubeDL
from yt_dlp.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

# Initialize the bot
# Replace `bot` with your actual bot instance
#bot = ...


@bot.on(events.NewMessage(incoming=True, pattern=r"yt(a|v) (.*)"))
async def download_media(event):
    url = event.pattern_match.group(2)
    media_type = event.pattern_match.group(1).lower()

    vtx = await event.reply("`Preparing to download...`")

    opts = {
        "format": "bestaudio/best" if media_type == "a" else "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": media_type == "a",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "480"}
        ] if media_type == "a" else [
            {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
        ],
        "outtmpl": "%(id)s.mp3" if media_type == "a" else "%(id)s.mp4",
        "quiet": True,
        "logtostderr": False,
    }
    audio = media_type == "a"
    video = not audio

    try:
        await vtx.edit("Fetching data, please wait...")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)

    except (
        DownloadError,
        ContentTooShortError,
        GeoRestrictedError,
        MaxDownloadsReached,
        PostProcessingError,
        UnavailableVideoError,
        XAttrMetadataError,
        ExtractorError,
        Exception,
    ) as e:
        await vtx.edit(f"Error: {str(e)}")
        return

    c_time = time.time()
    media_file = f"{ytdl_data['id']}.mp3" if audio else f"{ytdl_data['id']}.mp4"
    media_title = ytdl_data['title']
    media_uploader = ytdl_data['uploader']

    try:
        await vtx.edit(f"Preparing to upload {media_type}: '{media_title}' by '{media_uploader}'")
        await bot.send_file(
            event.chat_id,
            media_file,
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(ytdl_data['duration']) if audio else 0,
                    title=str(media_title),
                    performer=str(media_uploader),
                )
            ] if audio else None,
            caption=media_title if video else None,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "Uploading...", media_title)
            ),
        )
    except Exception as e:
        await vtx.edit(f"Error uploading {media_type}: {str(e)}")
    finally:
        os.remove(media_file)
        await vtx.delete()


async def progress(current, total, event, start, type_of_ps, file_name=None):
    """Generic progress_callback for uploads and downloads."""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join(["▰" for _ in range(math.floor(percentage / 10))]),
            "".join(["▱" for _ in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            await event.edit(
                "{}\nFile Name: `{}`\n{}".format(type_of_ps, file_name, tmp)
            )
        else:
            await event.edit("{}\n{}".format(type_of_ps, tmp))


def humanbytes(size):
    """Input size in bytes,
    outputs in a human-readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
        + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]