from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# --------- 游戏状态（每次刷新就是新人生）---------
state = {
    "age": 0,
    "money": 50,
    "health": 100,
    "log": []
}

year_lines = [
    "这一年过得很普通。",
    "你开始意识到时间在走。",
    "你有点累，但还是往前。",
    "这一年没有发生大事。",
    "你开始想得更多了。"
]

def add_year():
    state["age"] += 1
    state["health"] -= random.randint(0, 2)
    state["money"] += random.randint(-5, 10)
    line = f"{state['age']}岁这一年，{random.choice(year_lines)}"
    state["log"].append(line)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        add_year()
        return redirect(url_for("index"))
    return render_template("index.html", state=state)

if __name__ == "__main__":
    app.run(debug=True)
