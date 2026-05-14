# 1. AWS Lambda Python 3.12 のベースイメージを使用（osバージョン考慮）
FROM python:3.12-slim

# 1. Playwright公式イメージ（依存ライブラリが全て含む）
# FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# 2. 作業ディレクトリ設定
WORKDIR /app


# 3. requirements.txt をコピーしてライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Playwright の Chromium 本体をインストール
# (Lambdaの容量制限を意識して他のブラウザは入れない)
# ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
# RUN playwright install chromium

# 5. ソースコードをコンテナ内にコピー
# (srcディレクトリの中身を Lambda のタスクルートにコピー)
# COPY src/ ${LAMBDA_TASK_ROOT}/
COPY src/ ./

# 6. Lambda ハンドラーの実行指示
# srcの中身をカレントディレクトリにコピーしている場合
# 「-u」を追加すると、ログがリアルタイムに表示されるようになります
CMD [ "python", "-u", "main.py" ]