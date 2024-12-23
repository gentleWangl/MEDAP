import tkinter as tk
from tkinter import ttk, messagebox
from db.utils import fetch_all, delete_record, update_record, insert_record  # 引入现有的函数
from PIL import Image, ImageTk




def show_table(window, table_name):
    """显示选定表的数据"""
    # 获取数据
    try:
        query = f"SELECT * FROM {table_name}"
        rows = fetch_all(query)  # 使用 fetch_all 函数
        if not rows:
            messagebox.showwarning("警告", "没有数据")
            return

        # 获取列名
        columns = [desc[0] for desc in fetch_all(f"DESCRIBE {table_name}")]
        
        # 清除现有的显示
        for widget in window.winfo_children():
            widget.destroy()

        # 创建表格
        treeview = ttk.Treeview(window, columns=columns, show="headings")
        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=150, anchor="center")

        for row in rows:
            treeview.insert("", "end", values=row)

        treeview.pack(fill=tk.BOTH, expand=True)

        # 操作按钮框架
        action_frame = tk.Frame(window)
        action_frame.pack(fill=tk.X, pady=10)

        # 删除按钮
        delete_button = tk.Button(action_frame, text="删除选中数据", command=lambda: delete_data(table_name, treeview))
        delete_button.pack(side=tk.LEFT, padx=10)

        # 修改按钮
        update_button = tk.Button(action_frame, text="修改选中记录", command=lambda: update_data(table_name, treeview))
        update_button.pack(side=tk.LEFT, padx=10)

        # 添加按钮
        add_button = tk.Button(action_frame, text="添加记录", command=lambda: add_data(table_name))
        add_button.pack(side=tk.LEFT, padx=10)

        # 返回按钮
        # bg_image = Image.open("./icons/bk_admin01.jpg")
        # bg_image = bg_image.resize((800, 600)) 
        # bg_photo = ImageTk.PhotoImage(bg_image)
        # bg_label = tk.Label(window, image=bg_photo)
        # # bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        # bg_label.image = bg_photo  # 防止图片被垃圾回收
        # bg_label.is_bg_label = True  # 标记为背景图片标签
        back_button = tk.Button(window, text="返回", command=lambda: show_table_select_of_admin(window))
        back_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("错误", f"加载数据时发生错误: {e}")

def delete_data(table_name, treeview):
    """删除选中的数据"""
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("警告", "请先选择要删除的记录")
        return

    try:
        for item in selected_item:
            values = treeview.item(item, "values")
            primary_key = values[0]  # 假设ID是主键
            delete_record(table_name, primary_key)  # 使用 utils 中的 delete_record
        messagebox.showinfo("成功", "数据已删除")
        show_table(treeview.master, table_name)  # 刷新数据
    except Exception as e:
        messagebox.showerror("错误", f"删除数据时发生错误: {e}")

def update_data(table_name, treeview):
    """修改选中的数据"""
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("警告", "请先选择要修改的记录")
        return

    # 弹出修改窗口，填写修改内容
    current_values = treeview.item(selected_item[0], "values")
    update_window = tk.Toplevel()
    update_window.title("修改记录")

    entries = {}
    columns = [col for col in treeview["columns"]]
    for i, col in enumerate(columns):
        label = tk.Label(update_window, text=col)
        label.grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(update_window)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.insert(0, current_values[i])  # 填充当前值
        entries[col] = entry

    def submit_update():
        updated_values = {col: entry.get() for col, entry in entries.items()}
        set_clause = ", ".join([f"{col} = %s" for col in updated_values])
        primary_key = current_values[0]  # 假设ID是主键
        try:
            update_record(table_name, primary_key, updated_values)  # 使用 update_record 更新数据
            messagebox.showinfo("成功", "数据已更新")
            show_table(update_window.master, table_name)  # 刷新数据
            update_window.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"更新数据时发生错误: {e}")

    submit_button = tk.Button(update_window, text="提交", command=submit_update)
    submit_button.grid(row=len(entries), columnspan=2, pady=10)

