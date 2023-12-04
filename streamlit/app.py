import streamlit as st
import requests
import hashlib


def generate_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_auth(username, password):
    correct_username = "user"
    correct_password = generate_hash("123")
    if username == correct_username and generate_hash(password) == correct_password:
        return True
    else:
        return False


def login_user():
    username = st.sidebar.text_input("ユーザー名", key="username")
    password = st.sidebar.text_input("パスワード", type="password", key="password")

    # 'key' パラメーターに一意の値を設定します。
    if st.sidebar.button("ログイン", key="login_button"):
        if check_auth(username, password):
            st.session_state["logged_in"] = True
        else:
            st.session_state["logged_in"] = False
            st.sidebar.error("認証に失敗しました")


# Define the base URL for your FastAPI app
BASE_URL = "http://localhost:8000"


def create_article():
    st.subheader("新規作成")
    title = st.text_input("Title")
    content = st.text_area("Content")
    if st.button("作成"):
        response = requests.post(
            f"{BASE_URL}/articles/", json={"title": title, "content": content}
        )
        if response.status_code == 200:
            st.success("Article Created Successfully")
        else:
            st.error("Error in Article Creation")


def view_articles():
    st.subheader("一覧")
    response = requests.get(f"{BASE_URL}/articles/")
    if response.status_code == 200:
        articles = response.json()
        for article in articles:
            st.write(
                f"ID: {article['id']}, Title: {article['title']},content: {article['content']}"
            )


def update_article():
    st.subheader("更新")
    article_id = st.text_input("Article ID")
    title = st.text_input("New Title")
    content = st.text_area("New Content")
    if st.button("Update Article"):
        response = requests.put(
            f"{BASE_URL}/articles/{article_id}",
            json={"title": title, "content": content},
        )
        if response.status_code == 200:
            st.success("Article Updated Successfully")
        else:
            st.error("Error in Article Update")


def delete_article():
    st.subheader("削除")
    article_id = st.text_input("Article ID")
    if st.button("Delete Article"):
        response = requests.delete(f"{BASE_URL}/articles/{article_id}")
        if response.status_code == 200:
            st.success("Article Deleted Successfully")
        else:
            st.error("Error in Article Deletion")


def main():
    st.sidebar.title("ブログ管理画面ログイン")

    # セッション状態の初期化
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_user()
    if st.session_state["logged_in"]:
        # ログイン済みの場合はブログ管理メニューを表示
        st.sidebar.success("ログイン済みです")

        # ログインに成功したら、ブログ管理メニューを表示
        menu = ["作成", "一覧", "更新", "削除"]
        choice = st.selectbox("メニュー", menu, key="main_menu")

        if choice == "作成":
            create_article()
        elif choice == "一覧":
            view_articles()
        elif choice == "更新":
            update_article()
        elif choice == "削除":
            delete_article()


if __name__ == "__main__":
    main()
