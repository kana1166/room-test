import streamlit as st
import requests
from datetime import datetime

# FastAPIサーバーのURL
BASE_URL = "http://127.0.0.1:8000"


# ユーザー関連の関数
def list_users():
    response = requests.get(f"{BASE_URL}/users/")
    if response.status_code == 200:
        users = response.json()
        for user in users:
            st.write(user)


def create_user():
    with st.form("Create User"):
        username = st.text_input("Username", max_chars=12)
        email = st.text_input("Email")
        role = st.selectbox("Role", ["社員", "役員", "管理者"])
        employee_number = st.text_input("Employee Number")  # 社員番号の入力フィールドを追加
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
                st.success("User created successfully!")
            else:
                st.error(f"Failed to create user: {response.text}")


def update_user():
    with st.form("Update User"):
        user_id = st.text_input("User ID")
        username = st.text_input("Username")
        email = st.text_input("Email")
        role = st.selectbox("Role", ["社員", "役員", "管理者"])
        employee_number = st.text_input("Employee Number")  # 社員番号の入力フィールドを追加
        submitted = st.form_submit_button("Update")
        if submitted:
            response = requests.put(
                f"{BASE_URL}/users/{user_id}",
                json={
                    "username": username,
                    "email": email,
                    "role": role,
                    "employee_number": employee_number,  # 社員番号をJSONに含める
                },
            )
            if response.status_code == 200:
                st.success("User updated successfully!")
            else:
                st.error("Failed to update user")


def delete_user():
    with st.form("Delete User"):
        user_id = st.text_input("User ID")
        submitted = st.form_submit_button("Delete")
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
    with st.form("Create Room"):
        room_name = st.text_input("Room Name")
        capacity = st.number_input("Capacity", min_value=1, format="%d")  # 数字入力
        photo_url = st.text_input("Photo URL")
        executive = st.selectbox("Executive", ["Yes", "No"])  # ドロップダウンメニュー
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
                st.success("Room created successfully!")
            else:
                st.error("Failed to create room")


def update_room():
    with st.form("Update Room"):
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
    with st.form("Delete Room"):
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
        for booking in bookings:
            st.write(booking)


