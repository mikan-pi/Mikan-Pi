import discord

from public.embed import Embed
from public.logging.logger import MainLogger

from discord import app_commands

from features.admin_utils.embed.utils import parse_mimd


command_group_announce = discord.app_commands.Group(name="announce",description="メッセージを送信します")

logger = MainLogger()


def register(client: discord.Client, tree: discord.app_commands.CommandTree):
    # スコープを管理者限定に
    @command_group_announce.command(name="embed",description="embedを送信します")
    async def embed(interaction: discord.Interaction, file: discord.Attachment|None = None, txt: str = ""):
        logger.info(f"embed command called by {interaction.user.id}")
        return_embed = Embed.Default(title= f"/embed {file.filename if file is not None else ''} {txt}")
        embed = Embed.Default(title= f"")
        # 実行時に管理者権限チェック
        try:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("このコマンドを使用するには管理者権限が必要です。", ephemeral=True)
                logger.info("Permission denied: not admin")
                return
        except:
            await interaction.response.send_message("このコマンドはdmでは利用できません。", ephemeral=True)
            logger.info("User used DM")
            return
        # ファイルとテキストの両方が存在する場合はエラー
        if file is not None and txt != "":
            return_embed.add_field(name="",value="ファイルとテキストを同時に送ることはできません",inline=False)
            await interaction.response.send_message(embed=return_embed)
            logger.info("file and txt exist")
            return
        # ファイルがある場合はファイルを展開してtxtに代入
        if file is not None:
            try:
                txt = (await file.read()).decode("utf-8")
            except:
                return_embed.add_field(name="",value="ファイルの読み込みに失敗しました",inline=False)
                await interaction.response.send_message(embed=return_embed)
                logger.info("file decode error")
                return
        # テキストで送られてるなら\\nを改行に変換
        if txt:
            txt = txt.replace("\\n","\n")
            return_embed.add_field(name="",value="テキスト中に\\\\nが存在したため、改行に変換しました",inline=False)
        # 内容が空なら
        if txt == "":
            return_embed.add_field(name="",value="内容が空なので送信できません",inline=False)
            await interaction.response.send_message(embed=return_embed)
            logger.info("txt is empty")
            return
        send_data, other_dat = await parse_mimd(txt)
        logger.info("parsed txt")
        # embedに追加
        embed.title = other_dat["title"]
        for items in send_data:
            embed.add_field(name=items["name"],value=items["value"],inline=False)
        return_embed.add_field(name="",value="embedを送信しました",inline=False)
        # embedを送信
        await interaction.response.send_message(embed=return_embed,ephemeral=True)
        # 同じchidにembedを送信
        await interaction.channel.send(embed=embed)
        logger.info('embed sent')


    tree.add_command(command_group_announce)