import streamlit as st
import random
import requests
import json

page = st.sidebar.selectbox("Choose your page", ["users", "rooms", "bookings"])
if page == "users":
    st.title("ユーザー登録画面 ")
    with st.form(key="user"):
        user_id: int = random.randint(0, 10)
        username: str = st.text_input("ユーザー名", max_chars=12)
        data = {"user_id": user_id, "username": username}
        submit_button = st.form_submit_button(label="リクエスト送信")

    if submit_button:
        st.write("##送信データ")
        st.json(data)
        st.write("##レスポンスデータ")
        url = "http://127.0.0.1:8000/users"
        headers = {"Content-Type": "application/json"}  # JSONデータを送信するためのヘッダー
        res = requests.post(url, data=json.dumps(data), headers=headers)
        if res.status_code == 200:
            st.success("登録完了")
        st.write(res.status_code)
        st.json(res.json())

elif page == "rooms":
    st.title("会議室画面")

    with st.form(key="room"):
        room_id: int = random.randint(0, 10)
        room_name: str = st.text_input("ユーザー名", max_chars=12)
        capacity: int = st.number_input("定員", step=1)
        data = {"room_id": room_id, "room_name": room_name, "capacity": capacity}
        submit_button = st.form_submit_button(label="リクエスト送信")

    if submit_button:
        st.write("##送信データ")
        st.json(data)
        st.write("##レスポンスデータ")
        url = "http://127.0.0.1:8000/rooms"
        headers = {"Content-Type": "application/json"}  # JSONデータを送信するためのヘッダー
        res = requests.post(url, data=json.dumps(data), headers=headers)
