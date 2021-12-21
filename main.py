from bot import TuanAraiMaiRoo
from src.format.code import send_fmc
from src.utils.codechannel import AddCodeChannel,remove_channel
import discord
import discord_slash
from src.server.information import ku_info
from discord_slash import SlashCommand
from discord_slash.model import SlashCommandOptionType
from src.utils.returns import *
from src.utils.kick import random_kick
from src.utils.travel import random_travel
from src.utils.command import SlashChoice
from src.poker.poker import poker_play
from src.pog.pog import pog_play
from src.games import rockpaperscissors
from src.audio.audio import say, play, disconnect
from discord_slash.utils.manage_commands import create_option
from src.utils.env import vars
import pkg_resources

import platform
from datetime import datetime

pkg_resources.require("googletrans>=4.0.0-rc.1")

bot = TuanAraiMaiRoo()
slash = SlashCommand(bot, sync_commands=True)


ADMIN_ID = int(vars.ADMIN)


@bot.event
async def on_ready():
    print(f"{bot.user.name} is running now.")
    print(datetime.now())
    me = await bot.fetch_user(ADMIN_ID)
    await me.send(f"Running {bot.user.name} on\n{platform.uname()}")

@bot.event
async def on_message(msg: discord.Message):
    if msg.author.bot:
        return
    try:
        channel = msg.channel
        with open("lazydb/return_msg.json", "r+") as f:
            json_data = json.load(f)
        with open(file="lazydb/code_db.json",mode="r+",encoding="utf8") as g:
            code_db = json.load(g)
        if msg.content in json_data[str(msg.guild.id)].keys():
            await channel.send(json_data[str(msg.guild.id)][msg.content])
            return
        if str(msg.guild.id) in code_db.keys():
            programming_language = code_db[str(msg.guild.id)]['codechannel_ids'][str(channel.id)]["lang"]
            if msg.content[0] in ['_', '*', '`', ' ']:
                return
            await send_fmc(msg, programming_language)
            await msg.delete()
            return
    except:
        pass


