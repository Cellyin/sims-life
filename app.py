import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 角色状态初始化
def reset_state():
    return {
        "age": 0,
        "money": 0,
        "health": 100,
        "stress": 10,
        "debt": 0,
        "education": { "level": "none", "in_school": False },
        "career": { "track": "none", "seniority": 0, "income_level": 0 },
        "relationship": { "status": "single", "quality": 50, "years_together": 0, "no_kids_choice": False },
        "children": [],
        "family": {
            "wealth_tier": None,
            "parents_type": None,
            "parents_relation": None,
            "siblings_count": 0,
            "birth_order": "only"
        },
        "personality": {
            "self_worth_external": 50,
            "belonging_need": 50,
            "intimacy_desire": 50,
            "conflict_direct": 50
        },
        "history": {
            "year_lines": [],
            "key_choices": [],
            "themes_counter": {}
        }
    }

# 初始化游戏状态
state = reset_state()

# 年度旁白库
year_lines = {
    "0-6": [
        "你的记忆有些模糊，只记得家里总是很忙",
        "你还不知道什么叫选择，日子围着家转",
        "你学会了看大人的脸色",
        "你被照顾着，也被忽略过",
        "你偶尔哭闹，但世界照样往前走"
    ],
    "7-12": [
        "你开始适应上学的节奏",
        "作业变多了，你有点不情愿",
        "你在班里找到了一个还不错的位置",
        "你开始注意到谁更受欢迎",
        "你第一次因为同学的事不开心"
    ],
    "13-18": [
        "你开始更在意别人的眼光",
        "你开始把自己放进比较里",
        "你有了一点说不清的情绪",
        "你开始怀疑自己是不是不够好",
        "你变得敏感，但又不想被看出来"
    ],
    "18-30": [
        "你在现实里继续前行",
        "你忙着把日子过下去",
        "这一年过得很快，你没来得及细想",
        "你做了些妥协，也保留了些坚持",
        "你觉得自己好像一直在补救"
    ]
}

# 随机事件库
random_events = {
    "18-30": [
        {"event": "你决定是否上大学", "choices": ["上大学", "打工", "创业"]},
        {"event": "你面临是否贷款上大学的选择", "choices": ["贷款", "不贷款", "找奖学金"]},
        {"event": "你决定去参加一家公司面试", "choices": ["积极应聘", "不感兴趣", "犹豫不决"]},
        {"event": "你决定创业", "choices": ["申请创业贷款", "寻找合伙人", "放弃创业"]},
    ]
}

# 恋爱系统
def start_dating():
    if state["relationship"]["status"] == "single" and random.random() < 0.3:  # 30%概率开始恋爱
        state["relationship"]["status"] = "dating"
        state["relationship"]["quality"] = random.randint(40, 70)
        state["relationship"]["years_together"] = 0
        return "你开始和某个特别的人约会。"
    return ""

# 婚姻系统
def propose():
    if state["relationship"]["status"] == "dating" and state["relationship"]["years_together"] >= 2 and random.random() < 0.5:  # 50%概率
        state["relationship"]["status"] = "married"
        state["relationship"]["quality"] += 10  # 婚姻质量提升
        return "你向TA求婚了，并且TA答应了。你们结婚了！"
    return "你还没有准备好求婚。"

# 生育选择
def decide_to_have_children():
    if state["relationship"]["status"] == "married" and random.random() < 0.25:  # 25%概率
        choice = random.choice(["want_kids", "no_kids", "not_now"])
        if choice == "want_kids":
            state["children"].append({"age": 0, "health": 70, "talent": "normal", "temperament": "normal", "bond": 50})
            state["money"] -= 30  # 生育开销
            return "你决定要孩子，生活将变得更加忙碌。"
        elif choice == "no_kids":
            state["relationship"]["no_kids_choice"] = True
            return "你决定不生孩子，这样生活会更简单。"
        elif choice == "not_now":
            return "你决定暂时不生孩子，可能以后再考虑。"
    return "你们还没有讨论过要不要孩子。"

# 模拟生成每一年的事件
def add_year():
    state["age"] += 1
    state["health"] -= random.randint(0, 2)
    state["money"] += random.randint(-5, 10)

    # 事件处理
    if state["age"] <= 6:
        line = f"{state['age']}岁这一年，{random.choice(year_lines['0-6'])}"
    elif 7 <= state["age"] <= 12:
        line = f"{state['age']}岁这一年，{random.choice(year_lines['7-12'])}"
    elif 13 <= state["age"] <= 18:
        line = f"{state['age']}岁这一年，{random.choice(year_lines['13-18'])}"
    elif 18 <= state["age"] <= 30:
        line = f"{state['age']}岁这一年，{random.choice(year_lines['18-30'])}"
        if state["age"] == 18:
            # 处理大学选择
            event = random.choice(random_events["18-30"])
            line += f" 事件：{event['event']}，选择：{', '.join(event['choices'])}"
            if "上大学" in event["choices"]:
                state["education"]["level"] = "college"
                if state["family"]["wealth_tier"] == "poor":
                    state["education"]["loan_status"] = True
                    state["money"] -= 50  # 假设贷款
            elif "打工" in event["choices"]:
                state["career"]["status"] = "worker"
                state["career"]["track"] = "worker"
            elif "创业" in event["choices"]:
                state["career"]["status"] = "entrepreneur"
                state["career"]["track"] = "startup"
                state["money"] -= 30  # 启动资金

        # 恋爱系统：18岁时开始触发恋爱事件
        line += start_dating()

        # 婚姻系统：结婚选择
        if state["relationship"]["status"] == "dating":
            line += propose()

        # 生育系统：生育选择
        line += decide_to_have_children()

    state["log"].append(line)

# 处理年度结算
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        add_year()
        return redirect(url_for("index"))
    return render_template("index.html", state=state)

# 重新开始游戏
@app.route("/restart", methods=["POST"])
def restart():
    global state
    state = reset_state()  # 重置游戏状态
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
