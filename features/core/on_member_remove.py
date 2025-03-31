import discord
from public.logging.logger import MainLogger

def register(client: discord.Client):
    logger = MainLogger()
    @client.event
    async def on_member_remove(member: discord.Member):
        # ログ出力
        logger.info(f"Member Leave - {member.name} - {member.id} -")