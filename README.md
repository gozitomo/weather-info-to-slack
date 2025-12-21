# weather-info-to-slack
AWS Lambda (Python 3.12) 上で Playwright を動かし、指定したサイトの天気情報をスクリーンショットして Slack に通知するボットです。

## 技術スタック
- Language: Python 3.11/3.12
- Infrastructure: AWS Lambda (Container Image)
- Browser Automation: Playwright (Chromium)
- Package Manager: uv
- OS: Amazon Linux 2023

## 依存関係のインストール (ローカル)
```
uv sync
```

## デプロイ方法
1. `deploy.sh` を実行して ECR へイメージをプッシュします。
1. AWS Lambda コンソールでコンテナイメージを更新します。

## Lambda 設定の注意点
- メモリ: 1769 MB 以上 (CPU 1vCPU 相当を確保するため)
- タイムアウト: 3分
- 環境変数:
-- `SLACK_BOT_TOKEN`: Slack ボットトークン
-- `SLACK_CHANNEL_ID`: 送信先チャンネルID
-- `NOHEN_USERID`: ログイン用ユーザーID
-- `NOHEN_PASSWORD`: ログイン用パスワード

## Docker ビルドのポイント
- ベースイメージに `public.ecr.aws/lambda/python:3.12` を使用 (GLIBC の互換性のため)。
- `dnf` を使用してブラウザの実行に必要なシステムライブラリをインストール。
- Playwright は `--single-process` フラグを付けて起動。
