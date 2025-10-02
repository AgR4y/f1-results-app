# Pythonの軽量イメージをベースにする
FROM python:3.13-slim

# コンテナ内の作業ディレクトリ
WORKDIR /app

# requirements.txt を先にコピーしてライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリのコードをコピー
COPY . .

# コンテナ起動時に実行するコマンド
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
