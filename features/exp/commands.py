import discord
import features.exp.count
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import config
import features.exp.card
import features.exp.panel
from public.logging.logger import MainLogger



def register(client: discord.Client, tree: discord.app_commands.CommandTree):
    exp_obj = features.exp.count.experience(client)
    logger = MainLogger()
    data = features.exp.count.BotData(client)

    @discord.app_commands.command(name="leaderboard", description="経験値ランキングを確認できます(引数を指定しない場合自身の周辺を表示します)")
    async def send_leaderboard(interaction: discord.Interaction, rank: int | None = None):
        logger.info(f"leaderboard command called by {interaction.user.id}")

        # 表示場所が指定されていなければ自分の周辺を表示
        if rank is None:
            # 自身の順位をセット
            rank = await exp_obj.get_rank(interaction.user.id)
        lower_rank = rank - 5 if rank - 5 >= 0 else 0
        upper_rank = lower_rank + 10
        if len(exp_obj) <= lower_rank:
            await interaction.response.send_message(f"順位は現在{len(exp_obj)}位まで存在します", ephemeral=True)
            return
        byte_io = await features.exp.panel.create_image("Leaderboard", exp_obj = exp_obj, lower_rank = lower_rank, upper_rank = upper_rank)

        # メッセージとして画像を送信
        await interaction.response.send_message(file=discord.File(byte_io, filename="leaderboard.png"))

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

        byte_io = await features.exp.card.create_image(level, exp_obj, member_obj)

        # メッセージとして画像を送信
        await interaction.response.send_message(file=discord.File(byte_io, filename="level.png"))

    
    @discord.app_commands.command(name="add_other_exp", description="経験値を追加します")
    async def append_other_exp(interaction: discord.Interaction, member: discord.Member, exp: int):
        member_id = member.id
        # ユーザが管理者でなければ、return
        logger.info(f"add_other_exp command called by {interaction.user.id}")
        if not interaction.user.id in config.ADMIN_USERS:
            return
        await exp_obj.add_other_exp(member_id, exp)
        logger.info(f"add_other_exp {member.name} {exp}")
        await interaction.response.send_message("経験値を追加しました", ephemeral=True)

    tree.add_command(send_leaderboard)
    tree.add_command(send_level)
    tree.add_command(append_other_exp)