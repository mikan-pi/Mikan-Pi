from collections import deque

async def parse_mimd(text: str):
    first_title_flag = False
    send_data = deque([{"name":"","value":""}])
    origin_data = {"title": ""}
    for line in text.split("\n"):
        parse_line = line
        while parse_line.startswith(" "):
            parse_line = parse_line[1:]
        # #から始まる一文ならnameに
        if parse_line[0] == "#":
            send_data.append({"name":"","value":""})
            send_data[-1]["name"] = parse_line[1:]
        # タイトルの設定(先頭のみ有効)
        elif parse_line.startswith("|title|") and not first_title_flag:
            origin_data["title"] = parse_line[7:]
            first_title_flag = True
        # 何でもないテキストならデータをセット
        else:
            send_data[-1]["value"] += line
    return send_data, origin_data
