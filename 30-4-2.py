"""
智能学习系统 - 课时版本 (v3)
功能：
 - 多个学生管理（添加/删除/选择）
 - 多课程管理（包含先修课程）
 - 学习进度管理（按实际课时数+1）
 - 成绩记录（录入/修改成绩）
 - 学习排行榜（按已完成课程数或平均成绩排序）
 - 自动推荐下一门课程（基于未完成且先修满足）
 - 图形界面（Tkinter）
 - 数据库存储（SQLite）持久化：students, courses, progress

修复内容：
1. 修复 on_add_student 等方法因缩进错误导致的 AttributeError。
2. 进度管理从百分比改为课时数。
3. 优化学生列表和课程列表的显示。
"""

import sqlite3
import os
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# ---------------- 配置 ----------------
DB_FILE = "learning_system.db"
# 确保每次运行都从干净的状态开始（仅用于演示）
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

# ---------------- Database helpers ----------------
class DB:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        must_init = not os.path.exists(db_path)
        self.conn = sqlite3.connect(db_path)
        # 允许通过列名访问数据
        self.conn.row_factory = sqlite3.Row
        if must_init:
            self._init_db()

    def _init_db(self):
        cur = self.conn.cursor()
        cur.executescript('''
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_code TEXT UNIQUE
        );
        CREATE TABLE courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            total_lessons INTEGER DEFAULT 1,
            prereq TEXT DEFAULT '' -- comma-separated course ids
        );
        CREATE TABLE progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            progress INTEGER DEFAULT 0, -- 【已完成课时数】
            grade REAL,
            completed_date TEXT,
            UNIQUE(student_id, course_id)
        );
        ''' )
        self.conn.commit()
        self._seed_sample_data()

    def _seed_sample_data(self):
        cur = self.conn.cursor()
        # sample courses
        courses = [
            ("Python 入门", 10, ""), 
            ("Python 进阶", 12, "1"), 
            ("数据结构与算法", 15, "1"),
            ("人工智能基础", 14, "2,3"),
            ("数据库基础", 10, ""),
            ("Web 开发基础", 8, "1,5")
        ]
        cur.executemany("INSERT INTO courses (name, total_lessons, prereq) VALUES (?, ?, ?)", courses)

        # sample students
        students = [("张三", "S2025001"), ("李四", "S2025002"), ("王五", "S2025003")]
        cur.executemany("INSERT INTO students (name, student_code) VALUES (?, ?)", students)
        self.conn.commit()

    # Students
    def add_student(self, name, code):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO students (name, student_code) VALUES (?, ?)", (name, code))
        self.conn.commit()
        return cur.lastrowid

    def get_students(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM students ORDER BY id")
        return cur.fetchall()

    def get_student(self, student_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM students WHERE id=?", (student_id,))
        return cur.fetchone()

    # Courses
    def add_course(self, name, total_lessons=1, prereq=''):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO courses (name, total_lessons, prereq) VALUES (?, ?, ?)", (name, total_lessons, prereq))
        self.conn.commit()
        return cur.lastrowid

    def get_courses(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM courses ORDER BY id")
        return cur.fetchall()

    def get_course(self, course_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM courses WHERE id=?", (course_id,))
        return cur.fetchone()

    # Progress
    def ensure_progress(self, student_id, course_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM progress WHERE student_id=? AND course_id=?", (student_id, course_id))
        row = cur.fetchone()
        if not row:
            cur.execute("INSERT INTO progress (student_id, course_id, progress) VALUES (?, ?, 0)", (student_id, course_id))
            self.conn.commit()
            cur.execute("SELECT * FROM progress WHERE student_id=? AND course_id=?", (student_id, course_id))
            return cur.fetchone()
        return row

    def get_progress_for_student(self, student_id):
        cur = self.conn.cursor()
        # JOIN courses 表，获取 total_lessons 以计算进度
        cur.execute('''
            SELECT p.*, c.name as course_name, c.total_lessons 
            FROM progress p 
            JOIN courses c ON p.course_id=c.id 
            WHERE p.student_id=?
        ''', (student_id,))
        return cur.fetchall()

    def update_lessons_completed(self, student_id, course_id, new_lessons):
        # 更新的是已完成课时数 (progress)
        cur = self.conn.cursor()
        cur.execute("UPDATE progress SET progress=? WHERE student_id=? AND course_id=?", (new_lessons, student_id, course_id))
        self.conn.commit()

    def set_completed(self, student_id, course_id):
        # 设置 completed 状态时，将 progress 设为总课时数
        course = self.get_course(course_id)
        if not course: return

        cur = self.conn.cursor()
        completed_date = datetime.date.today().isoformat()
        total_lessons = course['total_lessons']
        
        cur.execute("UPDATE progress SET progress=?, completed_date=? WHERE student_id=? AND course_id=?", 
                    (total_lessons, completed_date, student_id, course_id))
        self.conn.commit()

    def set_grade(self, student_id, course_id, grade):
        cur = self.conn.cursor()
        cur.execute("UPDATE progress SET grade=? WHERE student_id=? AND course_id=?", (grade, student_id, course_id))
        self.conn.commit()

    def get_leaderboard(self, by='completed_count'):
        cur = self.conn.cursor()
        if by == 'completed_count':
            # 判断完成的逻辑：当 progress 等于 total_lessons 时视为完成
            cur.execute('''
            SELECT s.id, s.name, s.student_code, COUNT(p.id) as completed_count
            FROM students s
            LEFT JOIN progress p ON p.student_id=s.id 
            JOIN courses c ON p.course_id=c.id 
            WHERE p.progress = c.total_lessons
            GROUP BY s.id ORDER BY completed_count DESC, s.id
            ''')
            return cur.fetchall()
        else:
            # by average grade (unchanged)
            cur.execute('''
            SELECT s.id, s.name, s.student_code, AVG(p.grade) as avg_grade, COUNT(p.grade) as graded_count
            FROM students s
            LEFT JOIN progress p ON p.student_id=s.id AND p.grade IS NOT NULL
            GROUP BY s.id ORDER BY avg_grade DESC NULLS LAST
            ''')
            return cur.fetchall()

    def get_uncompleted_courses_for_student(self, student_id):
        cur = self.conn.cursor()
        # 需要获取总课时数 (total_lessons) 来判断是否完成
        cur.execute('''
        SELECT c.*, COALESCE(p.progress, 0) as progress
        FROM courses c
        LEFT JOIN progress p ON p.course_id=c.id AND p.student_id=?
        WHERE (p.progress IS NULL AND c.total_lessons > 0) OR (p.progress < c.total_lessons)
        ORDER BY c.id
        ''', (student_id,))
        return cur.fetchall()

    def get_completed_course_ids(self, student_id):
        cur = self.conn.cursor()
        # 判断完成逻辑
        cur.execute('''
        SELECT p.course_id 
        FROM progress p
        JOIN courses c ON p.course_id=c.id
        WHERE p.student_id=? AND p.progress=c.total_lessons
        ''', (student_id,))
        return [r['course_id'] for r in cur.fetchall()]

# ---------------- Business logic ----------------
class LearningSystem:
    def __init__(self, db: DB):
        self.db = db

    def study(self, student_id, course_id, amount=1): # 默认增加 1 课时
        self.db.ensure_progress(student_id, course_id)
        
        course = self.db.get_course(course_id)
        if not course: return 0
        total_lessons = course['total_lessons']

        cur = self.db.conn.cursor()
        cur.execute('SELECT progress FROM progress WHERE student_id=? AND course_id=?', (student_id, course_id))
        row = cur.fetchone()
        current = row['progress'] if row else 0
        
        # 新的进度是 current + amount，但不能超过 total_lessons
        newp = min(total_lessons, current + int(amount))
        
        self.db.update_lessons_completed(student_id, course_id, newp)
        
        # 达到总课时数时标记完成
        if newp == total_lessons:
            self.db.set_completed(student_id, course_id)
        return newp

    def is_course_completed(self, student_id, course_id):
        course = self.db.get_course(course_id)
        if not course: return False
        
        cur = self.db.conn.cursor()
        cur.execute('SELECT progress FROM progress WHERE student_id=? AND course_id=?', (student_id, course_id))
        row = cur.fetchone()
        # 已完成课时 >= 总课时
        return row and row['progress'] >= course['total_lessons']

    def complete_course_if_ready(self, student_id, course_id):
        if self.is_course_completed(student_id, course_id):
            self.db.set_completed(student_id, course_id)
            return True
        return False

    def recommend_next(self, student_id):
        uncompleted = self.db.get_uncompleted_courses_for_student(student_id)
        completed_ids = set(self.db.get_completed_course_ids(student_id))
        for c in uncompleted:
            prereq = c['prereq'].strip()
            if not prereq:
                return c
            # prereq is comma-separated course ids
            needed = [int(x) for x in prereq.split(',') if x.strip()]
            if set(needed).issubset(completed_ids):
                return c
        return None

    def assign_grade(self, student_id, course_id, grade):
        self.db.set_grade(student_id, course_id, float(grade))

# ---------------- GUI ----------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("智能学习系统（演示 - 课时版）")
        self.geometry("1000x600")
        self.db = DB()
        self.system = LearningSystem(self.db)
        self.selected_student_id = None
        self.selected_course_id = None
        self.create_widgets()
        self.refresh_all() # 确保在所有部件创建后刷新

    def create_widgets(self):
        # top frame for student actions
        top = ttk.Frame(self)
        top.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)

        add_student_btn = ttk.Button(top, text="添加学生", command=self.on_add_student)
        add_student_btn.pack(side=tk.LEFT, padx=4)

        add_course_btn = ttk.Button(top, text="添加课程", command=self.on_add_course)
        add_course_btn.pack(side=tk.LEFT, padx=4)

        refresh_btn = ttk.Button(top, text="刷新", command=self.refresh_all)
        refresh_btn.pack(side=tk.LEFT, padx=4)

        # main panes
        main = ttk.Frame(self)
        main.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        # students list
        left = ttk.Frame(main)
        left.pack(side=tk.LEFT, fill=tk.Y)
        ttk.Label(left, text="学生列表").pack()
        # 【修改 1】学生列表同时显示姓名和学号
        self.students_tree = ttk.Treeview(left, columns=("name", "code"), show='headings', height=20)
        self.students_tree.heading('name', text='姓名')
        self.students_tree.column('name', width=80)
        self.students_tree.heading('code', text='学号')
        self.students_tree.column('code', width=80)
        self.students_tree.pack(fill=tk.Y)
        self.students_tree.bind('<<TreeviewSelect>>', self.on_select_student)

        # courses list
        center = ttk.Frame(main)
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
        ttk.Label(center, text="课程列表").pack()
        # 【修改 2】课程列表显示名称（在 text 中），同时显示 ID, 总课时, 先修
        self.courses_tree = ttk.Treeview(center, columns=("id", "lessons", "prereq"), show='headings', height=10)
        self.courses_tree.heading('id', text='ID')
        self.courses_tree.column('id', width=30, anchor='center')
        self.courses_tree.heading('lessons', text='总课时')
        self.courses_tree.column('lessons', width=60, anchor='center')
        self.courses_tree.heading('prereq', text='先修(ID)')
        self.courses_tree.column('prereq', width=100)
        self.courses_tree['displaycolumns'] = ('id', 'lessons', 'prereq')
        self.courses_tree.pack(fill=tk.BOTH, expand=True)
        self.courses_tree.bind('<<TreeviewSelect>>', self.on_select_course)

        # right side actions & leaderboard
        right = ttk.Frame(main)
        right.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(right, text="操作").pack()
        self.status_label = ttk.Label(right, text="未选择学生")
        self.status_label.pack(pady=4)

        study_btn = ttk.Button(right, text="模拟学习 +1 课时", command=self.on_study)
        study_btn.pack(fill=tk.X, pady=2)

        complete_btn = ttk.Button(right, text="标记为已完成", command=self.on_complete)
        complete_btn.pack(fill=tk.X, pady=2)

        grade_btn = ttk.Button(right, text="录入/修改成绩", command=self.on_grade)
        grade_btn.pack(fill=tk.X, pady=2)

        recommend_btn = ttk.Button(right, text="推荐下一门课程", command=self.on_recommend)
        recommend_btn.pack(fill=tk.X, pady=2)

        ttk.Separator(right, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=6)
        ttk.Label(right, text="学习状态（选中学生）").pack()
        self.progress_list = tk.Listbox(right, width=40, height=12)
        self.progress_list.pack()

        ttk.Separator(right, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=6)
        ttk.Label(right, text="排行榜（按完成数）").pack()
        self.lb_tree = ttk.Treeview(right, columns=("completed",), show='headings', height=6)
        self.lb_tree.heading('completed', text='已完成课程数')
        self.lb_tree.pack()

    # ----- GUI handlers ----- 确保所有方法在此处，且缩进正确

    def on_add_student(self):
        name = simpledialog.askstring("添加学生", "姓名：", parent=self)
        if not name:
            return
        code = simpledialog.askstring("添加学生", "学号：", parent=self)
        if not code:
            return
        try:
            sid = self.db.add_student(name, code)
            messagebox.showinfo("成功", f"添加学生 {name} (id={sid})")
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def on_add_course(self):
        name = simpledialog.askstring("添加课程", "课程名：", parent=self)
        if not name:
            return
        lessons = simpledialog.askinteger("添加课程", "课时数：", parent=self, minvalue=1)
        prereq = simpledialog.askstring("添加课程", "先修课程 ID（用逗号分隔，如 1,2，留空无先修）：", parent=self)
        try:
            cid = self.db.add_course(name, lessons or 1, prereq or '')
            messagebox.showinfo("成功", f"添加课程 {name} (id={cid})")
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def refresh_all(self):
        self.refresh_students()
        self.refresh_courses()
        self.refresh_leaderboard()
        self.refresh_progress_display()

    def refresh_students(self):
        for r in self.students_tree.get_children():
            self.students_tree.delete(r)
        for s in self.db.get_students():
            # 【修改 1】将姓名和学号放入 values
            self.students_tree.insert('', 'end', iid=str(s['id']), values=(s['name'], s['student_code']), text="")

    def refresh_courses(self):
        for r in self.courses_tree.get_children():
            self.courses_tree.delete(r)
        for c in self.db.get_courses():
            # 【修改 2】将课程名称放入 text
            self.courses_tree.insert('', 'end', iid=str(c['id']), 
                                     values=(c['id'], c['total_lessons'], c['prereq']), 
                                     text=c['name'])

    def refresh_leaderboard(self):
        for r in self.lb_tree.get_children():
            self.lb_tree.delete(r)
        rows = self.db.get_leaderboard('completed_count')
        for r in rows:
            self.lb_tree.insert('', 'end', iid=str(r['id']), values=(r['completed_count'],), text=r['name'])

    def on_select_student(self, event=None):
        sel = self.students_tree.selection()
        if not sel:
            self.selected_student_id = None
            self.status_label.config(text="未选择学生")
        else:
            sid = int(sel[0])
            self.selected_student_id = sid
            s = self.db.get_student(sid)
            self.status_label.config(text=f"选中：{s['name']} ({s['student_code']})")
        self.refresh_progress_display()

    def on_select_course(self, event=None):
        sel = self.courses_tree.selection()
        if not sel:
            self.selected_course_id = None
        else:
            self.selected_course_id = int(sel[0])
        self.refresh_progress_display()

    def refresh_progress_display(self):
        self.progress_list.delete(0, tk.END)
        if not self.selected_student_id:
            return
        
        # 确保所有课程都有进度记录
        all_courses = self.db.get_courses()
        for c in all_courses:
            self.db.ensure_progress(self.selected_student_id, c['id'])
            
        progs = self.db.get_progress_for_student(self.selected_student_id)
        
        for p in progs:
            course_name = p['course_name']
            completed_lessons = p['progress']
            total_lessons = p['total_lessons']
            
            # 【修改 4】显示格式改为 (完成课时数/总课时数)
            progress_ratio = f"{completed_lessons}/{total_lessons}"
            
            # 计算百分比
            percent = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
            
            line = f"[{p['course_id']}] {course_name} - 进度: {progress_ratio} ({percent:.0f}%)"
            
            if p['grade'] is not None:
                line += f" | 成绩: {p['grade']}"
            if p['completed_date']:
                line += f" | 完成: {p['completed_date']}"
            self.progress_list.insert(tk.END, line)

    def on_study(self):
        if not self.selected_student_id or not self.selected_course_id:
            messagebox.showwarning("操作失败", "请先选中学生和课程")
            return
        # 调用 study 方法，增加 1 课时
        new_lessons = self.system.study(self.selected_student_id, self.selected_course_id, amount=1)
        
        course = self.db.get_course(self.selected_course_id)
        if course:
            total = course['total_lessons']
            messagebox.showinfo("学习完成", f"已完成课时数更新为：{new_lessons}/{total}")
        
        self.refresh_progress_display()
        self.refresh_leaderboard()

    def on_complete(self):
        if not self.selected_student_id or not self.selected_course_id:
            messagebox.showwarning("操作失败", "请先选中学生和课程")
            return
            
        course = self.db.get_course(self.selected_course_id)
        if not course: return
        total_lessons = course['total_lessons']
        
        is_ready = self.system.is_course_completed(self.selected_student_id, self.selected_course_id)
        
        if is_ready:
            self.db.set_completed(self.selected_student_id, self.selected_course_id)
            messagebox.showinfo("已完成", "课程已标记为完成")
        else:
            # 强制完成逻辑
            proceed = messagebox.askyesno("强制完成", f"当前进度未到 {total_lessons} 课时，是否强制标记为完成？（会将进度设为 {total_lessons} 课时）")
            if proceed:
                # 强制将进度设为总课时数
                self.db.update_lessons_completed(self.selected_student_id, self.selected_course_id, total_lessons)
                self.db.set_completed(self.selected_student_id, self.selected_course_id)
                messagebox.showinfo("已完成", "课程已强制标记为完成")
                
        self.refresh_progress_display()
        self.refresh_leaderboard()

    def on_grade(self):
        if not self.selected_student_id or not self.selected_course_id:
            messagebox.showwarning("操作失败", "请先选中学生和课程")
            return
        val = simpledialog.askfloat("录入成绩", "输入成绩（0-100）：", parent=self, minvalue=0, maxvalue=100)
        if val is None:
            return
        self.system.assign_grade(self.selected_student_id, self.selected_course_id, val)
        messagebox.showinfo("成功", "成绩已保存")
        self.refresh_progress_display()
        self.refresh_leaderboard()

    def on_recommend(self):
        if not self.selected_student_id:
            messagebox.showwarning("操作失败", "请先选中学生")
            return
        rec = self.system.recommend_next(self.selected_student_id)
        if rec:
            messagebox.showinfo("推荐课程", f"推荐：[{rec['id']}] {rec['name']} (课时: {rec['total_lessons']})")
        else:
            messagebox.showinfo("推荐课程", "暂无可推荐课程（可能全部已完成或先修未满足）")

# ----------------- Run -----------------
if __name__ == '__main__':
    # 注意：每次运行时都会删除并重建数据库文件 'learning_system.db'，以便使用新的逻辑。
    app = App()
    app.mainloop()