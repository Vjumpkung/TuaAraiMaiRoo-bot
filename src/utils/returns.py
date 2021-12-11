import discord_slash
import json

async def AddReturnMsg(ctx: discord_slash.SlashContext, message: str, return_message: str):
    # guilddata.return_msg.update({message: return_message})
    # guilddata.data['return_msg'] = guilddata.return_msg
    await ctx.send(f"`{message} -> {return_message}`")
    with open("lazydb/return_msg.json", 'r+', encoding='utf-8') as f:
        json_read = json.load(f)
        str_guild = str(ctx.guild.id)
        if(str_guild not in json_read.keys()):
            json_read[str_guild] = {}
        json_read[str_guild][message] = return_message
        #write to file
        f.seek(0)
        print(json_read)
        json.dump(json_read, f, indent=4)
        f.truncate()


async def RemoveReturnMsg(ctx: discord_slash.SlashContext, message: str):
    with open("lazydb/return_msg.json", 'r+', encoding='utf-8') as f:
        json_read = json.load(f)
        return_message = json_read[str(ctx.guild.id)][message]
        if(str(ctx.guild.id) not in json_read.keys()):
            json_read[str(ctx.guild.id)] = {}
        json_read[str(ctx.guild.id)].pop(message, None)
        #write to file
        f.seek(0)
        print(json_read)
        json.dump(json_read, f, indent=4)
        f.truncate()
    await ctx.send(f"Removed `{message}:{return_message}`")
