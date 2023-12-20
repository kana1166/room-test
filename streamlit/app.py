import streamlit as st
import requests
from datetime import datetime
import hashlib
import pytz

# FastAPIサーバーのURL
BASE_URL = "http://127.0.0.1:8000"


def generate_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_auth(username, password):
    correct_username = "user"
    correct_password = generate_hash("123")
    if username == correct_username and generate_hash(password) == correct_password:
        return True
    return False


# UTCからローカルタイムゾーンへの変換関数
def convert_utc_to_local(utc_datetime_str, local_tz_str):
    utc_datetime = datetime.strptime(utc_datetime_str, "%Y-%m-%dT%H:%M:%S")
    utc_datetime = utc_datetime.replace(tzinfo=pytz.utc)
    local_tz = pytz.timezone(local_tz_str)
    local_datetime = utc_datetime.astimezone(local_tz)
    return local_datetime.strftime("%Y-%m-%dT%H:%M:%S")


# ローカルタイムゾーンからUTCへの変換関数
def convert_local_to_utc(local_datetime_str, local_tz_str):
    local_tz = pytz.timezone(local_tz_str)
    local_datetime = datetime.strptime(local_datetime_str, "%Y-%m-%dT%H:%M:%S")
    local_datetime = local_tz.localize(local_datetime)
    utc_datetime = local_datetime.astimezone(pytz.utc)
    return utc_datetime.strftime("%Y-%m-%dT%H:%M:%S")


# デバッグ用の日時
local_tz_str = "Asia/Tokyo"
local_datetime_str = "2023-12-20T10:00:00"  # ローカルタイムゾーン（東京）のサンプル日時

# ローカルからUTCへの変換
utc_datetime_str = convert_local_to_utc(local_datetime_str, local_tz_str)
print(f"Local to UTC: {local_datetime_str} -> {utc_datetime_str}")

# UTCからローカルへの変換
converted_local_datetime_str = convert_utc_to_local(utc_datetime_str, local_tz_str)
print(f"UTC to Local: {utc_datetime_str} -> {converted_local_datetime_str}")

# 最初のローカル日時と最終的なローカル日時の比較
if local_datetime_str == converted_local_datetime_str:
    print("変換は正確です。")
else:
    print("変換に問題があります。")


# ユーザー関連の関数
def list_users():
    response = requests.get(f"{BASE_URL}/users/")
    if response.status_code == 200:
        users = response.json()
        for user in users:
            st.write(user)


def create_user():
    with st.form("ユーザー作成"):
        username = st.text_input("名前", max_chars=12)
        email = st.text_input("Email")
        role = st.selectbox("Role", ["社員", "役員", "管理者"])
        employee_number = st.text_input("社員番号入力")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Create")
        if submitted:
            response = requests.post(
                f"{BASE_URL}/users/",
                json={
                    "username": username,
                    "email": email,
                    "role": role,
                    "password": password,
                    "employee_number": employee_number,  # 社員番号をJSONに含める
                },
            )
            if response.status_code == 200:
                st.success("作成完了！")
            else:
                st.error(f"Failed to create user: {response.text}")


def update_user():
    with st.form("ユーザー更新"):
        user_id = st.text_input("ユーザー ID")
        username = st.text_input("名前", max_chars=12)
        email = st.text_input("Email")
        role = st.selectbox("Role", ["社員", "役員", "管理者"])
        employee_number = st.text_input("社員番号入力")
        submitted = st.form_submit_button("Update")
        if submitted:
            response = requests.put(
                f"{BASE_URL}/users/{user_id}",
                json={
                    "username": username,
                    "email": email,
                    "role": role,
                    "employee_number": employee_number,
                },
            )
            if response.status_code == 200:
                st.success("更新完了！")
            else:
                st.error("Failed to update user")


def delete_user():
    with st.form("ユーザー削除"):
        user_id = st.text_input("ユーザー ID")
        submitted = st.form_submit_button("削除")
        if submitted:
            response = requests.delete(f"{BASE_URL}/users/{user_id}")
            if response.status_code == 200:
                st.success("User deleted successfully!")
            else:
                st.error("Failed to delete user")


