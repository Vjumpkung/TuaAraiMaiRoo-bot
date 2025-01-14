from discord import FFmpegPCMAudio, Embed
from discord_slash import context
from src.utils.vc import joinVoiceChannel, leaveVoiceChannel, get_PATH_ffmpeg
from src.utils.member import getNick
from src.utils.config import CONFIG, MP3_files
from src.audio.tts import repeat
from src.utils.command import fetchArguments
PATH_ffmpeg = get_PATH_ffmpeg()


async def voice(bot, ctx, msg, language=None, ):

    if not language:
        msg, args = fetchArguments(msg)
        ttsLang = None
        if (args is not None) & (ttsLang is None):
            for arg in args:
                if arg.startswith('l'):
                    language = arg[2:]

    vc = await joinVoiceChannel(bot, ctx)

    if vc is None:
        return

    if (msg in MP3_files) & (not language):
        vc.play(FFmpegPCMAudio(executable=PATH_ffmpeg,
                source=f"{CONFIG.audio.PATH_mp3}{msg}.mp3"))
        returnMessage = f'{getNick(ctx.author)} เล่น **{msg}**.mp3'
    else:
        await repeat(vc, text=msg, lang=language)
        returnMessage = f'{getNick(ctx.author)}: {msg}'

    return await ctx.send(returnMessage)


async def say(bot, ctx, msg, language=None, travel=False):
    #send message for waiting some process completed.
    wc = await ctx.send("processing...")

    try:
        isBotCommand = ctx.message.startswith('$')
    except:
        isBotCommand = False

    if (language is None) & (isBotCommand):
        msg, args = fetchArguments(msg)
        if args is not None:
            for arg in args:
                if arg.startswith('l'):
                    language = arg[2:]

    vc = await joinVoiceChannel(bot, ctx)

    if vc is None:
        return

    await repeat(vc, text=msg, lang=language)

    if travel is True:
        welcome_back = f'{msg}'
        return await wc.edit(content=welcome_back)

    returnMessage = f'{getNick(ctx.author)}: {msg}'
    
    return await wc.edit(content=returnMessage)


async def play(bot, ctx, sound, political=False):

    vc = await joinVoiceChannel(bot, ctx)

    if vc is None:
        return

    vc.play(FFmpegPCMAudio(executable=PATH_ffmpeg,
            source=f"{CONFIG.audio.PATH_mp3}{sound}.mp3"))

    if not political:
        returnMessage = f'{getNick(ctx.author)} เล่น **{sound}**.mp3'
        return await ctx.send(returnMessage)
    else:
        returnMessage = f'||`ข้อความนี้ถูกลบโดยรัฐบาลไทย`||'
        return await ctx.send(returnMessage, delete_after=5)


async def disconnect(bot, ctx):
    await leaveVoiceChannel(bot, ctx)
