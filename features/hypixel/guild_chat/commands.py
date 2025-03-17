"""
コマンド処理
/が入力されたとき
保存しているmodリポジトリの.json内url等を書き換えて、コマンドを打った人に返す
同時にwebhookを作成(そのwebhookのurlを設定)
"""

import discord
import config
import features.data
import io
import zipfile
import os

PATH_TO_MOD_JSON = "./features/hypixel/guild_chat/mod/config.json"
PATH_TO_REPOS = "./features/hypixel/guild_chat/repos.zip"

def register(client: discord.Client, tree: discord.app_commands.CommandTree):
    # @discord.app_commands.command(name="want-hypixel-guild-mod", description="自身のhypixel-guild chatをdiscordに表示するmodを提供します。")
    # async def send_mod(interaction: discord.Interaction):
    #     # Discordに送信
    #     await interaction.user.send(file=discord.File(fp=PATH_TO_REPOS, filename="mod.zip"))
    #     await interaction.response.send_message("modをDMに送りました。", ephemeral=True)

    # tree.add_command(send_mod)
    pass