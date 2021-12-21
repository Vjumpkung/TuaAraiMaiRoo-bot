import discord
from discord import file
import discord_slash
import json           
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
            f.seek(0)
            json.dump(code_db,f,indent=4)
            f.truncate()
        await channel.set_permissions(ctx.guild.default_role, manage_messages=False)
        await ctx.send(f"ลบ {channel.mention} จาก Code Channels แล้ว")
    else:
        await ctx.send(f"{channel.mention} ไม่ได้เป็น Code Channel อยู่แล้ว")
    
    

        