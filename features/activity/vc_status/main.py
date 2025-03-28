import discord
from discord.ext import tasks
from config import GUILD_ID
from public.logging.logger import MainLogger
import asyncio


priority_games = ["Minecraft", "SkyBlock", "Essential", "SkyClient", "Lunar Client"]
async def check_priority_games(games):
    # 優先ゲームをチェック
    have_preiority = set()
    will_remove = set()
    for game in games:
        for priority_game in priority_games:
            if game.startswith(priority_game):
                will_remove.add(game)
                have_preiority.add(game)
                break
    games -= will_remove
    return have_preiority, games

logger = MainLogger()

def register(client: discord.Client):
    guild = client.get_guild(GUILD_ID)
    channel_cnt = len(guild.voice_channels)
    channel_per_api_interval = 3
    cycle_time = channel_cnt * 10
    @tasks.loop(seconds=cycle_time)
    async def update_vc_status():
        for vc in guild.voice_channels:  # サーバー内のすべてのVCを取得
            members = vc.members  # そのVCにいるメンバーを取得
            
            games = set()  # ゲーム名を格納するセット
            for member in members:
                for activity in member.activities:
                    if (isinstance(activity, discord.Activity) or isinstance(activity, discord.Game)):
                        games.add(activity.name)

            if games:
                priority, other = await check_priority_games(games)
                game_list = ", ".join(priority) + " | " + ", ".join(other)  # ゲーム名をカンマ区切りで結合
                try:
                    await vc.edit(status=f"{game_list[:200]}")  # VCの名前を変更（50文字制限）
                except discord.Forbidden:
                    logger.error(f"no permission to change vc status: {vc.name}")
                except discord.HTTPException:
                    logger.error(f"failed to change vc status: {vc.name}")
            await asyncio.sleep(channel_per_api_interval)

    update_vc_status.start()