import discord
from discord.ext import commands
from bot_token import BOT_TOKEN

TARGET_ROLE_PREFIX = "level"  # "level" から始まるロールを削除

intents = discord.Intents.default()
intents.guilds = True
intents.members = True  # ロール情報取得のため

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    for guild in bot.guilds:  # ボットが参加しているすべてのサーバーで処理
        roles_to_delete = [role for role in guild.roles if role.name.startswith(TARGET_ROLE_PREFIX)]

        if not roles_to_delete:
            print(f"サーバー '{guild.name}' に削除対象のロールはありません。")
            continue

        for role in roles_to_delete:
            try:
                await role.delete()
                print(f"サーバー '{guild.name}' のロール '{role.name}' を削除しました。")
            except discord.Forbidden:
                print(f"サーバー '{guild.name}' のロール '{role.name}' を削除できません（権限不足）。")
            except discord.HTTPException as e:
                print(f"サーバー '{guild.name}' のロール '{role.name}' 削除中にエラー: {e}")

bot.run(BOT_TOKEN)