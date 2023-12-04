# Pythonの公式イメージをベースとして使用
FROM python:3.11

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY pyproject.toml poetry.lock* /app/

# Poetryをインストールし、依存関係をインストールする
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction -vvv

# アプリケーションのコードをコピー
COPY . /app

# コンテナがリッスンするポート番号を指定
EXPOSE 8000

# コンテナ起動時にアプリケーションを起動するコマンド
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
