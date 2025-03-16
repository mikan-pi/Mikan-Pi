import discord
import features.exp.count
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import config
from features.exp.card import create_image
from public.logging.logger import MainLogger



def register(client: discord.Client, tree: discord.app_commands.CommandTree):
    exp_obj = features.exp.count.experience(client)
    logger = MainLogger()

    @discord.app_commands.command(name="level", description="現在の経験値量を確認できます(DMではuserを指定しないで下さい)")
    async def send_level(interaction: discord.Interaction, user: discord.Member | discord.User = None):
        logger.info(f"level command called by {interaction.user.id}")

        # botなら
        if user and user.bot:
            await interaction.response.send_message("botにはレベルが存在しません", ephemeral=True)
            return

        # 自分を取得
        member = interaction.user.id if not user else user.id

        # dmで引数付きなら拒否
        if interaction.guild is None and user is not None:
            await interaction.response.send_message("DMではuserを指定しないでください", ephemeral=True)
            return

        # 自身のレベルを取得
        level = await exp_obj.get_level(member)

        logger.info(f"level: {level}")

        # 無効ならエラーを返す
        if level == "Disabled":
            await interaction.response.send_message("準備中だよ！ちょっと待って！", ephemeral=True)
            return
        
        member_obj = interaction.user if not user else user

        byte_io = await create_image(level, exp_obj, member_obj)

        # メッセージとして画像を送信
        await interaction.response.send_message(file=discord.File(byte_io, filename="level.png"))

    tree.add_command(send_level)