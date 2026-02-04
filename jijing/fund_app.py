import streamlit as st
import requests
import re
import json
import pandas as pd
import time
import random

# --- 1. 页面基础配置 ---
st.set_page_config(
    page_title="刘姣的像素金库",
    page_icon="💖",
    layout="centered"
)

# --- 2. 注入“少女+像素”风格的 CSS ---
# 我们引入 Google Fonts 的 'VT323' 像素字体，并定义粉色系配色
pixel_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap');

    /* 全局背景：浅粉色 */
    .stApp {
        background-color: #FFF0F5;
        background-image: radial-gradient(#FFB6C1 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* 字体设置：优先使用像素字体，中文使用快乐体 */
    html, body, [class*="css"] {
        font-family: 'ZCOOL KuaiLe', 'VT323', monospace;
    }

    /* 标题样式：像素风阴影 */
    h1 {
        color: #FF1493;
        text-shadow: 2px 2px 0px #FFB6C1;
        font-size: 3.5rem !important;
        text-align: center;
    }

    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background-color: #FFE4E1;
        border-right: 4px dashed #FF69B4;
    }

    /* 按钮样式：复古游戏按钮 */
    div.stButton > button {
        background-color: #FF69B4;
        color: white;
        border: 4px solid #C71585;
        border-radius: 0px; /* 像素风不要圆角 */
        box-shadow: 4px 4px 0px #C71585;
        font-family: 'VT323', monospace;
        font-size: 20px;
        transition: all 0.1s;
    }
    div.stButton > button:active {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #C71585;
    }

    /* 卡片容器样式 */
    .pixel-card {
        background-color: #FFFFFF;
        border: 4px solid #000;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 6px 6px 0px #FF1493;
        position: relative;
    }

    /* 涨跌幅颜色覆盖 */
    .up-text { color: #FF0000; font-weight: bold; }
    .down-text { color: #32CD32; font-weight: bold; }
    
</style>
"""
st.markdown(pixel_css, unsafe_allow_html=True)

# --- 3. 核心功能逻辑 (保持不变) ---

def get_fund_valuation(fund_code):
    url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        timestamp = int(time.time() * 1000)
        response = requests.get(f"{url}?rt={timestamp}", headers=headers, timeout=5)
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

# 每日一句可爱问候
greetings = [
    "刘姣，今天也要发财鸭！🦆",
    "叮咚！你的小钱钱正在赶来... 💰",
    "又是变富婆的一天呢~ 🌸",
    "记得多喝热水，少看跌幅~ ☕"
]
st.caption(f"✨ {random.choice(greetings)} | 数据来源：天天基金")

# 侧边栏
with st.sidebar:
    st.markdown("### 🎮 玩家操作台")
    st.image("https://api.dicebear.com/7.x/pixel-art/svg?seed=LiuJiao", width=100) # 生成一个像素头像
    st.write("**玩家**: 刘姣 (Lv.99)")
    
    default_funds = "000001, 110011, 005827"
    user_input = st.text_area("🎫 投币口 (输入代码)", value=default_funds, height=100)
    
    if st.button("🕹️ 开始刷新"):
        st.rerun()

# 数据处理
fund_codes = [code.strip() for code in user_input.replace("，", ",").split(",") if code.strip()]

if fund_codes:
    # 进度条模拟加载游戏
    my_bar = st.progress(0)
    
    # 容器
    col1, col2 = st.columns(2)
    
    for i, code in enumerate(fund_codes):
        data = get_fund_valuation(code)
        
        # 模拟一点点复古加载延迟
        time.sleep(0.05)
        my_bar.progress((i + 1) / len(fund_codes))
        
        if data:
            name = data.get('name')
            gsz = data.get('gsz') # 估算值
            gszzl = data.get('gszzl') # 涨跌幅
            gztime = data.get('gztime')[-5:] # 只取时间 HH:mm
            
            # 判断涨跌图标
            try:
                rate = float(gszzl)
                if rate > 0:
                    trend_icon = "🔥" # 涨
                    trend_class = "up-text"
                    bg_color = "#FFF0F5" # 淡淡粉
                elif rate < 0:
                    trend_icon = "🍀" # 跌
                    trend_class = "down-text"
                    bg_color = "#F0FFF0" # 淡淡绿
                else:
                    trend_icon = "💤"
                    trend_class = ""
                    bg_color = "#FFFFFF"
            except:
                trend_icon = "❓"
                trend_class = ""
                bg_color = "#FFFFFF"

            # 决定放在左列还是右列
            target_col = col1 if i % 2 == 0 else col2
            
            # 使用 HTML 构建像素卡片
            card_html = f"""
            <div class="pixel-card" style="background-color: {bg_color}">
                <div style="font-size: 1.2rem; border-bottom: 2px dashed #000; margin-bottom: 10px;">
                    {name} <span style="font-size: 0.8rem; color: #666">({code})</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <div style="font-size: 2rem;">{gsz}</div>
                    <div class="{trend_class}" style="font-size: 1.5rem;">{trend_icon} {gszzl}%</div>
                </div>
                <div style="text-align: right; font-size: 0.8rem; color: #888; margin-top: 5px;">
                    ⏰ {gztime} 更新
                </div>
            </div>
            """
            target_col.markdown(card_html, unsafe_allow_html=True)
            
    my_bar.empty()
    
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #FF69B4;'>GAME OVER? NO, CONTINUE! 🪙</div>", unsafe_allow_html=True)

else:
    st.info("👈 请在左侧投币（输入基金代码）开始游戏！")
