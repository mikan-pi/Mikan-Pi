import features.exp.commands
import features.exp.count
import features.hypixel.guild_chat.commands
import features.join_member
import features.core.on_member_remove
from features.core.make_intent import make_intent
from features.core.run import run
from bot_token import BOT_TOKEN
import features.core.on_ready
import features.core.make_tree
import features.core.on_message
import features.hypixel.guild_chat.commands
import features.data
import features.admin_utils.embed.main

if __name__ == "__main__":
    client = make_intent()
    # clientの登録 & データの登録
    features.data.BotData().set_client(client)
    # treeの作成
    tree = features.core.make_tree.run(client)
    # bot起動時実行関数の登録
    features.core.on_ready.register(client, tree)
    # メッセージ受信時実行
    features.core.on_message.register(client, tree)

    # コマンドの登録
    features.exp.commands.register(client, tree)
    features.hypixel.guild_chat.commands.register(client, tree)
    features.admin_utils.embed.main.register(client, tree)


    # メンバー参加時アクションの登録
    features.join_member.setup(client)
    # メンバー退室時アクションの登録
    features.core.on_member_remove.register(client)
    run(client, BOT_TOKEN)