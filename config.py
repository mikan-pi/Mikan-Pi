DEV_MODE = True

GUILD_ID = 864093335123001374 if DEV_MODE else 807264600718442516
SYS_CHANNEL_ID = 1349749883506003979 if DEV_MODE else 1327223543548870678
BACKUP_CHANNEL_ID = 1349752769434878033 if DEV_MODE else 1349752853111242794

# vc経験値andデータセーブ1cycleの時間(秒)
VC_EXP_CYCLE_SEC = 600

# role経験値andレベルアップ判定andデータセーブ1cycleの時間(秒)
CYCLE_TIME = 600


EXP_RATE = {
    "role": 1000,    # 持っているロール1つ辺りの経験値
    "chat": 1,      # メッセージ1つ辺りの経験値
    "voice": 25     # vc接続10分毎の経験値
}

EXP_IGNORE_ROLES = [
    1350080113731043368,  # 実験用
    1293572837399072858, # member role
    1293572555474472990, # staff role
]

MAX_LEVEL = 20

LEVEL_ROLES_COLOR = {
    0: "#FFFFFF",
    1: "#49ffa1",
    2: "#7FE7FA",
    3: "#7EB0FA",
    4: "#B78AFA",
    5: "#FA89C2",
    6: "#FF5541",
    7: "#FFA23D",
    8: "#FFE873",
    9: "#BCFF00",
    10: "#A8FFF0",
    11: "#C1D4FF",
    12: "#E59FFF",
    13: "#FFD4FF",
    14: "#FFBADB",
    15: "#FFD4D4",
    16: "#FFE9D4",
    17: "#FFFFD4",
    18: "#E4FFD4",
    19: "#D4FFEA",
    20: "#D4FFFF"
}

# レベルアップに必要な総経験値
LEVEL_EXP = {
    1: 1000,
    2: 2000,
    3: 3000,
    4: 5000,
    5: 10000,
    6: 20000,
    7: 30000,
    8: 50000,
    9: 75000,
    10: 100000,
    11: 125000,
    12: 150000,
    13: 175000,
    14: 200000,
    15: 250000,
    16: 300000,
    17: 350000,
    18: 400000,
    19: 450000,
    20: 500000,
    21: 999999,
}

HYPIXEL_GUILD_CHAT_SEND_CHANNEL_ID = 1350677534194270268 if DEV_MODE else 1273623720778272768
HYPIXEL_GUILD_CHAT_WEBHOOK_CHANNEL_ID = 1350686296535732234 if DEV_MODE else 1350740053273350164


HYPIXEL_FETCH_CYCLE = 60 * 60 * 24