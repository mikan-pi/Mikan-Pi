import discord
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import config

async def create_image(level, exp_obj, usersobj: discord.User | discord.Member):
    if isinstance(usersobj, discord.Interaction):
        user = usersobj.user.id
        user_name = usersobj.user.name
        user_icon_url = usersobj.user.display_avatar.url or usersobj.user.default_avatar.url
    elif isinstance(usersobj, discord.Member) or isinstance(usersobj, discord.User):
        user = usersobj.id
        user_name = usersobj.name
        user_icon_url = usersobj.display_avatar.url or usersobj.default_avatar.url
    else:
        raise TypeError("usersobj must be discord.Interaction or discord.Member or discord.User")

    # UIを取得
    ui_image = Image.open(f"./public/pictures/level/{level}.png")

    # ユーザーアイコンをURLから取得
    response = requests.get(user_icon_url)
    user_picture = Image.open(BytesIO(response.content))
    # サイズを調整
    user_picture = user_picture.resize((80, 80))
    # rgbをrgbaに変換
    if user_picture.mode != "RGBA":
        user_picture = user_picture.convert("RGBA")

    # アイコンをUIに貼付
    ui_image.paste(user_picture, (50, 50), user_picture)
    draw = ImageDraw.Draw(ui_image)
    font_size = 40
    font = ImageFont.truetype("./public/fonts/KFHIMAJI.OTF", font_size)
    draw.text((150, 75), user_name, fill=(60, 60, 60, 255), font=font)

    # 現在レベルを貼付
    # digit_offset = int(font_size // 2)
    level_picture = Image.new("RGBA", (50,50), (0, 0, 0, 0))
    draw = ImageDraw.Draw(level_picture)
    draw.text((25, 25), str(level), fill=(255, 255, 255, 255),font=font, anchor="mm")
    # level_digits = len(str(level)) 
    ui_image.paste(level_picture, (245, 185), level_picture)

    # 経験値を取得
    role, vc, chat = await exp_obj.get_exp(user)

    exp_color = (60, 60, 60, 255)

    # 現在経験値 / 必要経験値を貼付
    exp_picture = Image.new("RGBA", (300,50), (0, 0, 0, 0))
    draw = ImageDraw.Draw(exp_picture)
    exp = role + vc + chat
    need = config.LEVEL_EXP[level + 1]
    # 文字サイズがあふれるので調整
    if level != config.MAX_LEVEL:
        if level < 9:
            draw.text((0, 0), f"{exp}/{need}", fill=exp_color,font=font)
        # 領域があふれるので調整
        elif level < 100:
            minifont = ImageFont.truetype("./public/fonts/KFHIMAJI.OTF", 30)
            draw.text((125, 5), f"{exp}", fill=exp_color,font=minifont,anchor="rt")
            draw.text((130, 0), f"/", fill=exp_color,font=font)
            draw.text((155, 10), f"{need}", fill=exp_color,font=minifont)
        else:
            draw.text((0, 0), f"{exp}", fill=exp_color,font=font)
    else:
        draw.text((0, 0), f"{exp}", fill=exp_color,font=font)
    ui_image.paste(exp_picture, (320, 190), exp_picture)

    # それぞれの経験値を貼付
    picture = Image.new("RGBA", (70,100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(picture)
    font = ImageFont.truetype("./public/fonts/KFHIMAJI.OTF", 15)
    draw.text((0, 0), str(vc).rjust(6), fill=exp_color,font=font)
    draw.text((0, 30), str(chat).rjust(6), fill=exp_color,font=font)
    draw.text((0, 60), str(role).rjust(6), fill=exp_color,font=font)
    ui_image.paste(picture, (100, 175), picture)


    # バイトデータとして保存
    byte_io = BytesIO()
    ui_image.save(byte_io, format='PNG')
    byte_io.seek(0)

    return byte_io