# database.py
from sqlalchemy import create_engine
from models import Base

# Docker Composeで設定したMySQLへの接続情報を設定
username = "user"  # Docker Composeファイルで設定したユーザー名
password = "userpassword"  # Docker Composeファイルで設定したパスワード
host = "localhost"  # ホストマシンを指定
database = "mydatabase"  # Docker Composeファイルで設定したデータベース名

# SQLAlchemyエンジンを作成
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}/{database}", echo=True
)


# Docker Composeで設定したMySQLへの接続情報を設定
# username = "root"  # Docker Composeファイルで設定したユーザー名
# password = "Pass.kana11"  # Docker Composeファイルで設定したパスワード
# host = "database1.c4eexno6zabj.us-east-1.rds.amazonaws.com"  # ホストマシンを指定
# database = "database2"  # Docker Composeファイルで設定したデータベース名

# SQLAlchemyエンジンを作成
# engine = create_engine(
#     f"mysql+pymysql://{username}:{password}@{host}/{database}", echo=True
# )

# テーブルの削除
# Base.metadata.drop_all(engine)

# テーブルの再作成
# Base.metadata.create_all(engine)