@slash.slash(name="hello", description="Say hi to the bot. Mo used to check if bot is ready.")
async def nine_nine(ctx: discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await ctx.send("HI :flushed:")


@slash.slash(name='invitebot', description='I will send you the authorization link, see you in your server.')
async def send_botinvitelink(ctx: discord_slash.SlashContext):
    await ctx.send('https://tinyurl.com/purplemairoo')


@slash.subcommand(base='game', name="poker", description="Plays Poker.")
async def _poker(ctx: discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await poker_play(bot, ctx)


@slash.subcommand(base='game', name="pokdeng", description="Plays Pok Deng.")
async def _pog(ctx: discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await pog_play(bot, ctx)


@slash.subcommand(base='game', subcommand_group='rockpaperscissors', name='singleplayer',
                  description='Play Rock Paper Scissors with bot.')
async def _rockpaperscissors(ctx: discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await rockpaperscissors.RockPaperScissors.PlaySP(bot, ctx)


@slash.subcommand(base='game', subcommand_group='rockpaperscissors', name='multiplayer',
                  description='Play Rock Paper Scissors with friends.')
async def _rockpaperscissors(ctx: discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await rockpaperscissors.RockPaperScissors.PlayMP(bot, ctx)


@slash.slash(name="say", description="Say some thing(Text to speech)",
             options=[create_option(name='message',
                                    description='The sound to play or the text for TTS',
                                    option_type=SlashCommandOptionType.STRING, required=True),

                      create_option(name='language',
                                    description='The language you want TTS to speak',
                                    option_type=SlashCommandOptionType.STRING, required=False,
                                    choices=SlashChoice.choiceVoiceLang)])
async def audio_say(ctx: discord_slash.SlashContext, message, language=None):
    print(f'{str(ctx.author)} used {ctx.name}')
    await say(bot, ctx, message, language)


@slash.slash(name="play", description="Play a sound",
             options=[create_option(name='sound',
                                    description='Choose a sound to play.',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=SlashChoice.choiceSound)])
async def audio_play(ctx: discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound)


@slash.slash(name="tu", description="ตู่",
             options=[create_option(name='sound',
                                    description='[รายละเอียดถูกลบโดยรัฐบาลไทย]',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=SlashChoice.choiceTuVoice)])
async def audio_play(ctx: discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound, political=True)


@slash.slash(name="pom", description="ป้อม",
             options=[create_option(name='sound',
                                    description='[รายละเอียดถูกลบโดยรัฐบาลไทย]',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=SlashChoice.choicePomVoice)])
async def audio_play(ctx: discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound, political=True)


@slash.subcommand(base='oneonetwo', name="o", description="112",
                  options=[create_option(name='sound',
                                         description='[รายละเอียดถูกลบโดยรัฐบาลไทย]',
                                         option_type=SlashCommandOptionType.STRING, required=True,
                                         choices=SlashChoice.choiceOVoice)])
async def audio_play(ctx: discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound, political=True)


@slash.subcommand(base='oneonetwo', name="nui", description="112",
                  options=[create_option(name='sound',
                                         description='[รายละเอียดถูกลบโดยรัฐบาลไทย]',
                                         option_type=SlashCommandOptionType.STRING, required=True,
                                         choices=SlashChoice.choiceNuiVoice)])
async def audio_play(ctx: discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound, political=True)


@slash.subcommand(base='oneonetwo', name="pui", description="112",
                  options=[create_option(name='sound',
                                         description='[รายละเอียดถูกลบโดยรัฐบาลไทย]',
                                         option_type=SlashCommandOptionType.STRING, required=True,
                                         choices=SlashChoice.choicePuiVoice)])
async def audio_play(ctx: discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound, political=True)


@slash.slash(name='n', description='Play N Sound for user [Warning! This sound can hurt your ears].',
             options=[create_option(name='sound',
                                    description='Select Sound To play',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=SlashChoice.choiceNVoice)])
async def audio_play(ctx: discord_slash.SlashContext, sound: str):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound)


@slash.slash(name='slap', description='Slap.')
async def audio_play(ctx: discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, 'slap')


@slash.slash(name="disconnect", description="Disconnect bot from the Voice Channel")
async def audio_disconnect(ctx: discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await disconnect(bot, ctx)


@slash.slash(name="snap", description="Perfectly balanced, as all things should be"
                        , options=[create_option(name="user",description="50% chance to kick that user or not.",option_type=SlashCommandOptionType.USER,required=True)])
async def snap_kick(ctx: discord_slash.SlashContext, user: discord.Member = None):
    print(f'{str(ctx.author)} used {ctx.name}')
    await random_kick(bot, ctx, user)


@slash.slash(name='travel', description="Travel to all of the Voice Channel.")
async def travel_chanel(ctx: discord_slash.SlashContext, user: discord.Member = None):
    print(f'{str(ctx.author)} used {ctx.name}')
    await random_travel(bot, ctx, user)


@slash.subcommand(base='return', name='add', description='Add return messages. (Teach the bot.)',
                  options=[create_option(name='message', description='-',
                                         option_type=SlashCommandOptionType.STRING, required=True),
                           create_option(name='return_message', description='The message that you want the bot to say in return.',
                                         option_type=SlashCommandOptionType.STRING, required=True)])
async def _returnmsg_add(ctx: discord_slash.SlashContext, message: str, return_message: str):
    await AddReturnMsg(ctx, message, return_message)
    
    
@slash.subcommand(base='return', name='remove', description="Remove return messages. (Delete the bot's memory.)",
                  options=[create_option(name='message', description='The message that you want to delete.',
                                         option_type=SlashCommandOptionType.STRING, required=True)])
async def _returnmsg_add(ctx: discord_slash.SlashContext, message: str):
    await RemoveReturnMsg(ctx, message)


@slash.slash(name='kuinfo', description='Shows KU info of a user.' , options=[create_option(name='kuid', description='รหัสนิสิต',option_type=SlashCommandOptionType.STRING, required=True)])
async def _info(ctx: discord_slash.SlashContext,kuid: str):
    wait = await ctx.send("processing...")
    print(f'{str(ctx.author)} used {ctx.name}')
    await wait.edit(content="",embed=ku_info(ctx,kuid))
    

@slash.slash(name="codechannel_add", description="create automatic code formatting." , 
             options=[
                 create_option(name="lang",description="Your programming language",option_type=SlashCommandOptionType.STRING,required=True)
            ])
async def _createcode(ctx: discord_slash.SlashContext,lang: str):
    await AddCodeChannel(ctx,ctx.channel,language=lang)
    
@slash.slash(name="codechannel_delete", description="remove automatic code formatting.")
async def _deletecode(ctx: discord_slash.SlashContext):
    await remove_channel(ctx)

bot.run(vars.TOKEN)