# 会議室関連の関数
def list_rooms():
    response = requests.get(f"{BASE_URL}/rooms/")
    if response.status_code == 200:
        rooms = response.json()
        for room in rooms:
            st.write(room)


def create_room():
    with st.form("会議室作成"):
        room_name = st.text_input("会議室名")
        capacity = st.number_input("人数", min_value=1, format="%d")  # 数字入力
        photo_url = st.text_input("写真 URL")
        executive = st.selectbox("役員専用ですか？", ["Yes", "No"])  # ドロップダウンメニュー
        submitted = st.form_submit_button("Create")
        if submitted:
            # executiveの値をブーリアンに変換
            executive_bool = executive == "Yes"

            response = requests.post(
                f"{BASE_URL}/rooms/",
                json={
                    "room_name": room_name,
                    "capacity": capacity,
                    "photo_url": photo_url,
                    "executive": executive_bool,
                },
            )
            if response.status_code == 200:
                st.success("会議室作成完了！")
            else:
                st.error("Failed to create room")


def update_room():
    with st.form("会議室更新"):
        room_id = st.text_input("Room ID")
        room_name = st.text_input("Room Name")
        capacity = st.text_input("Capacity")
        photo_url = st.text_input("Photo URL")
        executive = st.text_input("Executive")
        submitted = st.form_submit_button("Update")
        if submitted:
            response = requests.put(
                f"{BASE_URL}/rooms/{room_id}",
                json={
                    "room_name": room_name,
                    "capacity": capacity,
                    "photo_url": photo_url,
                    "executive": executive,
                },
            )
            if response.status_code == 200:
                st.success("Room updated successfully!")
            else:
                st.error("Failed to update room")


def delete_room():
    with st.form("会議室削除"):
        room_id = st.text_input("Room ID")
        submitted = st.form_submit_button("Delete")
        if submitted:
            response = requests.delete(f"{BASE_URL}/rooms/{room_id}")
            if response.status_code == 200:
                st.success("Room deleted successfully!")
            else:
                st.error("Failed to delete room")


# 予約関連の関数
def list_bookings():
    response = requests.get(f"{BASE_URL}/bookings/")
    if response.status_code == 200:
        bookings = response.json()
        local_tz_str = "Asia/Tokyo"  # 例として東京のタイムゾーンを使用
        for booking in bookings:
            # UTCからローカルタイムゾーンへの変換
            booking["start_datetime"] = convert_utc_to_local(
                booking["start_datetime"], local_tz_str
            )
            booking["end_datetime"] = convert_utc_to_local(
                booking["end_datetime"], local_tz_str
            )
            st.write(booking)


