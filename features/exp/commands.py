import discord
import features.exp.count
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import config
from features.exp.card import create_image



def register(client: discord.Client, tree: discord.app_commands.CommandTree):
    exp_obj = features.exp.count.experience(client)

    @discord.app_commands.command(name="level", description="自分のレベルを確認")
    async def send_level(interaction: discord.Interaction):
        # 自分を取得
        member = interaction.user.id

        # 自身のレベルを取得
        level = await exp_obj.get_level(member)

        # 無効ならエラーを返す
        if level == "Disabled":
            await interaction.response.send_message("準備中だよ！ちょっと待って！", ephemeral=True)
            return

        byte_io = await create_image(level, exp_obj, interaction)

        # メッセージとして画像を送信
        await interaction.response.send_message(file=discord.File(byte_io, filename="level.png"))

    tree.add_command(send_level)