import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="2点から直線を求める問題", layout="wide")

st.title("📐 2点から直線の式を求める（4択問題）")

# -------------------------
# 問題生成関数
# -------------------------
def generate_problem(level=1):
    # 難易度に応じて点の範囲を調整
    if level == 1:
        low, high = -5, 5
    else:
        low, high = -8, 8

    x1, y1 = random.randint(low, high), random.randint(low, high)
    x2, y2 = random.randint(low, high), random.randint(low, high)

    # x1 = x2 の場合は縦線になるので避ける（別問題で扱う）
    while x1 == x2:
        x2 = random.randint(low, high)

    # 傾きと切片
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    # 正解の式
    correct = f"y = {m:.2f}x + {b:.2f}"

    # 誤答生成（傾きミス・切片ミスなど）
    wrong1 = f"y = {m + random.choice([-2, -1, 1, 2]):.2f}x + {b:.2f}"
    wrong2 = f"y = {m:.2f}x + {b + random.choice([-3, -2, 2, 3]):.2f}"
    wrong3 = f"y = {m + random.choice([-1, 1]):.2f}x + {b + random.choice([-1, 1]):.2f}"

    choices = [correct, wrong1, wrong2, wrong3]
    random.shuffle(choices)

    return (x1, y1), (x2, y2), correct, choices


# -------------------------
# セッション状態の初期化
# -------------------------
if "problem" not in st.session_state:
    st.session_state.problem = None
if "level" not in st.session_state:
    st.session_state.level = 1
if "result" not in st.session_state:
    st.session_state.result = None


# -------------------------
# 新しい問題を生成
# -------------------------
if st.session_state.problem is None:
    st.session_state.problem = generate_problem(st.session_state.level)

p1, p2, correct, choices = st.session_state.problem

st.subheader("次の2点を通る直線の式を選びなさい")
st.write(f"点 A: {p1}, 点 B: {p2}")

# -------------------------
# 選択肢
# -------------------------
selected = st.radio("選択肢", choices, index=None)

# -------------------------
# 判定ボタン
# -------------------------
if st.button("判定する"):
    if selected is None:
        st.warning("選択肢を選んでください")
    else:
        if selected == correct:
            st.success("正解です！")
            st.session_state.result = "correct"
        else:
            st.error(f"不正解… 正解は **{correct}** です")
            st.session_state.result = "wrong"

        # グラフ描画
        fig, ax = plt.subplots(figsize=(6, 4))

        # 点を描画
        ax.scatter([p1[0], p2[0]], [p1[1], p2[1]], color="red", label="与えられた点")

        # x 範囲
        xs = np.linspace(-10, 10, 200)

        # 正解の直線
        m_c = float(correct.split("x")[0].replace("y = ", ""))
        b_c = float(correct.split("+")[1])
        ys_correct = m_c * xs + b_c
        ax.plot(xs, ys_correct, label="正解の直線", color="blue")

        # 誤答の直線（選んだ場合のみ）
        if selected != correct:
            m_w = float(selected.split("x")[0].replace("y = ", ""))
            b_w = float(selected.split("+")[1])
            ys_wrong = m_w * xs + b_w
            ax.plot(xs, ys_wrong, label="あなたの選んだ直線", color="green", linestyle="--")

        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

# -------------------------
# 次の問題ボタン
# -------------------------
if st.button("次の問題へ"):
    # 個別最適化：正解なら難易度を上げる
    if st.session_state.result == "correct":
        st.session_state.level = min(2, st.session_state.level + 1)
    else:
        st.session_state.level = 1

    st.session_state.problem = generate_problem(st.session_state.level)
    st.session_state.result = None
    st.experimental_rerun()
