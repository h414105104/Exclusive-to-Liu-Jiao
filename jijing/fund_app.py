import streamlit as st
import requests
import re
import json
import time
import random

# --- 1. 页面基础配置 ---
st.set_page_config(
    page_title="刘姣的像素金库",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="auto" # 手机端自动收起侧边栏
)

# --- 2. 注入“少女+像素”风格的 CSS (包含手机端适配) ---
pixel_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap');

    /* --- 全局背景：浅粉色 --- */
    .stApp {
        background-color: #FFF0F5;
        background-image: radial-gradient(#FFB6C1 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* --- 字体设置 --- */
    html, body, [class*="css"] {
        font-family: 'ZCOOL KuaiLe', 'VT323', monospace;
    }

    /* --- 标题样式 --- */
    h1 {
        color: #FF1493;
        text-shadow: 2px 2px 0px #FFB6C1;
        font-size: 3.5rem !important;
        text-align: center;
        margin-bottom: 0px;
    }

    /* --- 侧边栏样式 --- */
    [data-testid="stSidebar"] {
        background-color: #FFE4E1;
        border-right: 4px dashed #FF69B4;
    }

    /* --- 按钮样式 --- */
    div.stButton > button {
        background-color: #FF69B4;
        color: white;
        border: 4px solid #C71585;
        border-radius: 0px;
        box-shadow: 4px 4px 0px #C71585;
        font-family: 'VT323', monospace;
        font-size: 20px;
        width: 100%; /* 手机端按钮占满宽度更好按 */
    }
    div.stButton > button:active {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #C71585;
    }

    /* --- 卡片容器样式 --- */
    .pixel-card {
        background-color: #FFFFFF;
        border: 4px solid #000;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 5px 5px 0px #FF1493;
        position: relative;
        transition: transform 0.2s;
    }
    
    /* 简单的交互效果：鼠标悬停或手指点击时微微浮动 */
    .pixel-card:active {
        transform: scale(0.98);
    }

    .up-text { color: #FF0000; font-weight: bold; }
    .down-text { color: #32CD32; font-weight: bold; }

    /* =========================================
       📱 手机端专属适配 (Media Query)
       当屏幕宽度小于 600px 时生效
    ========================================= */
    @media only screen and (max-width: 600px) {
        /* 1. 缩小标题字体，防止手机换行 */
        h1 {
            font-size: 2.2rem !important;
            margin-top: -20px; /* 减少顶部留白 */
        }
        
        /* 2. 调整页面主体边距，利用更多屏幕空间 */
        .block-container {
            padding-top: 2rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        /* 3. 卡片字体微调 */
        .pixel-card-name {
            font-size: 1.1rem !important;
        }
        .pixel-card-val {
            font-size: 1.6rem !important;
        }
    }
    
</style>
"""
st.markdown(pixel_css, unsafe_allow_html=True)

# --- 3. 核心功能逻辑 ---

def get_fund_valuation(fund_code):
    url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        timestamp = int(time.time() * 1000)
        # 增加 timeout 防止手机网络不好时卡死
        response = requests.get(f"{url}?rt={timestamp}", headers=headers, timeout=3)
        if response.status_code == 200:
            pattern = re.compile(r'jsonpgz\((.*)\);')
            match = pattern.search(response.text)
            if match:
                return json.loads(match.group(1))
    except:
        pass
    return None

# --- 4. 页面内容布局 ---

# 标题区
st.markdown("<h1>👾 刘姣的小金库 💖</h1>", unsafe_allow_html=True)

greetings = [
    "刘姣，今天也要发财鸭！🦆",
    "叮咚！你的小钱钱正在赶来... 💰",
    "又是变富婆的一天呢~ 🌸",
    "记得多喝热水，少看跌幅~ ☕",
    "手机拿好，准备数钱！📱"
]
st.caption(f"✨ {random.choice(greetings)}")

# 侧边栏
with st.sidebar:
    st.markdown("### 🎮 玩家操作台")
    # 头像
    st.image("https://api.dicebear.com/7.x/pixel-art/svg?seed=LiuJiao&backgroundColor=ffdfbf", width=80)
    st.write("**玩家**: 刘姣 (手机版)")
    
    default_funds = "000001, 110011, 005827"
    user_input = st.text_area("🎫 投币口 (输入代码)", value=default_funds, height=100)
    
    # 增加两个按钮，方便手机操作
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        refresh = st.button("刷新")
    with col_btn2:
        if st.button("清空"):
             pass # 实际上Streamlit刷新页面逻辑比较特殊，这里仅作视觉占位或重置逻辑扩展

# 数据处理
fund_codes = [code.strip() for code in user_input.replace("，", ",").split(",") if code.strip()]

if fund_codes:
    # 手机端通常是一列显示，Streamlit的columns在手机端会自动堆叠
    # 但为了更好的控制，我们在手机端强制每行只显示一个大卡片，或者利用st.columns自动换行
    
    # 创建容器
    placeholder = st.container()

    # 模拟加载条
    my_bar = st.progress(0)
    
    # 使用 columns(2) 在桌面端是双列，手机端会自动变成单列
    col1, col2 = st.columns(2)
    cols = [col1, col2]
    
    for i, code in enumerate(fund_codes):
        data = get_fund_valuation(code)
        
        # 稍微快一点的进度条
        my_bar.progress((i + 1) / len(fund_codes))
        
        if data:
            name = data.get('name')
            gsz = data.get('gsz')
            gszzl = data.get('gszzl')
            gztime = data.get('gztime')[-5:]
            
            try:
                rate = float(gszzl)
                if rate > 0:
                    trend_icon = "🔥" 
                    trend_class = "up-text"
                    bg_color = "#FFF5F7" # 极淡粉红
                elif rate < 0:
                    trend_icon = "🍀" 
                    trend_class = "down-text"
                    bg_color = "#F5FFF5" # 极淡绿
                else:
                    trend_icon = "💤"
                    trend_class = ""
                    bg_color = "#FFFFFF"
            except:
                trend_icon = "❓"
                trend_class = ""
                bg_color = "#FFFFFF"

            # 轮流放入两列中
            target_col = cols[i % 2]
            
            # 优化后的 HTML 卡片
            # 1. 增加了 text-overflow 处理，防止基金名字太长撑破手机屏幕
            # 2. 使用了 flex 布局自动对齐
            card_html = f"""
            <div class="pixel-card" style="background-color: {bg_color}">
                <div class="pixel-card-name" style="
                    font-size: 1.2rem; 
                    border-bottom: 2px dashed #000; 
                    margin-bottom: 10px;
                    white-space: nowrap; 
                    overflow: hidden; 
                    text-overflow: ellipsis; 
                    width: 100%;">
                    {name} <span style="font-size: 0.8rem; color: #666">({code})</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <div class="pixel-card-val" style="font-size: 2rem; font-family: 'VT323';">{gsz}</div>
                    <div class="{trend_class}" style="font-size: 1.4rem;">{trend_icon} {gszzl}%</div>
                </div>
                <div style="text-align: right; font-size: 0.8rem; color: #888; margin-top: 5px;">
                    ⏰ {gztime}
                </div>
            </div>
            """
            target_col.markdown(card_html, unsafe_allow_html=True)
            
    my_bar.empty()
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #FF69B4; font-size: 0.9rem'>💖 MADE FOR LIUJIAO 💖</div>", unsafe_allow_html=True)

else:
    st.info("👈 点左上角箭头打开设置输入代码")
