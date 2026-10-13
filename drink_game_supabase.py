import streamlit as st
import random
import json
import os

# ====================== 页面配置 ======================
st.set_page_config(
    page_title="酒局小游戏🍻",
    page_icon="🍺",
    layout="wide"
)

# ====================== 默认题库 ======================
default_truth = [
    "说出你谈过几段恋爱",
    "现场说一个你最深的秘密",
    "在场最喜欢谁的性格",
    "第一次喝酒是什么时候",
    "有没有偷偷暗恋过别人",
    "说出自己一个最大缺点",
    "最近熬夜在干什么",
    "最尴尬的一次经历",
    "有没有骗过好朋友",
    "理想的结婚年龄"
]

default_dare = [
    "干一口酒！🍻",
    "和身边人对视10秒不许笑",
    "模仿表情包连续5个",
    "大声朗读一段土味情话",
    "做10个深蹲",
    "给任意好友发消息：我喜欢你",
    "用夹子音说一句话",
    "原地转5圈不摔倒",
    "让左手边的人捏脸",
    "跑调唱一句歌"
]

default_drink_task = [
    "全场最轻的人喝半杯",
    "指定一个人陪你喝一口",
    "免罚！幸运儿🥳",
    "直接干一杯！！",
    "只能左手拿杯子喝酒",
    "全场一起碰杯",
    "下一轮抽到你双倍惩罚",
    "挑选一人互换本轮惩罚"
]

DATA_FILE = "game_data.json"

# 加载数据
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "custom_truth": [],
            "custom_dare": [],
            "custom_drink": [],
            "players": {},
            "forbidden_words": []
        }

# 保存数据
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 初始化session
if "init" not in st.session_state:
    st.session_state.db = load_data()
    st.session_state.card_result = None
    st.session_state.dice_num = 0
    st.session_state.dice_res = ""
    st.session_state.wheel_result = None
    st.session_state.forbidden_word = ""
    st.session_state.init = True

db = st.session_state.db

def sync_save():
    save_data(db)

# 组装全部卡片
def get_all_cards():
    cards = []
    for item in default_truth + db["custom_truth"]:
        cards.append({"type": "🤍 真心话", "content": item})
    for item in default_dare + db["custom_dare"]:
        cards.append({"type": "💥 大冒险", "content": item})
    for item in default_drink_task + db["custom_drink"]:
        cards.append({"type": "🍷 喝酒任务", "content": item})
    return cards

# 页面标题
st.title("🍻 万能酒局小游戏")
st.divider()

# 一键重置
if st.button("⚠️ 一键清空全部数据", use_container_width=True):
    db["custom_truth"] = []
    db["custom_dare"] = []
    db["custom_drink"] = []
    db["players"] = {}
    db["forbidden_words"] = []
    st.session_state.forbidden_word = ""
    sync_save()
    st.warning("✅ 所有数据清空完成！")

# 玩家管理
st.subheader("👥 玩家管理（记录罚酒杯数）")
col_p1, col_p2, col_p3 = st.columns([3,1,1])
with col_p1:
    new_player_name = st.text_input("输入玩家名字", placeholder="例如：小明")
with col_p2:
    if st.button("➕ 添加玩家") and new_player_name.strip():
        name = new_player_name.strip()
        if name not in db["players"]:
            db["players"][name] = 0
            sync_save()
with col_p3:
    if st.button("🗑️ 清空全部玩家"):
        db["players"] = {}
        sync_save()

# 玩家榜单
if db["players"]:
    st.markdown("### 📊 罚酒榜单")
    for name, count in db["players"].items():
        c1, c2, c3 = st.columns([2,1,1])
        c1.write(f"**{name}**")
        c2.write(f"{count} 杯")
        with c3:
            b1, b2 = st.columns(2)
            if b1.button("➕", key=f"add_{name}"):
                db["players"][name] += 1
                sync_save()
            if b2.button("➖", key=f"sub_{name}") and db["players"][name]>0:
                db["players"][name] -=1
                sync_save()
else:
    st.info("请添加玩家，开始游戏！")

st.divider()

# 自定义题库
st.subheader("📝 自定义题库管理")
tab_t, tab_d, tab_dk = st.tabs(["🤍 真心话", "💥 大冒险", "🍷 喝酒任务"])
with tab_t:
    new_t = st.text_input("新增真心话题目", placeholder="写题目")
    if st.button("添加真心话", use_container_width=True):
        if new_t.strip():
            db["custom_truth"].append(new_t.strip())
            sync_save()
            st.success("添加成功！")
    st.write(f"自定义真心话数量：{len(db['custom_truth'])}")
    for idx, txt in enumerate(db["custom_truth"]):
        ca, cb = st.columns([5,1])
        ca.write(txt)
        if cb.button("删除", key=f"del_t_{idx}"):
            db["custom_truth"].pop(idx)
            sync_save()
            st.rerun()

