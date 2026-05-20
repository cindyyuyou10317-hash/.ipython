import streamlit as st
import webbrowser

# 1. 網頁基本設定
st.set_page_config(page_title="小說智慧導航島", page_icon="📚", layout="centered")
st.title("📚 小說聚合導航 App (無 AI 纯淨版)")
st.write("選擇你想看的小說類型與想去的平台，一鍵精準跳轉到搜尋結果頁面！")

st.divider()

# 2. 定義各大知名小說網站的搜尋網址規則
# 這裡以台灣讀者常用的平台（如起點中文網台灣分站、卡提諾、天火等概念）來做網址映射
# 注意：真實網站的 URL 結構各有不同，以下為示範與常用結構
PLATFORMS = {
    "起點中文網 (台灣)": "https://tw.qidian.com/search?kw=",
    "卡提諾論壇 (小說區)": "https://ck101.com/search.php?mod=forum&searchsubmit=yes&srchtxt=",
    "Google 精準搜尋": "https://www.google.com/search?q="
}

GENRES = [
    "科幻未來", 
    "都市言情", 
    "懸疑推理", 
    "古典武俠", 
    "玄幻奇幻", 
    "恐怖網遊",
    "霸道總裁",
    "修仙修真"
]

# 3. 建立前端輸入介面
st.subheader("🔍 篩選你的閱讀偏好")

# 讓使用者選擇平台
selected_platform = st.selectbox("1. 請選擇你想去的小說平台：", list(PLATFORMS.keys()))

# 讓使用者選擇書的類型
selected_genre = st.selectbox("2. 請選擇書的類型：", GENRES)

# 額外功能：允許使用者自己加上額外的關鍵字（例如主角名字或特定流派）
extra_keyword = st.text_input("3. 想要加上額外關鍵字嗎？（可不填，例如：女主、穿越、系統）", placeholder="例如：無敵流、高智商")

st.divider()

# 4. 核心跳轉邏輯
if st.button("🚀 一鍵開啟網站並搜尋", type="primary"):
    
    # 組合最終的搜尋關鍵字
    search_query = selected_genre
    if extra_keyword:
        search_query += f" {extra_keyword}"
        
    # 如果選擇的是 Google，我們可以用更聰明的語法（限定找小說）
    if selected_platform == "Google 精準搜尋":
        final_url = f"{PLATFORMS[selected_platform]}{search_query} 小說 線上看"
    else:
        # 組合出該網站的搜尋網址
        final_url = f"{PLATFORMS[selected_platform]}{search_query}"
        
    st.success(f"🎯 已成功生成搜尋網址！")
    st.info(f"🔗 即將前往：{final_url}")
    
    # 在 Streamlit 網頁上提供一個漂亮的點擊按鈕（因為瀏覽器安全機制，有時不允許程式自動彈窗）
    st.markdown(f'''
        <a href="{final_url}" target="_blank">
            <button style="
                background-color: #FF4B4B;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
                width: 100%;">
                👉 點擊這裡立刻前往閱讀 📖
            </button>
        </a>
    ''', unsafe_allow_html=True)
    