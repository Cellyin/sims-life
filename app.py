import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 角色状态
state = {
    "age": 0,
    "money": 50,
    "health": 100,
    "family": {
        "wealth_tier": "normal",  # 家庭经济状况：poor, normal, rich, affluent
        "siblings": 0,  # 兄弟姐妹
        "relationship_quality": "harmonious"  # 父母关系：harmonious, frequent, occasional
    },
    "log": [],
    "personality": {
        "self_worth": 50,  # 自我认同
        "social_comparison": 50,  # 对比其他人
        "intimacy_desire": 50,  # 渴望亲密关系
    }
}

# 年度旁白库
year_lines = {
    "0-6": [
        "这一年，你在家里开始学走路，偶尔会摔跤，但总能站起来。",
        "这一年，你学会了说话，有时候会讲出一些有趣的句子，大家都很喜欢听。",
        "这一年，家里发生了一些事，你渐渐开始懂事。",
        "这一年，你常常会在父母面前感到自己不被关注。",
        "这一年，兄弟姐妹开始有了自己的想法，你开始争夺资源。",
        "这一年，你已经能分辨出爸爸和妈妈不同的情绪变化了。",
        "这一年，家里有一些争吵，你不太明白，但你知道事情有点不一样。"
    ],
    "7-12": [
        "这一年，你开始适应学校的生活，作业增多了，也学会了如何交朋友。",
        "这一年，父母开始让你独立做决定，你偶尔感到有压力。",
        "这一年，你在班级里找到了一个固定的朋友，也开始有了新的兴趣爱好。",
        "这一年，你发现自己越来越在意其他同学的看法，偶尔会为了融入去做一些事。",
        "这一年，你的父母在家里吵了几次，但你没有完全明白发生了什么。",
        "这一年，你第一次参与到家庭事务中，父母让你帮忙做决定，你感到自己越来越独立。",
        "这一年，你和朋友因为一个玩具争吵了，但你们很快就和好了。"
    ],
    "13-18": [
        "这一年，你开始关注自己的外貌和形象。",
        "这一年，和同学之间有了更多的冲突，也有了很多的友谊。",
        "这一年，你第一次发现自己对某个人有了特别的感觉。",
        "这一年，你开始怀疑自己是不是不够好，有时觉得自己总是比别人差。",
        "这一年，你的父母不断催促你学好成绩，压力变得越来越大。",
        "这一年，你和朋友关系越来越复杂，有时候会为了小事吵架，但也会为了彼此支持。",
        "这一年，你第一次发现自己对某个同学产生了好感，但又害怕被拒绝。",
    ]
}

# 模拟生成每一年的事件
def add_year():
    state["age"] += 1
    state["health"] -= random.randint(0, 2)
    state["money"] += random.randint(-5, 10)

    # 按照年龄段和家庭背景选择旁白
    if state["age"] <= 6:
        line = f"{state['age']}岁这一年，{random.choice(year_lines['0-6'])}"
    elif 7 <= state["age"] <= 12:
        line = f"{state['age']}岁这一年，{random.choice(year_lines['7-12'])}"
    elif 13 <= state["age"] <= 18:
        line = f"{state['age']}岁这一年，{random.choice(year_lines['13-18'])}"
        # 处理青春期的选择和影响
        # 模拟个人成长：自我认同、社交对比、亲密欲望
        state["personality"]["self_worth"] += random.randint(-5, 5)
        state["personality"]["social_comparison"] += random.randint(-5, 5)
        state["personality"]["intimacy_desire"] += random.randint(-3, 3)
    state["log"].append(line)

# 首页路由
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        add_year()  # 每次点击按钮，就加一年
        return redirect(url_for("index"))
    return render_template("index.html", state=state)

if __name__ == "__main__":
    app.run(debug=True)
