import streamlit as st
import random
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

# 日本語フォントを優先（環境にあるものが使われる）
matplotlib.rcParams["font.family"] = [
    "Yu Mincho",      # Windows 10 以降によく入っている
    "MS Mincho",
    "MS Gothic",
    "IPAexMincho",
    "IPAexGothic"
]

# マイナス記号の文字化け防止
matplotlib.rcParams["axes.unicode_minus"] = False


st.set_page_config(page_title="2次関数（頂点と1点）5択トレーニング", layout="centered")
x = sp.Symbol("x")

# ============================================================
# グラフ描画（軸つき）
# ============================================================
def plot_quadratic_with_points(f, p, q, x1, y1):
    f_lam = sp.lambdify(x, f, "numpy")

    xs = np.linspace(p - 5, p + 5, 400)
    ys = f_lam(xs)

    fig, ax = plt.subplots(figsize=(5, 4))

    ax.plot(xs, ys, label="y = f(x)", color="blue")
    ax.scatter([p], [q],   color="red",   s=80, label="頂点 (p, q)")
    ax.scatter([x1], [y1], color="green", s=80, label="通る点 (x1, y1)")
    ax.axvline(p, color="purple", linestyle="--", linewidth=2, label="軸 x = p")

    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

# ============================================================
# 一般形 → 基本形（平方完成）の解説
# ============================================================
def explain_vertex_form(f):
    expanded = sp.expand(f)
    a = expanded.coeff(x, 2)
    b = expanded.coeff(x, 1)
    c = expanded.coeff(x, 0)

    p = -b / (2*a)
    q = c - b**2/(4*a)

    explanation = f"""
### 一般形 → 基本形（頂点形式）への変形

与えられた一般形  
\

\[
y = {sp.latex(a)}x^2 + {sp.latex(b)}x + {sp.latex(c)}
\\]



---

#### ① a をくくり出す  
\

\[
y = {sp.latex(a)}\\left(x^2 + {sp.latex(b/a)}x\\right) + {sp.latex(c)}
\\]



#### ② 平方完成する  
\

\[
x^2 + {sp.latex(b/a)}x
= \\left(x + {sp.latex(b/(2*a))}\\right)^2 - {sp.latex((b/(2*a))**2)}
\\]



#### ③ 頂点形式にまとめる  
\

\[
y = {sp.latex(a)}\\left(x - ({sp.latex(p)})\\right)^2 + {sp.latex(q)}
\\]



---

#### よって頂点は  
\

\[
({sp.latex(p)},\ {sp.latex(q)})
\\]


"""
    return explanation

# ============================================================
# 2次関数の生成：頂点 (p, q) と 1 点 (x1, y1)
# ============================================================


def generate_quadratic_problem(a_type="int"):
    p = random.randint(-5, 5)
    q = random.randint(-5, 5)

    d = random.randint(1, 5)
    x1 = p + random.choice([-d, d])

    # a の決定
    if a_type == "fraction":
        numerator = random.choice([1, 2, -1, -2])
        denominator = random.choice([2, 3])
        a = sp.Rational(numerator, denominator)
    else:
        a = random.choice([-3, -2, -1, 1, 2, 3])

    y1 = a * (x1 - p)**2 + q

    # 正解（一般形）
    f_vertex = a * (x - p)**2 + q
    f = sp.expand(f_vertex)

    # --------------------------------------------------------
    # 誤答の a を作る（小数禁止）★ここが関数内に必要
    # --------------------------------------------------------
    wrong_as = []

    candidates = [
        a * 2,
        a / 2,
        -a,
        a + sp.Rational(1, 1),
        a - sp.Rational(1, 1)
    ]

    for cand in candidates:
        if cand != a and cand not in wrong_as:
            wrong_as.append(cand)
        if len(wrong_as) == 4:
            break

    # 誤答の一般形
    wrong_fs = [sp.expand(A * (x - p)**2 + q) for A in wrong_as]

    # 選択肢
    options = [f] + wrong_fs
    random.shuffle(options)
    correct_idx = options.index(f)

    return {
        "p": p,
        "q": q,
        "x1": x1,
        "y1": y1,
        "options": options,
        "correct_idx": correct_idx,
        "f": f,
        "a": a
    }



