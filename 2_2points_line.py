import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction

st.set_page_config(page_title="2点から直線を求める問題", layout="wide")

st.title("📐 2点から直線の式を求める（4択：整数・分数対応）")

# -------------------------
# 傾き候補（整数 + 指定分数）
# -------------------------
slope_candidates = [
    1, 2, 3, -1, -2, -3,
    Fraction(1,2), Fraction(2,3), Fraction(1,3), Fraction(3,4), Fraction(1,4),
    Fraction(-1,2), Fraction(-1,3), Fraction(-2,3), Fraction(-3,4), Fraction(-1,4)
]

# -------------------------
# 分数を文字列に変換
# -------------------------
def frac_to_str(fr):
    if isinstance(fr, int):
        return str(fr)
    return f"{fr.numerator}/{fr.denominator}"

# -------------------------
# 式を文字列化
# -------------------------
def line_to_str(m, b):
    m_str = frac_to_str(m)
    b_str = frac_to_str(b)

    if b >= 0:
        return f"y = {m_str}x + {b_str}"
    else:
        return f"y = {m_str}x - {frac_to_str(-b)}"

# -------------------------
# 問題生成
# -------------------------
def generate_problem():
    m = random.choice(slope_candidates)

    # x1 を整数で選ぶ
    x1 = random.randint(-5, 5)
    y1 = random.randint(-5, 5)

    # x2 は x1 と異なる整数
    x2 = x1 + random.choice([-3, -2, -1, 1, 2, 3])

    # y2 = y1 + m*(x2 - x1)
    y2 = y1 + m * (x2 - x1)

    # 切片 b = y1 - m*x1
    b = y1 - m * x1

    correct = line_to_str(m, b)

    # 誤答生成（整数 or 分数）
    wrong_choices = []
    for _ in range(3):
        m_wrong = random.choice(slope_candidates)
        b_wrong = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        wrong_choices.append(line_to_str(m_wrong, b_wrong))

    choices = [correct] + wrong_choices
    random.shuffle(choices)

    return (x1, y1), (x2, y2), m, b, correct, choices

# -------------------------
# セッション初期化
# -------------------------
if "problem" not in st.session_state:
    st.session_state.problem = generate_problem()

if "result" not in st.session_state:
    st.session_state.result = None

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "correct_count" not in st.session_state:
    st.session_state.correct_count = 0

if "total_count" not in st.session_state:
    st.session_state.total_count = 0

# 最初の問題開始時刻を記録
if st.session_state.start_time is None:
    st.session_state.start_time = st.time()

p1, p2, m, b, correct, choices = st.session_state.problem

st.subheader("次の2点を通る直線の式を選びなさい")
st.write(f"点 A: {p1}, 点 B: {p2}")

selected = st.radio("選択肢", choices, index=None)

# -------------------------
# 判定
# -------------------------
if st.button("判定する"):
    if selected is None:
        st.warning("選択肢を選んでください")
    else:
        st.session_state.total_count += 1

        if selected == correct:
            st.success("正解です！")
            st.session_state.correct_count += 1
            st.session_state.result = "correct"
        else:
            st.error(f"不正解… 正解は **{correct}** です")
            st.session_state.result = "wrong"

        # グラフ描画
        fig, ax = plt.subplots(figsize=(6, 4))

        ax.scatter([p1[0], p2[0]], [p1[1], p2[1]], color="red", label="与えられた点")

        xs = np.linspace(-10, 10, 200)
        ys_correct = [float(m) * x + float(b) for x in xs]
        ax.plot(xs, ys_correct, label="正解の直線", color="blue")

        # 誤答の直線
        if selected != correct:
            sel = selected.replace("y = ", "")
            m_s, b_s = sel.split("x")
            m_s = Fraction(m_s)
            b_s = Fraction(b_s.replace("+", ""))

            ys_wrong = [float(m_s) * x + float(b_s) for x in xs]
            ax.plot(xs, ys_wrong, label="あなたの選んだ直線", color="green", linestyle="--")

        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

# -------------------------
# 次の問題
# -------------------------
if st.button("次の問題へ"):
    st.session_state.problem = generate_problem()
    st.session_state.result = None
    st.rerun()

# -------------------------
# 終了ボタン（解答時間・正答率を表示）
# -------------------------
if st.button("終了する"):

    end_time = st.time()
    elapsed = end_time - st.session_state.start_time

    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    if st.session_state.total_count > 0:
        accuracy = st.session_state.correct_count / st.session_state.total_count * 100
    else:
        accuracy = 0

    st.write("## 📘 学習を終了しました。お疲れさまでした。")
    st.write(f"### ⏱ 解答時間：{minutes} 分 {seconds} 秒")
    st.write(f"### 🎯 正答率：{st.session_state.correct_count} / {st.session_state.total_count}（{accuracy:.1f}%）")

    st.session_state.clear()
    st.stop()
