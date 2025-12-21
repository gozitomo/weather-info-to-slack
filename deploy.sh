#!/bin/bash

# 1. 変数の設定
AWS_REGION="ap-northeast-1"
AWS_ACCOUNT="434364279795"
REPOSITORY_NAME="weather-bot-repo"
LAMBDA_NAME="weather-bot"
DOCKERFILE_DIR="Dockerfile"

ECR_URL="${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"

echo "=== Start deploying ${LAMBDA_NAME} ==="

# 2. ECRにログイン
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_URL}

# 3. Dockerイメージのビルド
echo "1. Building Docker image"
docker build --platform linux/amd64 -t ${REPOSITORY_NAME} .

# 4. タグ付け
docker tag ${REPOSITORY_NAME}:latest ${ECR_URL}/${REPOSITORY_NAME}:latest

# 5. ECRへプッシュ
echo "2. Pushing image to ECR"
docker push ${ECR_URL}/${REPOSITORY_NAME}:latest

# 6. Lambdaのコードを更新
echo "3. Updating Lambda"
aws lambda update-function-code --function-name ${LAMBDA_NAME} --image-uri ${ECR_URL}/${REPOSITORY_NAME}:latest

echo "=== Deploying has finished ${LAMBDA_NAME} ==="
