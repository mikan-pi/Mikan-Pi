import discord
from features.data import BotData
import config
from public.logging.logger import MainLogger

async def run(client: discord.client):
    data = BotData(client)
    # ロールを作成
    # 記録されているロールを削除
    for role_id in data.data.get("level_roles", {}).values():
        for guild in client.guilds:
            role = guild.get_role(role_id)
            if role:  # ロールが存在するなら削除
                await role.delete()

    # データを削除
    data.data["level_roles"] = {}
    # 新たに10個準備する
    for i in range(config.MAX_LEVEL + 1):
        for guild in client.guilds:
            role = await guild.create_role(name=f"level{i}", color = discord.Color.from_str(config.LEVEL_ROLES_COLOR[i]))
            # ロールidを追加
            data.data["level_roles"][str(i)] = role.id


    await data.set_data()

async def create_level_i_role(client: discord.Client, i: int):
    data = BotData(client)
    for guild in client.guilds:
        role = await guild.create_role(name=f"level{i}", color = discord.Color.from_str(config.LEVEL_ROLES_COLOR[i]))
        # ロールidを追加
        data.data["level_roles"][str(i)] = role.id
        await data.set_data()
        return role
    
async def create_if_not_exist(client: discord.Client):
    data = BotData(client)
    logger = MainLogger()
    for i in range(config.MAX_LEVEL + 1):
        # サーバーにロールがないなら
        for guild in client.guilds:
            if not data.data["level_roles"].get(str(i)) or not guild.get_role(data.data["level_roles"][str(i)]):
                logger.info(f"level{i} role is not exist. creating...")
                await create_level_i_role(client, i)