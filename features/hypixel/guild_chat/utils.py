import requests
from hypixel_token import HYPIXEL_TOKEN
# メモ化
from functools import lru_cache
from features.data import BotData

import discord
import time

from public.logging.logger import MainLogger


logger = MainLogger()

def parse_msg(msg: str):
    # msgを解析
    msg = msg.split("\n")
    name = msg[0]
    msg = msg[1:]

    return name, msg

@lru_cache
def get_mcid(username: str):
    # ① MinecraftのUUIDを取得
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("id")
    return None


async def mcid_to_discord(client: discord.Client, uuid: str):
    data = BotData(client)
    if "mcuuid_to_discord" not in data.data:
        data.data["mcuuid_to_discord"] = {}
    # 24時間以内に取得済みならそれを返す
    if uuid in data.data["mcuuid_to_discord"] and int(time.time()) - data.data["mcuuid_to_discord"][uuid]["time_stamp"] < 3600 * 24:
        return data.data["mcuuid_to_discord"][uuid]["discord_id"]
    else:
        item = get_hypixel_discord(uuid)
        data.data["mcuuid_to_discord"][uuid] = {"discord_id": item, "time_stamp": int(time.time())}
        await data.set_data()
        return item


def get_hypixel_discord(uuid: str):
    url = f"https://api.hypixel.net/player?key={HYPIXEL_TOKEN}&uuid={uuid}"
    logger.info("get_api(uuid to discord) : " + uuid + " -> " + url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        discord_id = data.get("player", {}).get("socialMedia", {}).get("links", {}).get("DISCORD")
        return discord_id
    return None