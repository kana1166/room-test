会議室予約システム

概要

このプロジェクトは、会議室の予約管理を行うための Web アプリケーションです。ユーザーは複数の会議室を予約し、管理者は全ての予約を監視し管理することができます。予約システムでは会議室の写真閲覧、予約キャンセル規則、役員専用会議室の予約などの機能を提供します。

技術スタック

Frontend: Next.js
Backend: FastAPI
Data Visualization: Streamlit
Database: MySQL/PostgreSQL

セットアップ手順

リポジトリをクローンします。
bash
Copy code
git clone [リポジトリ URL]
必要な依存関係をインストールします。
Copy code
npm install
pip3 install streamlit
poetry add fastapi
poetry add uvicorn
**`Cmd+Shift+P`インタープリンター確認**
poetry shell
poetry install
sql
Copy code
uvicorn main:app --reload
streamlit run app.py

使用方法
ユーザー
会議室の予約、確認、キャンセル。
会議室の写真を閲覧。
会議のメンバーを登録。
管理者
すべての予約の監視と管理。
役員専用会議室の設定。
システム全体の監視。