def create_booking():
    # 現在の日時を取得し、ローカルタイムゾーンに変換
    current_utc_datetime = datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S")
    local_tz_str = "Asia/Tokyo"
    current_local_datetime = convert_utc_to_local(current_utc_datetime, local_tz_str)

    with st.form("予約作成"):
        room_id = st.number_input("Room ID", min_value=1, format="%d")
        main_user_employee_number = st.text_input("Main User Employee Number")

        room_capacity = get_room_capacity(room_id)
        st.write(f"Room Capacity: {room_capacity}")

        additional_member_numbers = st.text_area("参加する社員は社員ID入力 (comma separated)")
        guest_names = st.text_area("ゲストは名前入力 (comma separated)")

        # Streamlitのstateを使用して日時を取得
        if "start_datetime" not in st.session_state:
            st.session_state["start_datetime"] = current_local_datetime
        if "end_datetime" not in st.session_state:
            st.session_state["end_datetime"] = current_local_datetime

        start_datetime = st.text_input(
            "Start Datetime", st.session_state["start_datetime"]
        )
        end_datetime = st.text_input("End Datetime", st.session_state["end_datetime"])

        print(f"User Input - Start Datetime: {start_datetime}")
        print(f"User Input - End Datetime: {end_datetime}")

        submitted = st.form_submit_button("Create Booking")
        if submitted:
            st.session_state["start_datetime"] = start_datetime
            st.session_state["end_datetime"] = end_datetime
            try:
                user_response = requests.get(
                    f"{BASE_URL}/users/employee_number/{main_user_employee_number}"
                )

                if user_response.status_code != 200:
                    st.error("Failed to retrieve user information.")
                    return

                user_info = user_response.json()
                user_id = user_info["user_id"]

                member_employee_numbers = [
                    num.strip()
                    for num in additional_member_numbers.split(",")
                    if num.strip()
                ]
                guests = [
                    name.strip() for name in guest_names.split(",") if name.strip()
                ]

                # UTCに戻すための変換
                start_datetime_utc = convert_local_to_utc(start_datetime, local_tz_str)
                end_datetime_utc = convert_local_to_utc(end_datetime, local_tz_str)
                print(f"Converted to UTC - Start Datetime: {start_datetime_utc}")
                print(f"Converted to UTC - End Datetime: {end_datetime_utc}")

                booking_data = {
                    "room_id": room_id,
                    "user_id": user_id,
                    "main_user_employee_number": main_user_employee_number,
                    "member_employee_numbers": member_employee_numbers,
                    "guest_names": guests,
                    "start_datetime": start_datetime_utc,
                    "end_datetime": end_datetime_utc,
                }

                print("Sending booking request with the following data:")
                print(booking_data)

                response = requests.post(
                    f"{BASE_URL}/bookings/",
                    json={
                        "room_id": room_id,
                        "user_id": user_id,
                        "main_user_employee_number": main_user_employee_number,
                        "member_employee_numbers": member_employee_numbers,
                        "guest_names": guests,
                        "start_datetime": start_datetime_utc,
                        "end_datetime": end_datetime_utc,
                    },
                )
                if response.status_code == 200:
                    st.success("Booking created successfully!")
                else:
                    st.error(f"Failed to create booking: {response.text}")

            except requests.RequestException as e:
                st.error(f"Network error: {e}")


def get_room_capacity(room_id):
    response = requests.get(f"{BASE_URL}/rooms/{room_id}")
    if response.status_code == 200:
        room = response.json()
        return room.get("capacity", 0)
    return 0


def update_booking():
    # 現在の日時を取得し、ローカルタイムゾーンに変換
    current_utc_datetime = datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S")
    local_tz_str = "Asia/Tokyo"
    current_local_datetime = convert_utc_to_local(current_utc_datetime, local_tz_str)

    with st.form("Update Booking"):
        booking_id = st.text_input("Booking ID")
        main_user_employee_number = st.text_input("Main User Employee Number")
        room_id = st.number_input("Room ID", min_value=1, format="%d")
        additional_member_numbers = st.text_area("参加する社員は社員ID入力 (comma separated)")
        guest_names = st.text_area("ゲストは名前入力 (comma separated)")
        # Streamlitのstateを使用して日時を取得
        if "start_datetime" not in st.session_state:
            st.session_state["start_datetime"] = current_local_datetime
        if "end_datetime" not in st.session_state:
            st.session_state["end_datetime"] = current_local_datetime

        start_datetime = st.text_input(
            "Start Datetime", st.session_state["start_datetime"]
        )
        end_datetime = st.text_input("End Datetime", st.session_state["end_datetime"])

        print(f"User Input - Start Datetime: {start_datetime}")

        submitted = st.form_submit_button("Update")

        if submitted:
            # 更新ボタンが押されたら、すべてのチェックを行う
            # ユーザー情報の取得
            user_response = requests.get(
                f"{BASE_URL}/users/employee_number/{main_user_employee_number}"
            )
            if user_response.status_code != 200:
                st.error("Failed to retrieve user information.")
                return

            user_info = user_response.json()
            user_id = user_info.get("user_id")  # ユーザーIDの取得

            # 部屋のキャパシティを取得して表示
            room_capacity = get_room_capacity(room_id)
            st.write(f"Room Capacity: {room_capacity}")

            member_employee_numbers = [
                num.strip()
                for num in additional_member_numbers.split(",")
                if num.strip()
            ]
            guests = [name.strip() for name in guest_names.split(",") if name.strip()]

            start_datetime_utc = convert_local_to_utc(start_datetime, local_tz_str)
            end_datetime_utc = convert_local_to_utc(end_datetime, local_tz_str)

            # 予約の更新処理
            try:
                response = requests.put(
                    f"{BASE_URL}/bookings/{booking_id}",
                    json={
                        "user_id": user_id,  # ユーザーIDをリクエストに追加
                        "main_user_employee_number": main_user_employee_number,
                        "member_employee_numbers": member_employee_numbers,
                        "guest_names": guests,
                        "room_id": room_id,
                        "start_datetime": start_datetime_utc,
                        "end_datetime": end_datetime_utc,
                    },
                )
                if response.status_code == 200:
                    st.success("Booking updated successfully!")
                else:
                    st.error(f"Failed to update booking: {response.text}")
            except requests.RequestException as e:
                st.error(f"Network error: {e}")


