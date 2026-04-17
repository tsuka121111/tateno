from flask import Flask, request, redirect, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB = "genba.db"

# ------------------------
# 初期化（クラウド用安全）
# ------------------------
def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS workers (
        worker_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sites (
        site_id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_name TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        worker_id INTEGER,
        site_id INTEGER,
        work_date TEXT,
        type INTEGER,
        man_power REAL
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ------------------------
# ホーム
# ------------------------
@app.route("/")
def index():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    workers = cur.execute("SELECT worker_id, name FROM workers").fetchall()
    sites = cur.execute("SELECT site_id, site_name FROM sites").fetchall()

    html = """
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <h2>現場勤怠クラウド</h2>

    <form method="POST" action="/add">

    名前<br>
    <select name="worker_id">
    """

    for w in workers:
        html += f"<option value='{w[0]}'>{w[1]}</option>"

    html += """
    </select><br><br>

    現場<br>
    <select name="site_id">
    """

    for s in sites:
        html += f"<option value='{s[0]}'>{s[1]}</option>"

    html += """
    </select><br><br>

    日付<br>
    <input name="work_date"><br><br>

    type<br>
    <select name="type">
        <option value="1">人工</option>
        <option value="2">残業</option>
        <option value="3">深夜</option>
    </select><br><br>

    <button style="font-size:20px;">登録</button>
    </form>

    <br>
    <a href="/list">履歴</a>
    """

    return html

# ------------------------
# 登録
# ------------------------
@app.route("/add", methods=["POST"])
def add():
    worker_id = request.form["worker_id"]
    site_id = request.form["site_id"]
    work_date = request.form["work_date"]
    type_ = request.form["type"]

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO attendance (worker_id, site_id, work_date, type, man_power)
    VALUES (?, ?, ?, ?, 1)
    """, (worker_id, site_id, work_date, type_))

    conn.commit()
    conn.close()

    return redirect("/")

# ------------------------
# 履歴
# ------------------------
@app.route("/list")
def list_data():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    rows = cur.execute("""
    SELECT a.id, w.name, s.site_name, a.work_date, a.type
    FROM attendance a
    JOIN workers w ON a.worker_id = w.worker_id
    JOIN sites s ON a.site_id = s.site_id
    ORDER BY a.id DESC
    """).fetchall()

    html = "<h2>履歴</h2>"

    for r in rows:
        html += f"<p>{r[1]} / {r[2]} / {r[3]} / type:{r[4]}</p>"

    return html

# ------------------------
# 起動
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)