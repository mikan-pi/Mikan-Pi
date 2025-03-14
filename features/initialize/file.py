from public.json_util import init_data
import discord
import config
import logging
from features.data import BotData
import os
import features.initialize.make_roles

async def run(client: discord.Client):
    is_first = False
    # ファイルがないなら新しいデータを作る
    if not os.path.exists('./data.json'):
        # 現在の人数を取得
        guild = config.GUILD_ID
        guild = client.get_guild(guild)
        member_count = len(guild.members)
        init_data({
            "userdata": {}, # ユーザが持つ経験値などの情報
            "join_order": member_count, # 何人目の参加者かの情報
            "level_roles": {} # level毎のロール
        })
        is_first = True
    # データインスタンスの作成
    data = BotData(client)
    data.load()
    if is_first:
        # ファイルがなければ、ロール作成
        await features.initialize.make_roles.run(client)