def delete_booking():
    with st.form("Delete Booking"):
        booking_id = st.text_input("Booking ID")
        submitted = st.form_submit_button("Delete")
        if submitted:
            response = requests.delete(f"{BASE_URL}/bookings/{booking_id}")
            if response.status_code == 200:
                st.success("Booking deleted successfully!")
            else:
                # エラーレスポンスの詳細表示
                st.error(
                    f"Failed to delete booking: {response.status_code} {response.text}"
                )


# ゲストユーザー関連の関数
def list_guest_users():
    response = requests.get(f"{BASE_URL}/guest_users/")
    if response.status_code == 200:
        guest_users = response.json()
        for guest_user in guest_users:
            st.write(guest_user)


def create_guest_user():
    with st.form("Create Guest User"):
        name = st.text_input("Name")
        booking_id = st.text_input("Booking ID")  # 文字列として入力を受け付ける

        submitted = st.form_submit_button("Create")
        if submitted:
            guest_user_data = {"name": name}
            if booking_id:  # booking_id が入力されている場合のみ追加
                guest_user_data["booking_id"] = int(booking_id)

            # リクエストデータのデバッグ出力
            st.write("Request Data:", guest_user_data)

            response = requests.post(f"{BASE_URL}/guest_users/", json=guest_user_data)

            # レスポンスのデバッグ出力
            st.write("Response Status Code:", response.status_code)
            st.write("Response Text:", response.text)

            if response.status_code == 200:
                st.success("Guest User created successfully!")
            else:
                st.error(f"Failed to create guest user: {response.text}")


def update_guest_user():
    with st.form("Update Guest User"):
        guest_user_id = st.text_input("Guest User ID")
        name = st.text_input("Name")
        booking_id = st.text_input("booking ID")
        submitted = st.form_submit_button("Update")
        if submitted:
            guest_user_data = {"name": name}
            if booking_id:
                guest_user_data["booking_id"] = int(booking_id)
            response = requests.put(
                f"{BASE_URL}/guest_users/{guest_user_id}",
                json=guest_user_data,
            )
            if response.status_code == 200:
                st.success("Guest User updated successfully!")
            else:
                st.error("Failed to update guest user")


def delete_guest_user():
    with st.form("Delete Guest User"):
        guest_user_id = st.text_input("Guest User ID")
        submitted = st.form_submit_button("Delete")
        if submitted:
            response = requests.delete(f"{BASE_URL}/guest_users/{guest_user_id}")
            if response.status_code == 200:
                st.success("Guest User deleted successfully!")
            else:
                st.error("Failed to delete guest user")


def list_executive_booking():
    # 役員用の予約リスト表示機能
    response = requests.get(f"{BASE_URL}/bookings/")
    if response.status_code == 200:
        bookings = response.json()
        local_tz_str = "Asia/Tokyo"
        for booking in bookings:
            # UTCからローカルタイムゾーンへの変換
            booking["start_datetime"] = convert_utc_to_local(
                booking["start_datetime"], local_tz_str
            )
            booking["end_datetime"] = convert_utc_to_local(
                booking["end_datetime"], local_tz_str
            )
            st.write(booking)


