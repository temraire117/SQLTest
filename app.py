from flask import Flask, request, render_template, g
import sqlite3
import os

app = Flask(__name__)
app.config.from_mapping(
    DATABASE=os.path.join(app.root_path, "students.db")
)

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template("index.html", result="")

@app.route("/score", methods=["POST"])
def score():
    student_id = request.form.get("student_id", "").strip()
    if not (1 <= len(student_id) <= 20):
        return render_template("index.html", result="잘못된 학번입니다.")
    db = get_db()

    #안전하게 바꾼 코드
    cur = db.execute("SELECT name, score FROM students WHERE id = ?", (student_id,))
    row = cur.fetchone()
    
    if row:
        return render_template("index.html", result=f"이름: {row['name']} / 점수: {row['score']}")
    else:
        return render_template("index.html", result="학생을 찾을 수 없습니다.")
        
if __name__ == "__main__":
    app.run(debug=True)
