import tkinter as tk

def main_window(identity):
    """根据用户身份显示不同内容"""
    window = tk.Tk()
    window.title(f"{identity} 主界面")

    if identity == "admin":
        # 显示管理员界面的操作
        tk.Label(window, text="管理员界面").pack()
        tk.Button(window, text="管理演习数据").pack()
        # 其他管理员功能
    else:
        # 显示军事迷界面的操作
        tk.Label(window, text="军事迷界面").pack()
        tk.Button(window, text="查看演习数据").pack()
        # 其他军事迷功能

    window.mainloop()
