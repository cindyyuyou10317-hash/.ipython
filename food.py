import streamlit as st
import random
import time

# 1. 網頁基本設定
st.set_page_config(page_title="今天吃啥？美食幸運輪盤", page_icon="🍔", layout="centered")
st.title("🍔 今天吃啥？美食幸運輪盤")
st.write("肚子餓了卻不知道吃什麼？讓輪盤幫你決定，並一鍵搜尋在地美食！")

st.divider()

# 2. 預設的美食清單（你可以自由增加或修改喜歡的食物）
FOOD_LIST = [
    "火鍋", "拉麵", "義大利麵", "燒肉", "壽司生魚片", 
    "滷肉飯小吃", "美式漢堡", "韓式料理", "泰式料理", 
    "早午餐", "咖哩飯", "牛排", "居酒屋", "炸雞啤酒","粥","水餃類",'烏龍麵','火鍋','披薩'
]

# 預設的熱門地區選單（包含雙北知名商圈，也可以自己手動輸入）
POPULAR_AREAS = [
    "中山", "信義", "西門町", "公館", "東區", 
    "板橋", "淡水", "中正", "大安", "松山", "其他（自行輸入）"
]

# 3. 介面佈局
st.subheader("📍 第一步：選擇你的目前位置")
area_choice = st.selectbox("請選擇或點選靠近你的區域：", POPULAR_AREAS)

# 如果選擇「其他」，就跳出文字輸入框讓使用者自己打字
if area_choice == "其他（自行輸入）":
    current_area = st.text_input("請輸入你想搜尋的地區或縣市（例如：中壢、台中一中、高雄左營）：", placeholder="例如：桃園中壢")
else:
    current_area = area_choice

st.divider()

st.subheader("🎲 第二步：啟動美食幸運輪盤")

# 使用 Streamlit 的 session_state 來記住轉盤轉到的結果
if "chosen_food" not in st.session_state:
    st.session_state.chosen_food = None

# 當按下「轉盤開始」按鈕
if st.button("✨ 幫我決定今天吃什麼！ ✨", type="primary"):
    # 做出一個好玩的動態倒數效果，模擬輪盤在轉
    with st.spinner("🔮 輪盤瘋狂旋轉中... 🤤"):
        time.sleep(1)  # 讓程式暫停 1 秒，增加期待感
        st.session_state.chosen_food = random.choice(FOOD_LIST)
    
    st.balloons()  # 噴出慶祝氣球！

# 4. 顯示轉盤結果與搜尋按鈕
if st.session_state.chosen_food:
    st.markdown(f"""
        <div style="background-color: #FFF3CD; padding: 20px; border-radius: 10px; text-align: center; border: 2px dashed #FFC107;">
            <h3 style="color: #856404; margin: 0;">🎯 輪盤最終決定：今天就吃 【 <span style="color: #DC3545; font-size: 28px;">{st.session_state.chosen_food}</span> 】 吧！</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("") # 空一行
    
    if not current_area:
        st.warning("⚠️ 提示：請先在第一步輸入或選擇地區，才能幫你精準搜尋喔！")
    else:
        # 核心：自動拼出 Google 的搜尋網址
        search_query = f"{current_area} {st.session_state.chosen_food} 美食 推薦"
        google_url = f"https://www.google.com/search?q={search_query}"
        
        st.write(f"🌐 準備幫你搜尋： `{search_query}`")
        
        # 做出一個超漂亮的網頁按鈕，點擊後會另開視窗直接去 Google
        st.markdown(f'''
            <a href="{google_url}" target="_blank">
                <button style="
                    background-color: #28A745;
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 18px;
                    font-weight: bold;
                    width: 100%;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    🔍 一鍵查看 【{current_area}】 的 {st.session_state.chosen_food} 推薦名單 🍽️
                </button>
            </a>
        ''', unsafe_allow_html=True)