# ============================================================
# 5 題セット生成（難易度順）
# ============================================================
def build_set():
    problems = []
    seen = set()

    # 易しい：a = ±1 の整数
    while len([p for p in problems if abs(p["a"]) == 1 and isinstance(p["a"], int)]) < 2:
        prob = generate_quadratic_problem("int")
        if abs(prob["a"]) == 1:
            key = (prob["p"], prob["q"], prob["x1"], prob["y1"])
            if key not in seen:
                seen.add(key)
                problems.append(prob)

    # 中間：a = ±2, ±3 の整数
    while len([p for p in problems if isinstance(p["a"], int)]) < 4:
        prob = generate_quadratic_problem("int")
        if abs(prob["a"]) in [2, 3]:
            key = (prob["p"], prob["q"], prob["x1"], prob["y1"])
            if key not in seen:
                seen.add(key)
                problems.append(prob)

    # 難しい：分数係数（1題）
    while len(problems) < 5:
        prob = generate_quadratic_problem("fraction")
        key = (prob["p"], prob["q"], prob["x1"], prob["y1"])
        if key not in seen:
            seen.add(key)
            problems.append(prob)

    return problems

# ============================================================
# セッション管理
# ============================================================
if "problems" not in st.session_state:
    st.session_state.problems = []
if "selects" not in st.session_state:
    st.session_state.selects = [None] * 5
if "checked" not in st.session_state:
    st.session_state.checked = False
if "set_id" not in st.session_state:
    st.session_state.set_id = 0

# ============================================================
# UI
# ============================================================
st.title("2次関数（頂点と1点）5択トレーニング")

if st.button("5題を生成する"):
    st.session_state.problems = build_set()
    st.session_state.selects = [None] * 5
    st.session_state.checked = False
    st.session_state.set_id += 1

probs = st.session_state.problems

if probs:
    st.markdown("### 頂点と1点から 2 次関数を選んでください")

    for i, p in enumerate(probs):
        st.markdown(f"#### 【問題 {i+1}】")

        st.latex(rf"\text{{頂点 }}({p['p']}, {p['q']})")
        st.latex(rf"\text{{通る点 }}({p['x1']}, {p['y1']})")

        labels = [f"$y = {sp.latex(opt)}$" for opt in p["options"]]

        choice = st.radio(
            f"選択肢（問題 {i+1}）",
            options=list(range(5)),
            format_func=lambda j, labels=labels: labels[j],
            index=None,
            key=f"choice_{st.session_state.set_id}_{i}",
        )
        st.session_state.selects[i] = choice

    if st.button("採点する"):
        st.session_state.checked = True

    if st.session_state.checked:
        st.markdown("## 採点結果")

        correct_now = 0
        for i, p in enumerate(probs):
            user = st.session_state.selects[i]
            st.markdown(f"### 【問題 {i+1}】")

            if user == p["correct_idx"]:
                st.success("正解")
                correct_now += 1
            else:
                st.error("不正解")

            st.latex(rf"正しい式：\ y = {sp.latex(p['f'])}")

            plot_quadratic_with_points(
                p['f'],
                p['p'], p['q'],
                p['x1'], p['y1']
            )

            st.markdown(explain_vertex_form(p['f']))

        st.markdown(f"## このセットの正答数：{correct_now} / 5")

        if st.button("次の問題セットへ"):
            st.session_state.problems = build_set()
            st.session_state.selects = [None] * 5
            st.session_state.checked = False
            st.session_state.set_id += 1

else:
    st.info("「5題を生成する」を押してください。")
