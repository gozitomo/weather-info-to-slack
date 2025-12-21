import os

from slack_sdk import WebClient


def send_image_to_slack(file_path, comment):
    """
    send_image_to_slack の Docstring
    保存された画像をSlackに投稿する
    :param file_path: 送信ファイルのパス
    :param comment: 投稿に添えるメッセージ
    """
    # トークン取得
    token = os.getenv("SLACK_BOT_TOKEN")
    channel_id = os.getenv("SLACK_CHANNEL_ID")

    client = WebClient(token=token)

    try:
        client.files_upload_v2(
            channel=channel_id, file=file_path, initial_comment=comment
        )

        return True
    except Exception as e:
        print(f"Slack送信エラー：{e}")
        return False
