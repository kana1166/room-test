# database.py
from sqlalchemy import create_engine

# Docker Composeで設定したMySQLへの接続情報を設定
username = "user"  # Docker Composeファイルで設定したユーザー名
password = "userpassword"  # Docker Composeファイルで設定したパスワード
host = "localhost"  # ホストマシンを指定
database = "mydatabase"  # Docker Composeファイルで設定したデータベース名

# SQLAlchemyエンジンを作成
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}/{database}", echo=True
)
