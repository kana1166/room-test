# database.py
from sqlalchemy import create_engine

# Docker Composeで設定したMySQLへの接続情報を設定
username = "root"  # Docker Composeファイルで設定したユーザー名
password = "Pass.kana11"  # Docker Composeファイルで設定したパスワード
host = "database1.c4eexno6zabj.us-east-1.rds.amazonaws.com"  # ホストマシンを指定
database = "database1"  # Docker Composeファイルで設定したデータベース名

# SQLAlchemyエンジンを作成
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}/{database}", echo=True
)
