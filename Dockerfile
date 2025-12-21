# 1. AWS Lambda Python 3.12 のベースイメージを使用（osバージョン考慮）
FROM public.ecr.aws/lambda/python:3.12

# 2. Chromiumの実行に必要な依存ライブラリを手動でインストール (Amazon Linux用)
# Amazon 新しいOS（AL2023）用の依存関係
# Amazon Linux 2023 (AL2023) 用の依存関係（修正版）
RUN dnf install -y \
    alsa-lib \
    atk \
    at-spi2-atk \
    cups-libs \
    gtk3 \
    libXcomposite \
    libXcursor \
    libXdamage \
    libXext \
    libXi \
    libXrandr \
    libXtst \
    pango \
    libdrm \
    mesa-libgbm \
    libxshmfence \
    liberation-sans-fonts \
    vulkan-loader \
    nss \
    && dnf clean all

# 3. requirements.txt をコピーしてライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Playwright の Chromium 本体をインストール
# (Lambdaの容量制限を意識して他のブラウザは入れない)
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN playwright install chromium

# 5. ソースコードをコンテナ内にコピー
# (srcディレクトリの中身を Lambda のタスクルートにコピー)
COPY src/ ${LAMBDA_TASK_ROOT}/

# 6. Lambda ハンドラーの実行指示
# (src/main.py 内の lambda_handler 関数を呼び出す設定)
CMD [ "main.lambda_handler" ]