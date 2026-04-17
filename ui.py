import sqlite3
import tkinter as tk
from tkinter import ttk
from datetime import date

# =========================
# DB設定
# =========================
DB_PATH = "genba.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# =========================
# データ取得
# =========================
cur.execute("SELECT worker_id, name FROM workers")
workers = cur.fetchall()

cur.execute("SELECT site_id, site_name FROM sites")
sites = cur.fetchall()

# =========================
# UI
# =========================
root = tk.Tk()
root.title("現場勤怠アプリ")

root.geometry("400x250")

# -------------------------
# 名前
# -------------------------
tk.Label(root, text="名前").pack()
worker_var = tk.StringVar()
worker_box = ttk.Combobox(root, textvariable=worker_var)
worker_box["values"] = [f"{w[0]}:{w[1]}" for w in workers]
worker_box.pack()

# -------------------------
# 現場
# -------------------------
tk.Label(root, text="現場").pack()
site_var = tk.StringVar()
site_box = ttk.Combobox(root, textvariable=site_var)
site_box["values"] = [f"{s[0]}:{s[1]}" for s in sites]
site_box.pack()

# -------------------------
# 日付
# -------------------------
tk.Label(root, text="日付").pack()
date_entry = tk.Entry(root)
date_entry.insert(0, str(date.today()))
date_entry.pack()

# -------------------------
# type
# -------------------------
tk.Label(root, text="type（1=人工 / 2=残業 / 3=深夜）").pack()
type_var = tk.StringVar(value="1")
type_box = ttk.Combobox(root, textvariable=type_var)
type_box["values"] = ["1", "2", "3"]
type_box.pack()

# =========================
# 出勤登録
# =========================
def register():

    worker_id = int(worker_var.get().split(":")[0])
    site_id = int(site_var.get().split(":")[0])
    work_date = date_entry.get()
    type_ = int(type_var.get())

    cur.execute("""
        INSERT INTO attendance (worker_id, site_id, work_date, type, man_power)
        VALUES (?, ?, ?, ?, 1)
    """, (worker_id, site_id, work_date, type_))

    conn.commit()

    print("登録完了")

# =========================
# Excel出力（そのままexport.py相当）
# =========================
def export_excel():
    import subprocess
    subprocess.run(["python", "export.py"])
    print("Excel出力完了")

# =========================
# ボタン
# =========================
tk.Button(root, text="出勤登録", command=register).pack(pady=5)
tk.Button(root, text="Excel出力", command=export_excel).pack(pady=5)

# =========================
# 起動
# =========================
root.mainloop()

conn.close()