def generate_problem():
    m = random.choice(slope_candidates)

    x1 = random.randint(-5, 5)
    y1 = random.randint(-5, 5)

    # dx の候補を作る（最大5まで）
    if isinstance(m, int):
        # 整数傾き → dx は ±1〜±5 の中から選ぶ
        dx_candidates = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
    else:
        # 分数傾き → 分母 q の倍数で、かつ |dx| ≤ 5
        q = m.denominator
        dx_candidates = [k for k in range(-5, 6) if k != 0 and k % q == 0]

    dx = random.choice(dx_candidates)

    x2 = x1 + dx
    y2 = y1 + m * dx  # 必ず整数になる

    b = y1 - m * x1
    correct = line_to_str(m, b)

    wrong_choices = []
    for _ in range(3):
        m_wrong = random.choice(slope_candidates)
        b_wrong = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        wrong_choices.append(line_to_str(m_wrong, b_wrong))

    choices = [correct] + wrong_choices
    random.shuffle(choices)

    return (x1, y1), (x2, y2), m, b, correct, choices