def add_data(table_name):
    """添加新记录"""
    add_window = tk.Toplevel()
    add_window.title("添加记录")

    entries = {}
    try:
        # 获取表结构
        columns = fetch_all(f"DESCRIBE {table_name}")
        entries = {col[0]: tk.Entry(add_window) for col in columns if col[0] != "id"}  # 排除自动生成的主键

        for i, (col_name, entry) in enumerate(entries.items()):
            label = tk.Label(add_window, text=col_name)
            label.grid(row=i, column=0, padx=10, pady=5)
            entry.grid(row=i, column=1, padx=10, pady=5)

        def submit_add():
            values = [entry.get() for entry in entries.values()]
            try:
                insert_record(table_name, values)  # 使用 insert_record 插入数据
                messagebox.showinfo("成功", "数据已添加")
                show_table(add_window.master, table_name)  # 刷新数据
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"插入数据时发生错误: {e}")

        submit_button = tk.Button(add_window, text="提交", command=submit_add)
        submit_button.grid(row=len(entries), columnspan=2, pady=10)

    except Exception as e:
        messagebox.showerror("错误", f"加载表结构时发生错误: {e}")

import tkinter as tk
from PIL import Image, ImageTk

def show_table_select_of_admin(window):
    """显示表选择界面"""
        # 设置背景图片
    bg_image = Image.open("./icons/bk_admin01.jpg")
    bg_image = bg_image.resize((1600, 800)) 
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo  # 防止图片被垃圾回收
    bg_label.is_bg_label = True  # 标记为背景图片标签
    # 清空现有内容，但保留背景图片
    for widget in window.winfo_children():
        if not hasattr(widget, 'is_bg_label') or not widget.is_bg_label:
            widget.destroy()

     # 创建大标题
    title_label = tk.Label(window, text="强国有我,请党放心！", font=("Arial", 50), bg='blue', fg='red')
    title_label.pack(pady=(50, 20))
    title_label2 = tk.Label(window, text="欢迎您，管理员同志！", font=("Arial", 30), bg='blue', fg='red')
    title_label2.pack(pady=(50, 20))
    # 创建父控件并设置背景透明
    frame = tk.Frame(window, bg='white')  # 使用白色背景
    frame.pack(side=tk.BOTTOM, fill=tk.X)  # 将父控件放置在底部

    # 创建表按钮
    tables = ["Exercise", "Equipment", "Scale", "Media", "Reaction"]  # 表名列表
    tables_CN = ["军事演习", "武器装备", "演习规模", "媒体", "反应信息"]
    colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1']  # 按钮颜色列表

    for i, (table, table_cn, color) in enumerate(zip(tables, tables_CN, colors)):
        button = tk.Button(frame, text=table_cn, command=lambda t=table: show_table(window, t),
                           bg=color, fg='white', height=5, width=10,font=("Arial", 20))
        button.grid(row=0, column=i, padx=20, pady=10, sticky='nsew')

    # 设置网格列权重，使按钮均匀分布
    for i in range(len(tables)):
        frame.grid_columnconfigure(i, weight=1)

def main_window(identity):
    """根据用户身份显示不同内容"""
    window = tk.Tk()
    window.title(f"{identity} 主界面")
    window.geometry("1600x800")

    if identity == "admin":
        # 显示管理员界面
        show_table_select_of_admin(window)

    else:
        # 显示军事迷界面
        title_label = tk.Label(window, text="强国有我,请党放心！", font=("Arial", 50), bg='blue', fg='red')
        title_label.pack(pady=(50, 20))
        
        tk.Label(window, text="军事迷界面").pack(pady=20)
        tk.Button(window, text="查看演习数据").pack()

    window.mainloop()

# 示例调用
if __name__ == "__main__":
    main_window("admin")  # 或者 main_window("military_enthusiast")