with tab_d:
    new_d = st.text_input("新增大冒险题目", placeholder="写任务")
    if st.button("添加大冒险", use_container_width=True):
        if new_d.strip():
            db["custom_dare"].append(new_d.strip())
            sync_save()
            st.success("添加成功！")
    st.write(f"自定义大冒险数量：{len(db['custom_dare'])}")
    for idx, txt in enumerate(db["custom_dare"]):
        ca, cb = st.columns([5,1])
        ca.write(txt)
        if cb.button("删除", key=f"del_d_{idx}"):
            db["custom_dare"].pop(idx)
            sync_save()
            st.rerun()

with tab_dk:
    new_dk = st.text_input("新增喝酒任务", placeholder="写任务")
    if st.button("添加喝酒任务", use_container_width=True):
        if new_dk.strip():
            db["custom_drink"].append(new_dk.strip())
            sync_save()
            st.success("添加成功！")
    st.write(f"自定义喝酒任务数量：{len(db['custom_drink'])}")
    for idx, txt in enumerate(db["custom_drink"]):
        ca, cb = st.columns([5,1])
        ca.write(txt)
        if cb.button("删除", key=f"del_dk_{idx}"):
            db["custom_drink"].pop(idx)
            sync_save()
            st.rerun()

st.divider()

# 4个游戏标签页
tab1, tab2, tab3, tab4 = st.tabs(["🎴 抽卡游戏", "🎲 骰子猜大小", "🎡 幸运转盘", "🚫 禁词游戏"])

# 1.抽卡
with tab1:
    st.subheader("随机抽卡｜真心话/大冒险/喝酒任务")
    st.info("抽到喝酒任务，在上方榜单手动增加杯数")
    all_cards = get_all_cards()
    if st.button("🔥 抽卡！", use_container_width=True):
        st.session_state.card_result = random.choice(all_cards)
    if st.session_state.card_result:
        res = st.session_state.card_result
        st.markdown(f"# {res['type']}")
        st.markdown(f"## {res['content']}")

#2.骰子猜大小
with tab2:
    st.subheader("🎲 骰子猜大小")
    st.info("1~3小，4~6大，猜错罚一杯！")
    if db["players"]:
        player_sel = st.selectbox("本轮玩家", list(db["players"].keys()))
        choose = st.radio("选择", ["猜大", "猜小"])
        if st.button("掷骰子！", use_container_width=True):
            num = random.randint(1,6)
            st.session_state.dice_num = num
            res_word = "小" if num <=3 else "大"
            st.session_state.dice_res = res_word
            if choose == f"猜{res_word}":
                st.success(f"🎉 {player_sel}！点数：{num}，是{res_word}，猜对啦！")
            else:
                st.error(f"😭 {player_sel}！点数：{num}，是{res_word}，猜错，罚一杯！")
                db["players"][player_sel] += 1
                sync_save()
    else:
        st.warning("请先添加玩家！")

#3.幸运转盘
with tab3:
    st.subheader("🎡幸运转盘，和抽卡共用题库")
    all_cards = get_all_cards()
    if st.button("🎡转动转盘！", use_container_width=True):
        st.session_state.wheel_result = random.choice(all_cards)
    if st.session_state.wheel_result:
        res = st.session_state.wheel_result
        st.markdown(f"# {res['type']}")
        st.markdown(f"## {res['content']}")

#4.禁词游戏
with tab4:
    st.subheader("🚫 禁词游戏：聊天不能说这个词！")
    col_f1, col_f2 = st.columns([3,1])
    with col_f1:
        forbid_input = st.text_input("添加禁词", placeholder="你、我、喝、是")
    with col_f2:
        if st.button("➕添加禁词") and forbid_input.strip():
            w = forbid_input.strip()
            if w not in db["forbidden_words"]:
                db["forbidden_words"].append(w)
                sync_save()
                st.success("添加成功")
    st.markdown("### 当前禁词库")
    if db["forbidden_words"]:
        for idx, w in enumerate(db["forbidden_words"]):
            ca, cb = st.columns([4,1])
            ca.write(f"🔴 {w}")
            if cb.button("删除", key=f"del_forbid_{idx}"):
                db["forbidden_words"].pop(idx)
                sync_save()
                st.rerun()
        st.divider()
        if st.button("🎲随机抽取本轮禁词", use_container_width=True):
            st.session_state.forbidden_word = random.choice(db["forbidden_words"])
        if st.session_state.forbidden_word:
            st.markdown(f"# 本轮禁词：`{st.session_state.forbidden_word}`")
            st.warning("所有人禁止说出这个词！")
            if db["players"]:
                offender = st.selectbox("谁违规说了禁词？", list(db["players"].keys()))
                if st.button("✅判定违规，罚一杯", use_container_width=True):
                    db["players"][offender] +=1
                    sync_save()
                    st.error(f"{offender} 说出禁词，罚一杯！")
    else:
        st.info("禁词库为空，请添加禁词！")

st.divider()
st.caption("💡温馨提示：适度饮酒，请勿酗酒，酒后不开车！")