def create_executive_booking():
    # 現在の日時を取得し、ローカルタイムゾーンに変換
    current_utc_datetime = datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S")
    local_tz_str = "Asia/Tokyo"
    current_local_datetime = convert_utc_to_local(current_utc_datetime, local_tz_str)

    st.subheader("Create Executive Booking")
    employee_number = st.text_input("Employee Number")
    room_id = st.number_input("Room ID", min_value=1, format="%d")
    main_user_employee_number = st.text_input("Main User Employee Number")
    additional_member_numbers = st.text_area("参加する社員は社員ID入力 (comma separated)")
    guest_names = st.text_area("ゲストは名前入力 (comma separated)")

    # Streamlitのstateを使用して日時を取得
    if "start_datetime" not in st.session_state:
        st.session_state["start_datetime"] = current_local_datetime
    if "end_datetime" not in st.session_state:
        st.session_state["end_datetime"] = current_local_datetime

    start_datetime = st.text_input("Start Datetime", st.session_state["start_datetime"])
    end_datetime = st.text_input("End Datetime", st.session_state["end_datetime"])

    submit_button = st.button("Check Role and Create Booking")

    if submit_button:
        # UTCに戻すための変換
        start_datetime_utc = convert_local_to_utc(start_datetime, local_tz_str)
        end_datetime_utc = convert_local_to_utc(end_datetime, local_tz_str)

        # 社員番号に基づいてユーザー情報を取得
        user_response = requests.get(
            f"{BASE_URL}/users/employee_number/{employee_number}"
        )
        if user_response.status_code == 200:
            user_info = user_response.json()
            st.write("User info:", user_info)  # ユーザー情報のデバッグ表示
            if user_info["role"] != "役員":
                st.error("Only executives are allowed to make bookings.")
                return
            user_id = user_info["user_id"]  # ユーザーIDを取得
            st.success("Role verified: Executive")

            # 予約処理
            try:
                member_employee_numbers = [
                    num.strip()
                    for num in additional_member_numbers.split(",")
                    if num.strip()
                ]
                guests = [
                    name.strip() for name in guest_names.split(",") if name.strip()
                ]

                response = requests.post(
                    f"{BASE_URL}/bookings/",
                    json={
                        "user_id": user_id,
                        "room_id": room_id,
                        "main_user_employee_number": main_user_employee_number,
                        "member_employee_numbers": member_employee_numbers,
                        "guest_names": guests,
                        "start_datetime": start_datetime_utc,
                        "end_datetime": end_datetime_utc,
                    },
                )
                if response.status_code == 200:
                    st.success("Booking created successfully!")
                else:
                    st.error(f"Failed to create booking: {response.text}")
            except ValueError as e:
                st.error(f"Invalid date format: {e}")
        else:
            st.error("Failed to retrieve user information.")


def update_executive_booking():
    # 現在の日時を取得し、ローカルタイムゾーンに変換
    current_utc_datetime = datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S")
    local_tz_str = "Asia/Tokyo"
    current_local_datetime = convert_utc_to_local(current_utc_datetime, local_tz_str)

    with st.form("Update Executive Booking"):
        booking_id = st.text_input("Booking ID")
        new_employee_number = st.text_input("New Employee Number")
        new_room_id = st.number_input("New Room ID", min_value=1, format="%d")
        # Streamlitのstateを使用してデフォルトの日時を設定
        if "new_start_datetime" not in st.session_state:
            st.session_state["new_start_datetime"] = current_local_datetime
        if "new_end_datetime" not in st.session_state:
            st.session_state["new_end_datetime"] = current_local_datetime

        new_start_datetime = st.text_input(
            "New Start Datetime", st.session_state["new_start_datetime"]
        )
        new_end_datetime = st.text_input(
            "New End Datetime", st.session_state["new_end_datetime"]
        )

        submitted = st.form_submit_button("Check Role and Update Booking")

        if submitted:
            # UTCに戻すための変換
            new_start_datetime_utc = convert_local_to_utc(
                new_start_datetime, local_tz_str
            )
            new_end_datetime_utc = convert_local_to_utc(new_end_datetime, local_tz_str)

            # 新しい社員番号に基づいてユーザー情報を取得
            user_response = requests.get(
                f"{BASE_URL}/users/employee_number/{new_employee_number}"
            )
            if user_response.status_code == 200:
                new_user_info = user_response.json()
                if new_user_info["role"] != "役員":
                    st.error("Only executives can update bookings.")
                    return
                new_user_id = new_user_info["user_id"]

                # 予約更新処理
                update_data = {
                    "user_id": new_user_id,
                    "room_id": new_room_id,
                    "start_datetime": new_start_datetime_utc,
                    "end_datetime": new_end_datetime_utc,
                }
                response = requests.put(
                    f"{BASE_URL}/bookings/{booking_id}", json=update_data
                )
                if response.status_code == 200:
                    st.success("Booking updated successfully!")
                else:
                    st.error(f"Failed to update booking: {response.text}")
            else:
                st.error("Failed to retrieve user information.")


