import streamlit as st
import random

# --------------------------------
# 直線の式を y = mx + b の形に整える
# --------------------------------
def line_equation_from_two_points(x1, y1, x2, y2):
    if x1 == x2:
        return f"x = {x1}"

    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    m = round(m, 2)
    b = round(b, 2)

    if b >= 0:
        return f"y = {m}x + {b}"
    else:
        return f"y = {m}x - {abs(b)}"


def line_equation_from_point_slope(x1, y1, m):
    if m == 0:
        return f"y = {y1}"

    b = y1 - m * x1
    m = round(m, 2)
    b = round(b, 2)

    if b >= 0:
        return f"y = {m}x + {b}"
    else:
        return f"y = {m}x - {abs(b)}"


# --------------------------------
# 誤答を作る
# --------------------------------
def make_choices(correct):
    choices = {correct}
    while len(choices) < 4:
        dx = random.randint(-3, 3)
        dy = random.randint(-3, 3)
        wrong = correct.replace("x", f"{1+dx}x").replace("+", f"+{dy}")
        if wrong != correct:
            choices.add(wrong)
    return random.sample(list(choices), 4)


# --------------------------------
# 2点が与えられる問題（1問は必ず x = a）
# --------------------------------
def generate_two_point_set():
    problems = []

    # ★ 必ず1問は x = a の直線
    a = random.randint(-5, 5)
    y1 = random.randint(-5, 5)
    y2 = random.randint(-5, 5)
    correct = f"x = {a}"
    problem_text = f"点 ({a}, {y1}) と ({a}, {y2}) を通る直線は？"
    choices = make_choices(correct)
    problems.append((problem_text, correct, choices))

    # 残り4問
    for _ in range(4):
        x1 = random.randint(-5, 5)
        y1 = random.randint(-5, 5)
        x2 = random.randint(-5, 5)
        y2 = random.randint(-5, 5)

        if x1 == x2:
            x2 += 1

        correct = line_equation_from_two_points(x1, y1, x2, y2)
        problem_text = f"点 ({x1}, {y1}) と ({x2}, {y2}) を通る直線は？"
        choices = make_choices(correct)
        problems.append((problem_text, correct, choices))

    return problems


# --------------------------------
# 1点と傾きが与えられる問題（3回に1回は水平線）
# --------------------------------
def generate_point_slope_set():
    problems = []

    for _ in range(5):
        x1 = random.randint(-5, 5)
        y1 = random.randint(-5, 5)

        # ★ 3回に1回は水平線
        if random.random() < 1/3:
            m = 0
        else:
            m = random.randint(-5, 5)

        correct = line_equation_from_point_slope(x1, y1, m)
        problem_text = f"点 ({x1}, {y1}) を通り、傾き {m} の直線は？"
        choices = make_choices(correct)
        problems.append((problem_text, correct, choices))

    return problems


# --------------------------------
# Streamlit UI
# --------------------------------

st.title("直線の4択問題（5問セット）")

mode = st.radio("出題形式を選んでください", ["2点が与えられる", "1点と傾きが与えられる"])

if st.button("問題を生成する"):
    st.session_state.answers = {}
    if mode == "2点が与えられる":
        st.session_state.problems = generate_two_point_set()
    else:
        st.session_state.problems = generate_point_slope_set()

if "problems" not in st.session_state:
    st.stop()

problems = st.session_state.problems

st.subheader("【5問セット】")

for i, (text, correct, choices) in enumerate(problems):
    st.write(f"**第{i+1}問：{text}**")
    st.session_state.answers[i] = st.radio(
        f"あなたの解答（第{i+1}問）",
        choices,
        key=f"q{i}",
        index=None
    )

# --------------------------------
# 採点
# --------------------------------
if st.button("採点する"):
    score = 0
    st.subheader("【採点結果】")

    for i, (text, correct, choices) in enumerate(problems):
        user_ans = st.session_state.answers[i]
        if user_ans == correct:
            st.success(f"第{i+1}問：正解 → {correct}")
            score += 1
        else:
            st.error(f"第{i+1}問：不正解（あなたの答え = {user_ans}、正解 = {correct}）")

    st.write(f"### 合計得点：**{score} / 5**")

    if st.button("もう一度"):
        st.session_state.clear()
        st.experimental_rerun()

    if st.button("終了"):
        st.session_state.clear()
        st.write("お疲れさまでした。")
