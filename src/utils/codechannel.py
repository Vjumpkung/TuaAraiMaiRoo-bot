import discord
from discord import file
import discord_slash
import json

from discord_slash.context import SlashContext
def getNick(member):
    return member.nick if member.nick is not None else member.name

def formatCode_emb(msg: discord.Message, language: str, sourcecode: str):
    if len(sourcecode) >= 1021:
        SCsplit = sourcecode.split('\n')
        SCsplitratio = -(-len(sourcecode)//1024)+1
        SCsplitind = len(SCsplit)//SCsplitratio
        SClist = []
        for i in range(1, SCsplitratio+1):
            SClist.append(SCsplit[SCsplitind*(i-1):SCsplitind*(i)])
        return SClist

    else:
        pfp = msg.author.avatar_url
        embed = discord.Embed()
        embed.set_thumbnail(url=pfp)
        embed.add_field(
            name='Code', value=f"""By {getNick(msg.author)}```{language}\n{sourcecode}\n```""")
        return embed


def formatCode(msg: discord.Message, language: str, sourcecode: str):
    if len(sourcecode) >= 2000:
        SCsplit = sourcecode.split('\n')
        SCsplitratio = -(-len(sourcecode)//2000)
        SCsplitind = len(SCsplit)//SCsplitratio
        SClist = []
        for i in range(1, SCsplitratio+1):
            SClist.append(SCsplit[SCsplitind*(i-1):SCsplitind*(i)])
        return SClist

    else:
        return f"""By {getNick(msg.author)}```{language}\n{sourcecode}\n```"""


async def send_fmc(msg: discord.Message, language: str):
    if msg.content[:2] in '-e':
        fmc = formatCode_emb(msg, language, msg.content[2:])
        if type(fmc) == list:
            SCfst = '\n'.join(fmc[0])
            pfp = msg.author.avatar_url
            embed = discord.Embed()
            embed.set_thumbnail(url=pfp)
            embed.add_field(
                name='Code', value=f"""By {getNick(msg.author)}```{language}\n{SCfst}\n```""")
            for count, code in enumerate(fmc[1:], start=1):
                SCrest = '\n'.join(code)
                embed.add_field(
                    name=f'#continue {count}', value=f"""```{language}\n{SCrest}\n```""", inline=False)
            await msg.channel.send(embed=embed)
        else:
            await msg.channel.send(embed=fmc)
    else:
        fmc = formatCode(msg, language, msg.content)
        if type(fmc) == list:
            SCfst = '\n'.join(fmc[0])
            await msg.channel.send(f"""By {getNick(msg.author)}```{language}\n{SCfst}\n```""")
            for code in fmc[1:]:
                SCline = '\n'.join(code)
                await msg.channel.send(f"""```{language}\n{SCline}\n```""")
        else:
            await msg.channel.send(formatCode(msg, language, msg.content))
            
async def AddCodeChannel(ctx: discord_slash.SlashContext, channel: discord.TextChannel, language: str):
    try:
        with open(file="lazydb/code_db.json",mode="r+",encoding="utf8") as f:
            code_db = json.load(f)
    except:
        code_db = {}
    print("str(ctx.guild_id)",code_db)
    if str(ctx.guild_id) not in code_db:
        code_db[str(ctx.guild_id)] = {}
        code_db[str(ctx.guild_id)]["codechannel_ids"] = {}
        print(f'Added {ctx.guild.name} to guild table')

    guilddata = code_db[str(ctx.guild_id)]
    
    CHANNEL_ID = channel.id
    # print(guilddata["codechannel_ids"])
    if str(CHANNEL_ID) in guilddata["codechannel_ids"]:
        codeChannel = guilddata["codechannel_ids"][str(CHANNEL_ID)]
        if codeChannel['lang'] == language:
            await ctx.send(f"{channel.mention} เป็น Code Channel ภาษา {language} อยู่แล้ว")
        else:
            try:
                botmsg = await channel.fetch_message(codeChannel['botmsgID'])
                await botmsg.delete()
            except:
                print("Bot couldn't find the Bot's pinned message")

            em = discord.Embed(title=f'{channel.name}')
            em.add_field(name="Programming Language:", value=f"{language}")
            botmsg = await channel.send(embed=em)
            await botmsg.pin()

            guilddata["codechannel_ids"][str(CHANNEL_ID)]['lang'], guilddata["codechannel_ids"][str(CHANNEL_ID)]['botmsgID'] = language, str(botmsg.id)

            await ctx.send(f"แก้ไขให้ {channel.mention} เป็น Code Channel ภาษา {language} แล้ว")

    else:
        em = discord.Embed(title=f'{channel.name}')
        em.add_field(name="Programming Language:", value=f"{language}")
        botmsg = await channel.send(embed=em)
        await botmsg.pin()
        guilddata["codechannel_ids"][str(CHANNEL_ID)] = {}
        guilddata["codechannel_ids"][str(CHANNEL_ID)]["lang"] = language
        guilddata["codechannel_ids"][str(CHANNEL_ID)]['channelID'] = str(channel.id)
        guilddata["codechannel_ids"][str(CHANNEL_ID)]['botmsgID'] = str(botmsg.id)
        await channel.set_permissions(ctx.guild.default_role, manage_messages=True)
        await ctx.send(f"เพิ่ม {channel.mention} เป็น Code Channel ภาษา {language} แล้ว")
    
    code_db[str(ctx.guild_id)].update(guilddata)
    
    # print(code_db)
    
    with open(file="lazydb/code_db.json",mode="r+",encoding="utf8") as f:
        f.seek(0)
        json.dump(code_db,f,indent=4)
        f.truncate()

async def remove_channel(ctx: discord_slash.SlashContext):
    channel = ctx.channel
    CHANNEL_ID = channel.id
    try:
        with open(file="lazydb/code_db.json",mode="r+",encoding="utf8") as f:
            code_db = json.load(f)
    except:
        code_db = {}
    guilddata = code_db[str(ctx.guild_id)]
    if str(CHANNEL_ID) in guilddata["codechannel_ids"]:
        codeChannel = guilddata["codechannel_ids"][str(CHANNEL_ID)]
        print(f'Removed {ctx.guild.name} to guild table')
        botmsg = await channel.fetch_message(codeChannel['botmsgID'])
        await botmsg.unpin()
        await botmsg.delete()
        del code_db[str(ctx.guild_id)]["codechannel_ids"][str(CHANNEL_ID)]
        print(code_db)
        with open(file="lazydb/code_db.json",mode="r+",encoding="utf8") as f:
            f.seek(0)#
            json.dump(code_db,f,indent=4)
            f.truncate()
        await channel.set_permissions(ctx.guild.default_role, manage_messages=False)
        await ctx.send(f"ลบ {channel.mention} จาก Code Channels แล้ว")
    else:
        await ctx.send(f"{channel.mention} ไม่ได้เป็น Code Channel อยู่แล้ว")
    
    

        