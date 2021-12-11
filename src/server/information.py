from inspect import formatargspec
import discord
from discord_slash import SlashContext
from discord.utils import get
from discord import Embed
from bs4 import BeautifulSoup
import requests
import json

def request_nisit(id: str):
    soup = BeautifulSoup(requests.get(f"http://nisit-ku.ku.ac.th/WebForm_Index_Report.aspx?stdid={id}&h=0").content, "html.parser")
    return soup

def get_nisit_data(id: str):
    k = ['id', 'nam-sur', 'faculty', 'department', 'status', 'campus']
    v = [i[-1].strip() for i in [d.getText().split(":")
                                 for d in request_nisit(id).find('table').find_all('p')[:6]]]
    nisit_data = dict(zip(k, v))
    nisit_data['nam'], nisit_data['sur'] = map(
        str, nisit_data['nam-sur'].replace('นาย', '').replace('นางสาว', '').split())
    return nisit_data

def ku_info(ctx: SlashContext,kuid: str):
    try:
        data = get_nisit_data(kuid)
    except:
        data = {}
        data['department'] = "ไม่พบข้อมูล"
    if data['department'] != "วิศวกรรมคอมพิวเตอร์" or data == None:
        em = Embed(
            title=f"About {kuid}", description="This user not in CPE")
        em.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/KU_SubLogo.png/1200px-KU_SubLogo.png")
        return em
    else:
        user_data = data
        with open("src/server/verified_db/verified.json", "r" ,encoding='utf8') as f:
            verified_data = json.load(f)
        nick = ""
        for i in verified_data:
            if i['kuid'] == kuid:
                try:
                    name = i['name']
                    surname = i['surname']
                    nick = i['nickname']
                    break
                except:
                    break
        em = Embed(title=f"About {name} {surname}", color=0x1f8b4c)
        em.set_thumbnail(url="https://cdn.discordapp.com/icons/847172394316464178/60070dd1b80e09ab6e2e6b7b208bd27f.webp")
        em.add_field(name="ชื่อ นามสกุล",value=f"{name} {surname}", inline=False)
        em.add_field(name="Nickname", value=nick, inline=True)
        em.add_field(name="Gender", value="ชาย" if "นาย" in user_data['nam-sur'] else "หญิง", inline=True)
        em.add_field(name="รหัสนิสิต", value=f"{kuid}", inline=True)
        em.add_field(name="Faculty", value=user_data['faculty'], inline=True)
        em.add_field(name="Department",value=user_data['department'], inline=True)
        return em