import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction
import time

st.set_page_config(page_title="4本の直線から選ぶ問題", layout="wide")

st.title("📐 一次関数の式に対応する直線を選びなさい")

# -------------------------
# 傾き候補（整数 + 指定分数）
# -------------------------
slope_candidates = [
    1, 2, 3, -1, -2, -3,
    Fraction(1,2), Fraction(2,3), Fraction(1,3), Fraction(3,4), Fraction(1,4),
    Fraction(-1,2), Fraction(-1,3), Fraction(-2,3), Fraction(-3,4), Fraction(-1,4)
]

# -------------------------
# 分数を LaTeX 文字列に変換
# -------------------------
def frac_to_str(fr):
    if isinstance(fr, int):
        return str(fr)
    return f"\\frac{{{fr.numerator}}}{{{fr.denominator}}}"

# -------------------------
# 一次関数を LaTeX 文字列に変換
# -------------------------
def line_to_str(m, b):
    # 傾き
    if m == 1:
        m_str = "x"
    elif m == -1:
        m_str = "-x"
    else:
        m_str = f"{frac_to_str(m)}x"

    # 切片
    if b == 0:
        return f"$y = {m_str}$"
    elif b > 0:
        return f"$y = {m_str} + {frac_to_str(b)}$"
    else:
        return f"$y = {m_str} - {frac_to_str(-b)}$"

# -------------------------
# ランダムな一次関数を生成
# -------------------------
def generate_line():
    m = random.choice(slope_candidates)
    b = random.randint(-5, 5)
    return m, b

# -------------------------
# 問題生成（正解1本 + 誤答3本）
# -------------------------
def generate_problem():
    # 正解の直線
    m, b = generate_line()
    correct_eq = line_to_str(m, b)

    # 誤答3本
    wrong_lines = []
    while len(wrong_lines) < 3:
        m2, b2 = generate_line()
        if (m2, b2) != (m, b):
            wrong_lines.append((m2, b2))

    # 4本の直線をまとめる
    lines = [(m, b)] + wrong_lines
    random.shuffle(lines)

    # 正解の index
    correct_index = lines.index((m, b))

    return lines, correct_index, correct_eq

# -------------------------
# セッション初期化
# -------------------------
if "problem" not in st.session_state:
    st.session_state.problem = generate_problem()

if "correct_count" not in st.session_state:
    st.session_state.correct_count = 0

if "total_count" not in st.session_state:
    st.session_state.total_count = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# -------------------------
# 現在の問題
# -------------------------
lines, correct_index, correct_eq = st.session_state.problem

# -------------------------
# グラフ描画
# -------------------------
fig, ax = plt.subplots(figsize=(6, 6))

xs = np.linspace(-10, 10, 200)

for i, (m, b) in enumerate(lines):
    ys = [float(m) * x + float(b) for x in xs]
    ax.plot(xs, ys, label=f"{i+1}番の直線")

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.grid(True)
ax.legend()
st.pyplot(fig)

# -------------------------
# 問題文
# -------------------------
st.markdown(f"### 次の一次関数に対応する直線を選びなさい：{correct_eq}")

# -------------------------
# ラジオボタン（ヌル値）
# -------------------------
selected = st.radio("選択肢", [1, 2, 3, 4], index=None)

# -------------------------
# 答え合わせ
# -------------------------
if st.button("答え合わせ"):
    if selected is None:
        st.warning("選択肢を選んでください")
    else:
        st.session_state.total_count += 1

        if selected - 1 == correct_index:
            st.success("正解です！")
            st.session_state.correct_count += 1
        else:
            st.error(f"不正解… 正解は **{correct_index+1}番の直線** です")

        # 正答率表示
        accuracy = st.session_state.correct_count / st.session_state.total_count * 100
        st.write(f"### 正解数：{st.session_state.correct_count}")
        st.write(f"### 問題数：{st.session_state.total_count}")
        st.write(f"### 正答率：{accuracy:.1f}%")

# -------------------------
# 次の問題
# -------------------------
if st.button("次の問題"):
    st.session_state.problem = generate_problem()
    st.rerun()

# -------------------------
# 終了
# -------------------------
if st.button("終了"):
    end_time = time.time()
    elapsed = end_time - st.session_state.start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    accuracy = (
        st.session_state.correct_count / st.session_state.total_count * 100
        if st.session_state.total_count > 0 else 0
    )

    st.write("## 📘 学習を終了しました。お疲れさまでした。")
    st.write(f"### ⏱ 解答時間：{minutes}分 {seconds}秒")
    st.write(f"### 🎯 正答率：{st.session_state.correct_count} / {st.session_state.total_count}（{accuracy:.1f}%）")

    st.session_state.clear()
    st.stop()
