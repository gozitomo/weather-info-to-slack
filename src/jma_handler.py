import os
import time


def capture_jma_table(page, output_path):
    """
    気象庁の2週間予報テーブルを画像として保存する
    :param page: PlaywrightのPageオブジェクト　操作対象のブラウザページ
    :param output_path: 保存先となる画像ファイルのパス
    :return: 成功した場合はTrue、データが不正または欠損している場合はFalse
    """

    # 保存先フォルダの作成
    dir_name = os.path.dirname(output_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)

    try:
        # 気象庁長野2週間予報ページに移動
        page.goto("https://www.data.jma.go.jp/cpd/twoweek/?fuk=48")
        print("4. 画面遷移後読み込みを待っています...")
        page.wait_for_load_state("networkidle")
        time.sleep(1)  # 念のためグラフの描画を待つ

        # id="47610"であるセレクタを探す
        selector = '[id="47610"]'
        # 要素が見つかるまで待機
        element = page.wait_for_selector(selector)

        if element:
            # スクリーンショット
            element.screenshot(path=output_path)
            return True
    except Exception as e:
        print(f"スクリーンショット取得エラー：{e}")
    return False
