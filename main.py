import features.exp.commands
import features.exp.count
import features.join_member
from features.core.make_intent import make_intent
from features.core.run import run
from bot_token import BOT_TOKEN
import features.core.on_ready
import features.core.make_tree
import features.core.on_message

if __name__ == "__main__":
    client = make_intent()
    # treeの作成
    tree = features.core.make_tree.run(client)
    # bot起動時実行関数の登録
    features.core.on_ready.register(client, tree)
    # メッセージ受信時実行
    features.core.on_message.register(client, tree)

    # コマンドの登録
    features.exp.commands.register(client, tree)

    # メンバー参加時アクションの登録
    features.join_member.setup(client)
    run(client, BOT_TOKEN)