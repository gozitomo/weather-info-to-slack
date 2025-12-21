import os


def goto_nohen_rain_pred(page):
    """
    login_nohen の Docstring
    nohenページにログインし、降水可能性予測ページに遷移
    :param page: PlaywrightのPageオブジェクト　操作対象のブラウザページ
    """
    try:
        nohen_login_url = os.getenv("NOHEN_LOGIN_URL")
        nohen_pred_url = os.getenv("NOHEN_PRED_URL")
        user_id_str = os.getenv("NOHEN_USERID")
        user_pass_str = os.getenv("NOHEN_PASSWORD")

        print("1. ログインページにアクセス...")
        # 直接アクセスしてもログインしていなければログイン画面が出るはずです
        page.goto(nohen_login_url)

        # 2. ログインフォームの入力
        print("2. ログイン情報を入力中...")

        # [name="userid"] または [name="password"] を探して入力
        page.locator('input[name="userid"]').fill(user_id_str)
        page.locator('input[name="password"]').fill(user_pass_str)

        print("3. ログインボタンをクリックします...")
        # ボタンのタイプが submit のものをクリック、または「ログイン」という文字を探す
        page.locator('button[type="submit"]').click()
        # ページが完全に読み込まれるまで少し待機
        page.wait_for_selector(".main_container")
        print("1. 降水可能性予測ページURLにアクセスします...")
        page.goto(nohen_pred_url)

        # ログイン後のページ読み込みを待機
        print("4. 画面遷移後読み込みを待っています...")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("img.resize_graph", timeout=30000)
        page.wait_for_function(
            "selector => document.querySelector(selector).src.includes('base64')",
            arg="img.resize_graph",
            timeout=10000,
        )

        return True

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return False
