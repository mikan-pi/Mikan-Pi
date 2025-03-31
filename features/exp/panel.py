import discord
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import config
import features.exp.count
import features.data
import itertools

class default_user:
    def __init__(self):
        self.name = "Invalid User"

leaderboard_image = Image.open(f"./public/pictures/leaderboard/panel.png")
data = features.data.BotData()
async def _leaderboard(exp_obj: features.exp.count.experience, lower_rank: int, upper_rank: int):
    rank_offset = 18
    user_offset = 45
    level_offset = 226
    upper_offset = 71
    str_offset = 8
    height = 110 / 3
    send_image = leaderboard_image.copy()

    # ソート済みデータから該当部分を取得
    sorted_items = (await exp_obj.sort(cache_time=10 * 60)).items()
    sort_data = list(itertools.islice(sorted_items, lower_rank, upper_rank + 1))
    draw = ImageDraw.Draw(send_image)
    font = ImageFont.truetype("./public/fonts/KFHIMAJI.OTF", 15)
    expfont = ImageFont.truetype("./public/fonts/KFHIMAJI.OTF", 10)

    draw.text((rank_offset, 20), f"経験値ランキング {lower_rank + 1}位 ~ {upper_rank}位", (0, 0, 0), font=ImageFont.truetype("./public/fonts/KFHIMAJI.OTF", 20))

    # sort_dataの中身を画像に
    for i in range(len(sort_data)):
        # ユーザー情報を取得
        user: int = int(sort_data[i][0])
        level = await exp_obj.get_level(user)
        exp = sum(await exp_obj.get_exp(user))
        rank = lower_rank + i + 1
        user = discord.utils.get(data.client.get_guild(config.GUILD_ID).members, id=user)
        if user is None: user = default_user()
        user_name = user.name
        # ユーザー情報を画像に
        # rankを貼付
        bbox = draw.textbbox((0, 0), str(rank), font=font)
        text_width = bbox[2] - bbox[0]  # bbox の幅を計算
        text_x = rank_offset - text_width // 2  # 中央揃えに調整
        text_y = int(upper_offset + height * i + str_offset)
        draw.text((text_x, text_y), str(rank), (0, 0, 0), font=font)
        # # ユーザーアイコンをURLから取得
        # response = requests.get(user_icon)
        # user_picture = Image.open(BytesIO(response.content))
        # # サイズを調整
        # user_picture = user_picture.resize((30, 30))
        # # rgbをrgbaに変換
        # if user_picture.mode != "RGBA":
        #     user_picture = user_picture.convert("RGBA")

        # # アイコンをUIに貼付
        # send_image.paste(user_picture, (user_offset, int(upper_offset + height * i)), user_picture)
        # ユーザー名を貼付
        draw.text((user_offset, int(upper_offset + height * i + str_offset)), user_name, (0, 0, 0), font=font)
        # levelを貼付
        bbox = draw.textbbox((0, 0), str(level), font=font)
        text_width = bbox[2] - bbox[0]  # bbox の幅を計算
        text_x = level_offset - text_width // 2  # 中央揃えに調整
        text_y = int(upper_offset + height * i + str_offset)
        draw.text((text_x, text_y), str(level), (0, 0, 0), font=font)

        # expを貼付
        draw.text((level_offset + 15, int(upper_offset + height * i + str_offset + 8)), str(exp) + "/" + str(config.LEVEL_EXP[level + 1]), (0, 0, 0), font=expfont)

    # バイトデータとして保存
    byte_io = BytesIO()
    send_image.save(byte_io, format='PNG')
    byte_io.seek(0)

    return byte_io

async def create_image(type: str, **kwargs):
    """
    type : "Leaderboard"

    other : 
        type == "Leaderboard" then exp_obj: features.exp.count.experience
    """
    if type == "Leaderboard":
        # exp_objが存在しなければ引数エラー
        exp_obj = kwargs.get("exp_obj")
        lower_rank = kwargs.get("lower_rank")
        upper_rank = kwargs.get("upper_rank")
        if not exp_obj:
            raise TypeError("exp_obj must be exist")
        else:
            return await _leaderboard(exp_obj, lower_rank, upper_rank)
    else:
        TypeError("type must be Leaderboard")
