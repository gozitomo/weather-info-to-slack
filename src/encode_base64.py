import base64
import os


def save_base64_image(page, selector, output_path):
    """
    save_base64_image の Docstring
    指定したセレクタのimgタグのsrcからBase64データを取得、画像として保存する
    :param page: PlaywrightのPageオブジェクト　操作対象のブラウザページ
    :param selector: 抽出対象となるimg要素を指定するためのCSSセレクタ
    :param output_path: 保存先となる画像ファイルのパス
    :return: 成功した場合はTrue、データが不正または欠損している場合はFalse
    """
    # 保存先ディレクトリがなければ作成する
    dir_name = os.path.dirname(output_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(f"ディレクトリを作成しました：{dir_name}")

    print(f"画像を抽出中{output_path}")

    # imgタグのsrc属性を取得
    src_data = page.get_attribute(selector, "src")

    if src_data and "base64," in src_data:
        # "data:image/png;base64, iVBOR..."のカンマ以降を取得
        base64_str = src_data.split("base64,")[1]

        # でコードしてバイナリデータに変換
        image_data = base64.b64decode(base64_str)

        # ファイルとして書き出し
        with open(output_path, "wb") as f:
            f.write(image_data)
        return True
    return False
