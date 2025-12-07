# ========= Course 课程类 =========
class Course:
    def __init__(self, name, total_lessons):
        self.name = name
        self.total_lessons = total_lessons

    def show_info(self):
        print(f"课程名称：{self.name} | 总课时：{self.total_lessons}")


# ========= Student 学生类 =========
class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.progress = 0          # 学习进度（0-100）
        self.completed_courses = []  # 已完成课程列表

    # 学习（进度增加）
    def study(self, amount=10):
        if self.progress < 100:
            self.progress += amount
            if self.progress > 100:
                self.progress = 100
            print(f"{self.name} 学习中... 当前进度：{self.progress}%")
        else:
            print("课程已学完，无需继续学习。")

    # 完成课程
    def complete_course(self, course_name):
        if self.progress == 100:
            self.completed_courses.append(course_name)
            print(f"✅ {self.name} 已完成课程：{course_name}")
            self.progress = 0  # 重置进度，准备学下一门
        else:
            print("⚠️ 进度未到 100%，无法完成课程！")

    # 查看学生状态
    def get_status(self):
        print("\n📊 学生当前状态")
        print("-------------------------")
        print(f"姓名：{self.name}")
        print(f"学号：{self.student_id}")
        print(f"当前进度：{self.progress}%")
        print(f"已完成课程：{self.completed_courses}")
        print("-------------------------\n")


# ========= 系统运行演示 =========
def main():
    print("🎓 智能学习系统启动中...\n")

    # 创建课程
    python_course = Course("Python 入门", 20)
    ai_course = Course("人工智能基础", 15)

    python_course.show_info()
    ai_course.show_info()

    print("\n-------------------------\n")

    # 创建学生
    student = Student("张三", "2025001")

    # 查看初始状态
    student.get_status()

    # 模拟学习过程
    student.study()
    student.study()
    student.study()
    student.study()
    student.study()

    # 尝试完成课程（未满 100%）
    student.complete_course("Python 入门")

    # 继续学习到 100%
    student.study()
    student.study()
    student.study()
    student.study()
    student.study()

    # 正式完成课程
    student.complete_course("Python 入门")

    # 查看最终状态
    student.get_status()

    print("🎉 学习系统演示结束！")


# 程序入口
if __name__ == "__main__":
    main()