def delete_executive_booking():
    with st.form("Delete Executive Booking"):
        booking_id = st.text_input("Booking ID")
        employee_number = st.text_input("Your Employee Number")
        submitted = st.form_submit_button("Check Role and Delete Booking")

        if submitted:
            # 社員番号に基づいてユーザー情報を取得
            user_response = requests.get(
                f"{BASE_URL}/users/employee_number/{employee_number}"
            )
            if user_response.status_code == 200:
                user_info = user_response.json()
                if user_info["role"] != "役員":
                    st.error("Only executives can delete bookings.")
                    return

                # 予約削除処理
                response = requests.delete(f"{BASE_URL}/bookings/{booking_id}")
                if response.status_code == 200:
                    st.success("Booking deleted successfully!")
                else:
                    st.error("Failed to delete booking")
            else:
                st.error("Failed to retrieve user information.")


if "login" not in st.session_state:
    st.session_state["login"] = False


def login():
    if st.session_state.get("login", False):  # ログイン済みの場合
        st.subheader("Logout")
        st.write("You are currently logged in.")
        if st.button("Logout,2click"):
            st.session_state["login"] = False
            st.info("Logged out successfully!")
    else:  # 未ログインの場合
        st.subheader("Login")
        with st.form("Login Form"):  # フォームを作成
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login,2click")
            if submitted:
                if check_auth(username, password):
                    st.session_state["login"] = True
                    st.success("ログイン成功！")
                else:
                    st.error("Incorrect username or password")


option = None

# フォームの外でログイン状態を確認
if st.session_state["login"]:
    option = st.sidebar.selectbox(
        "選択してください",
        (
            "ユーザーリスト",
            "ユーザー作成",
            "ユーザー更新",
            "ユーザー削除",
            "会議室リスト",
            "会議室作成",
            "会議室更新",
            "会議室削除",
            "予約リスト",
            "予約作成",
            "予約更新",
            "予約削除",
            "ゲストユーザーリスト",
            "ゲストユーザー作成",
            "ゲストユーザー更新",
            "ゲストユーザー削除",
            "役員予約リスト",
            "役員予約作成",
            "役員予約更新",
            "役員予約削除",
        ),
    )


# 選択されたオプションに応じて機能を表示

if option == "ユーザーリスト":
    list_users()
elif option == "ユーザー作成":
    create_user()
elif option == "ユーザー更新":
    update_user()
elif option == "ユーザー削除":
    delete_user()
elif option == "会議室リスト":
    list_rooms()
elif option == "会議室作成":
    create_room()
elif option == "会議室更新":
    update_room()
elif option == "会議室削除":
    delete_room()
elif option == "予約リスト":
    list_bookings()
elif option == "予約作成":
    create_booking()
elif option == "予約更新":
    update_booking()
elif option == "予約削除":
    delete_booking()
elif option == "ゲストユーザーリスト":
    list_guest_users()
elif option == "ゲストユーザー作成":
    create_guest_user()
elif option == "ゲストユーザー更新":
    update_guest_user()
elif option == "ゲストユーザー削除":
    delete_guest_user()
elif option == "役員予約リスト":
    list_executive_booking()
elif option == "役員予約作成":
    create_executive_booking()
elif option == "役員予約更新":
    update_executive_booking()
elif option == "役員予約削除":
    delete_executive_booking()

st.sidebar.markdown("[Next.jsアプリケーションに戻る](http://localhost:3000)")

if __name__ == "__main__":
    login()
