import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from encode_base64 import save_base64_image
from jma_handler import capture_jma_table
from nohen_handler import goto_nohen_rain_pred
from slack_post import send_image_to_slack


def lambda_handler(event, context):
    """
    lambda_handler の Docstring
    AWSLambdaからのエントリーポイント
    :param event: 説明
    :param context: 説明
    """
    # Lambdaで書き込み可能なのは/tmpのみ
    output_dir = "/tmp/data"

    # 実行
    result = run_weather_bot(output_dir)

    return {"statusCode": 200, "body": result}


def run_weather_bot(output_dir):
    """
    main の Docstring
    - nohenログイン
    - 降水可能性予測ページに遷移
    - 降水可能性予測画像をdownload
    - Slack投稿
    """
    # 画像保存先ディレクトリの作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 画像保存先の指定
    nohen_output_path = os.path.join(output_dir, "nohen_rain_pred_image.png")
    jma_output_path = os.path.join(output_dir, "jma_screenshot.png")

    # 環境変数をロード
    load_dotenv()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--single-process",
                ],
            )
            # ビューポートを大きめに設定
            context = browser.new_context(viewport={"width": 1280, "height": 1600})
            page = context.new_page()

            # nohenページから降水可能性予測画像を取得
            if goto_nohen_rain_pred(page):
                # nohenの画像を取得
                success_nohen = save_base64_image(
                    page, "img.resize_graph", nohen_output_path
                )
                if success_nohen:
                    print("nohen画像の取得に成功")
                else:
                    print("nohen画像の取得に失敗")

            # 気象庁予報ページのスクリーンショットを取得
            success_jma = capture_jma_table(page, jma_output_path)
            if success_jma:
                print("気象庁スクショの取得に成功")
            else:
                print("気象庁スクショの取得に失敗")

            # ブラウザを閉じる
            browser.close()

            # Slackに画像を投稿
            # 送信ファイルリスト
            upload_files = []

            if success_nohen:
                upload_files.append(
                    {"path": nohen_output_path, "title": "【ノーエン】降水可能性予測"}
                )
            if success_jma:
                upload_files.append(
                    {"path": jma_output_path, "title": "【気象庁】2週間気温予報"}
                )

            # Slackに画像を投稿
            for file in upload_files:
                success_post = send_image_to_slack(file["path"], file["title"])
                if success_post:
                    print(f"Slackへの投稿完了{file['title']}")
                else:
                    print(f"Slack投稿失敗{file['title']}")

    except Exception as e:
        error_msg = f"エラーが発生しました: {e}"
        print(error_msg)
        return error_msg


if __name__ == "__main__":
    """
    ローカルでの手動テスト用
    """
    local_output_dir = os.path.join(os.path.dirname(__file__), "../data")
    print("ローカルモードで実行...")
    run_weather_bot(local_output_dir)
