import streamlit as st
import random
import time
import sqlite3
import pandas as pd
import datetime

# --- 1. 資料庫函數定義 ---
def init_db():
    conn = sqlite3.connect('food_diary.db')
    c = conn.cursor()
    
    # 📝 資料表 A：用餐紀錄表 (保留)
    c.execute('''
        CREATE TABLE IF NOT EXISTS dining_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,  
            date TEXT,
            meal_time TEXT,
            food_type TEXT,
            restaurant TEXT,
            price INTEGER,
            location TEXT,
            rating REAL
        )
    ''')
    
    # 🔐 新增資料表 B：會員名單表 (用來動態儲存大家的註冊資料)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 註冊新會員的函數
def register_user(username, password):
    conn = sqlite3.connect('food_diary.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        # 如果帳號重複了，SQLite 會自動報錯
        success = False
    conn.close()
    return success

# 驗證登入的函數
def check_login(username, password):
    conn = sqlite3.connect('food_diary.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# 記帳功能函數
def add_record(user_id, date, meal_time, food_type, restaurant, price, location, rating):
    conn = sqlite3.connect('food_diary.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO dining_records (user_id, date, meal_time, food_type, restaurant, price, location, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, date, meal_time, food_type, restaurant, price, location, rating))
    conn.commit()
    conn.close()

def get_user_records(user_id):
    conn = sqlite3.connect('food_diary.db')
    query = "SELECT * FROM dining_records WHERE user_id = ?"
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df

def get_admin_all_records():
    conn = sqlite3.connect('food_diary.db')
    query = "SELECT * FROM dining_records"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 執行資料庫初始化
init_db()

# --- 2. 網頁基本配置 ---
st.set_page_config(page_title="今天吃啥？美食幸運輪盤", page_icon="🍔", layout="centered")

# --- 3. 會員系統（支援註冊與登入） ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# 情況 A：如果還沒登入，顯示含有「登入 / 註冊」切換的分頁
if st.session_state.user_id is None:
    st.title("🔐 美食幸運輪盤 - 歡迎使用")
    
    # 建立一個切換頁籤，讓使用者自己選要登入還是註冊
    tab1, tab2 = st.tabs(["🔑 會員登入", "📝 新用戶註冊"])
    
    with tab1:
        st.write("請輸入您的個人帳號密碼：")
        login_user = st.text_input("帳號", key="login_user")
        login_pass = st.text_input("密碼", type="password", key="login_pass")
        
        if st.button("立即登入", type="primary"):
            # 🌟 特殊邏輯：免註冊的萬能管理員密道，或者是從資料庫撈資料驗證
            if login_user == "admin" and login_pass == "boss999":
                st.session_state.user_id = "admin"
                st.success("🎖 最高管理員登入成功！")
                time.sleep(0.5)
                st.rerun()
            elif check_login(login_user, login_pass):
                st.session_state.user_id = login_user
                st.success(f"歡迎回來，{login_user}！安全連線已建立...")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ 帳號或密碼錯誤，或者該帳號尚未註冊！")
                
    with tab2:
        st.write("第一次使用？請在下方給自己設定一組專屬帳密：")
        reg_user = st.text_input("請輸入想建立的帳號名稱", key="reg_user")
        reg_pass = st.text_input("請輸入想設定的密碼", type="password", key="reg_pass")
        
        if st.button("提交註冊並建立帳戶"):
            if not reg_user or not reg_pass:
                st.warning("⚠️ 帳號和密碼都不能留空喔！")
            elif reg_user == "admin":
                st.error("❌ 不能註冊名為 'admin' 的帳號，這是系統保留字！")
            else:
                # 呼叫寫入 users 資料表的函數
                if register_user(reg_user, reg_pass):
                    st.success(f"🎉 帳號【{reg_user}】註冊成功！現在請切換到「會員登入」頁籤進行登入。")
                else:
                    st.error("❌ 這個帳號已經被別人註冊過了，換個名字試試看吧！")

# 情況 B：如果已經登入，解鎖完整網站功能
else:
    with st.sidebar:
        st.write(f"👤 目前登入：**{st.session_state.user_id}**")
        if st.session_state.user_id == "admin":
            st.info("🎖 系統管理員權限已開通")
        if st.button("登出帳號"):
            st.session_state.user_id = None
            st.rerun()

    # 主網頁功能 (完全保留之前的輪盤與個人記帳本)
    st.title("🍔 今天吃啥？美食幸運輪盤")
    
    FOOD_LIST = ["火鍋", "拉麵", "義大利麵", "燒肉", "壽司生魚片", "滷肉飯小吃", "美式漢堡", "韓式料理", "泰式料理", "早午餐", "咖哩飯", "牛排", "居酒屋", "炸雞啤酒","粥","水餃類",'烏龍麵','披薩']
    POPULAR_AREAS = ["中山", "信義", "西門町", "公館", "東區", "板橋", "淡水", "中正", "大安", "松山", "其他（自行輸入）"]

    st.divider()
    st.subheader("📍 第一步：選擇你的目前位置")
    area_choice = st.selectbox("請選擇或點選靠近你的區域：", POPULAR_AREAS)
    current_area = st.text_input("請輸入你想搜尋的地區或縣市：", placeholder="例如：桃園中壢") if area_choice == "其他（自行輸入）" else area_choice

    st.divider()
    st.subheader("🎲 第二步：啟動美食幸運輪盤")
    if "chosen_food" not in st.session_state: st.session_state.chosen_food = None

    if st.button("✨ 幫我決定今天吃什麼！ ✨", type="primary"):
        with st.spinner("🔮 輪盤瘋狂旋轉中... 🤤"):
            time.sleep(0.5)  
            st.session_state.chosen_food = random.choice(FOOD_LIST)
        st.balloons()  

    if st.session_state.chosen_food and current_area:
        search_query = f"{current_area} {st.session_state.chosen_food} 美食 推薦"
        google_url = f"https://www.google.com/search?q={search_query}"
        st.markdown(f'<a href="{google_url}" target="_blank"><button style="background-color: #28A745; color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-size: 18px; font-weight: bold; width: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">🔍 一鍵查看 【{current_area}】 的 {st.session_state.chosen_food} 推薦名單 🍽️</button></a>', unsafe_allow_html=True)

    # 📝 第三步：美食記帳本表單
    st.divider() 
    st.subheader("📝 新增用餐紀錄 (美食記帳本)")

    with st.form("add_record_form"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("用餐日期", datetime.date.today())
            meal_time = st.selectbox("用餐時段", ["午餐", "晚餐", "宵夜", "其他"])
            food_type = st.text_input("食物類型")
        with col2:
            restaurant = st.text_input("餐廳名稱")
            price = st.number_input("花費金額 (元)", min_value=0, step=10)
            location = st.text_input("餐廳位置")
            rating = st.slider("評分 (1~5顆星)", 1.0, 5.0, 3.0, 0.5)
            
        submitted = st.form_submit_button("儲存紀錄")
        if submitted:
            add_record(st.session_state.user_id, str(date), meal_time, food_type, restaurant, price, location, rating)
            st.success("✅ 紀錄已成功儲存到你的專屬資料庫！")
            st.rerun()

    # 📊 第四步：個人專屬儀表板
    st.divider()
    st.subheader("📊 我的專屬數據歷史紀錄")
    
    df = get_user_records(st.session_state.user_id)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        col1, col2 = st.columns(2)
        with col1: st.metric(label="💰 專屬累積總花費", value=f"{df['price'].sum()} 元")
        favorite_food = df['food_type'].mode()[0] if not df['food_type'].dropna().empty else "無"
        with col2: st.metric(label="🏆 你的最愛食物", value=favorite_food)
    else:
        st.info("目前還沒有你的專屬紀錄喔！")

    # 👑 上帝視角 - 管理員全站機密後台 (只要是 admin 登入就能看到所有人動態註冊並填寫的內容)
    if st.session_state.user_id == "admin":
        st.write("")
        st.markdown("""
            <div style="background-color: #F8D7DA; padding: 15px; border-radius: 5px; border-left: 5px solid #DC3545;">
                <h4 style="color: #721C24; margin: 0;">🛑 系統管理員機密後台 (Admin Panel)</h4>
            </div>
        """, unsafe_allow_html=True)
        
        admin_df = get_admin_all_records()
        if not admin_df.empty:
            st.write("📋 全站會員原始總數據：")
            st.dataframe(admin_df, use_container_width=True)
        else:
            st.info("資料庫目前空空如也，尚無任何動態註冊的會員提交資料。")