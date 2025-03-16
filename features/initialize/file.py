from public.json_util import init_data
import discord
import config
import logging
from features.data import BotData
import os
import features.initialize.make_roles
from public.logging.logger import MainLogger

async def run(client: discord.Client):
    logger = MainLogger()
    is_first = False
    data = BotData(client)
    # ファイルがないなら新しいデータを作る
    if data.data == {}:
        # 現在の人数を取得
        guild = config.GUILD_ID
        guild = client.get_guild(guild)
        member_count = len(guild.members)
        # データが入ってなければ再セット
        await data.set_data({
            "userdata": {}, # ユーザが持つ経験値などの情報
            "join_order": member_count, # 何人目の参加者かの情報
            "level_roles": {} # level毎のロール
        })
        # ファイルがなければ、ロール作成
        await features.initialize.make_roles.run(client)
    logger.info("File Initialize - Ended -")
    