def create_booking():
    current_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    with st.form("Create Booking"):
        room_id = st.number_input("Room ID", min_value=1, format="%d")
        main_user_employee_number = st.text_input("Main User Employee Number")

        # 部屋のキャパシティを取得して表示
        room_capacity = get_room_capacity(room_id)
        st.write(f"Room Capacity: {room_capacity}")

        # 追加メンバーの社員番号とゲスト名の入力
        additional_member_numbers = st.text_area("参加する社員は社員ID入力 (comma separated)")
        guest_names = st.text_area("ゲストは名前入力 (comma separated)")

        start_datetime = st.text_input("Start Datetime", current_datetime)
        end_datetime = st.text_input("End Datetime", current_datetime)

        submitted = st.form_submit_button("Create Booking")
        if submitted:
            try:
                # ユーザー情報の取得
                user_response = requests.get(
                    f"{BASE_URL}/users/employee_number/{main_user_employee_number}"
                )
                if user_response.status_code != 200:
                    st.error("Failed to retrieve user information.")
                    return

                user_info = user_response.json()
                user_id = user_info["user_id"]

                # 入力された追加メンバーとゲスト名をリストに変換
                member_employee_numbers = [
                    num.strip()
                    for num in additional_member_numbers.split(",")
                    if num.strip()
                ]
                guests = [
                    name.strip() for name in guest_names.split(",") if name.strip()
                ]

                # 予約情報の送信
                response = requests.post(
                    f"{BASE_URL}/bookings/",
                    json={
                        "room_id": room_id,
                        "user_id": user_id,
                        "main_user_employee_number": main_user_employee_number,
                        "member_employee_numbers": member_employee_numbers,
                        "guest_names": guests,
                        "start_datetime": start_datetime,
                        "end_datetime": end_datetime,
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
    current_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    with st.form("Update Booking"):
        booking_id = st.text_input("Booking ID")
        main_user_employee_number = st.text_input("Main User Employee Number")

        # ユーザー情報の取得
        user_response = requests.get(
            f"{BASE_URL}/users/employee_number/{main_user_employee_number}"
        )
        if user_response.status_code == 200:
            user_info = user_response.json()
        else:
            st.error("Failed to retrieve user information.")
            return

        room_id = st.number_input("Room ID", min_value=1, format="%d")

        # 部屋のキャパシティを取得して表示
        room_capacity = get_room_capacity(room_id)
        st.write(f"Room Capacity: {room_capacity}")

        additional_member_numbers = st.text_area("参加する社員は社員ID入力 (comma separated)")
        guest_names = st.text_area("ゲストは名前入力 (comma separated)")
        start_datetime = st.text_input("Start Datetime", current_datetime)
        end_datetime = st.text_input("End Datetime", current_datetime)

        submitted = st.form_submit_button("Update")
        if submitted:
            try:
                member_employee_numbers = [
                    num.strip()
                    for num in additional_member_numbers.split(",")
                    if num.strip()
                ]
                guests = [
                    name.strip() for name in guest_names.split(",") if name.strip()
                ]

                response = requests.put(
                    f"{BASE_URL}/bookings/{booking_id}",
                    json={
                        "main_user_employee_number": main_user_employee_number,
                        "member_employee_numbers": member_employee_numbers,
                        "guest_names": guests,
                        "room_id": room_id,
                        "start_datetime": start_datetime,
                        "end_datetime": end_datetime,
                    },
                )
                if response.status_code == 200:
                    st.success("Booking updated successfully!")
                else:
                    st.error("Failed to update booking")

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
                st.error("Failed to delete booking")


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
        email = st.text_input("Email")
        booking_id = st.text_input("Booking ID")  # 文字列として入力を受け付ける

        submitted = st.form_submit_button("Create")
        if submitted:
            guest_user_data = {"name": name, "email": email}
            if booking_id:  # booking_id が入力されている場合のみ追加
                guest_user_data["booking_id"] = int(booking_id)

            response = requests.post(f"{BASE_URL}/guest_users/", json=guest_user_data)
            if response.status_code == 200:
                st.success("Guest User created successfully!")
            else:
                st.error(f"Failed to create guest user: {response.text}")


def update_guest_user():
    with st.form("Update Guest User"):
        guest_user_id = st.text_input("Guest User ID")
        name = st.text_input("Name")
        email = st.text_input("Email")
        booking_id = st.text_input("Reservation ID")
        submitted = st.form_submit_button("Update")
        if submitted:
            response = requests.put(
                f"{BASE_URL}/guest_users/{guest_user_id}",
                json={"name": name, "email": email, "booking_id": booking_id},
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
        for booking in bookings:
            st.write(booking)


def create_executive_booking():
    current_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    st.subheader("Create Executive Booking")
    employee_number = st.text_input("Employee Number")
    check_role_button = st.button("Check Role")

    user_id = None
    if check_role_button:
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
        else:
            st.error("Failed to retrieve user information.")
            return

    if user_id:
        with st.form("Create Executive Booking"):
            room_id = st.number_input("Room ID", min_value=1, format="%d")
            main_user_employee_number = st.text_input("Main User Employee Number")

            # 部屋のキャパシティを取得して表示
            room_capacity = get_room_capacity(room_id)
            st.write(f"Room Capacity: {room_capacity}")

            # 追加メンバーの社員番号とゲスト名の入力
            additional_member_numbers = st.text_area("参加する社員は社員ID入力 (comma separated)")
            guest_names = st.text_area("ゲストは名前入力 (comma separated)")

            start_datetime = st.text_input("Start Datetime", current_datetime)
            end_datetime = st.text_input("End Datetime", current_datetime)

            submitted = st.form_submit_button("Create Booking")
            member_employee_numbers = []
            guests = []
            if submitted:
                # 入力された追加メンバーとゲスト名をリストに変換
                member_employee_numbers = [
                    num.strip()
                    for num in additional_member_numbers.split(",")
                    if num.strip()
                ]
                guests = [
                    name.strip() for name in guest_names.split(",") if name.strip()
                ]

            try:
                response = requests.post(
                    f"{BASE_URL}/bookings/",
                    json={
                        "user_id": user_id,
                        "room_id": room_id,
                        "main_user_employee_number": main_user_employee_number,
                        "member_employee_numbers": member_employee_numbers,
                        "guest_names": guests,
                        "start_datetime": start_datetime,
                        "end_datetime": end_datetime,
                    },
                )
                if response.status_code == 200:
                    st.success("Booking created successfully!")
                else:
                    st.error(f"Failed to create booking: {response.text}")
            except ValueError as e:
                st.error(f"Invalid date format: {e}")


def update_executive_booking():
    with st.form("Update Executive Booking"):
        booking_id = st.text_input("Booking ID")
        new_employee_number = st.text_input("New Employee Number")

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
        else:
            st.error("Failed to retrieve user information.")
            return

        new_room_id = st.number_input("New Room ID", min_value=1, format="%d")
        new_start_datetime = st.text_input("New Start Datetime", "2021-01-01T01:00:00")
        new_end_datetime = st.text_input("New End Datetime", "2021-01-01T02:00:00")

        submitted = st.form_submit_button("Update")
        if submitted:
            # 予約更新処理
            update_data = {
                "user_id": new_user_id,
                "room_id": new_room_id,
                "start_datetime": new_start_datetime,
                "end_datetime": new_end_datetime,
            }
            response = requests.put(
                f"{BASE_URL}/bookings/{booking_id}", json=update_data
            )
            if response.status_code == 200:
                st.success("Booking updated successfully!")
            else:
                st.error(f"Failed to update booking: {response.text}")


def delete_executive_booking():
    with st.form("Delete Executive Booking"):
        booking_id = st.text_input("Booking ID")
        employee_number = st.text_input("Your Employee Number")

        # 社員番号に基づいてユーザー情報を取得
        user_response = requests.get(
            f"{BASE_URL}/users/employee_number/{employee_number}"
        )
        if user_response.status_code == 200:
            user_info = user_response.json()
            if user_info["role"] != "役員":
                st.error("Only executives can delete bookings.")
                return
        else:
            st.error("Failed to retrieve user information.")
            return

        submitted = st.form_submit_button("Delete")
        if submitted:
            response = requests.delete(f"{BASE_URL}/bookings/{booking_id}")
            if response.status_code == 200:
                st.success("Booking deleted successfully!")
            else:
                st.error("Failed to delete booking")


# サイドバーのプルダウンメニュー
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
