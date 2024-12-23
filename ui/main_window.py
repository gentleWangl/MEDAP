import tkinter as tk
from tkinter import ttk, messagebox
from db.utils import fetch_all, delete_record, update_record, insert_record ,fetch_one # 引入现有的函数
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
        delete_button = tk.Button(action_frame, text="删除选中记录", command=lambda: delete_data(table_name, treeview))
        delete_button.pack(side=tk.LEFT, padx=10)

        # 修改按钮
        update_button = tk.Button(action_frame, text="修改选中记录", command=lambda: update_data(table_name, treeview))
        update_button.pack(side=tk.LEFT, padx=10)

        # 添加按钮
        add_button = tk.Button(action_frame, text="添加记录", command=lambda: add_data(table_name))
        add_button.pack(side=tk.LEFT, padx=10)
        # 返回按钮
        back_button = tk.Button(window, text="返回", command=lambda: show_table_select_of_admin(window))
        back_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("错误", f"加载数据时发生错误: {e}")


def user_show_table(window, table_name):
    """显示普通用户的统计信息界面"""
    try:
        # 获取数据
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

        # 替换原有按钮为统计信息按钮
        if table_name == "Exercise":
            # 演习表统计信息按钮
            exercise_stats_button = tk.Button(action_frame, text="演习总数统计", command=lambda: show_exercise_stats(window))
            exercise_stats_button.pack(side=tk.LEFT, padx=10)

            country_stats_button = tk.Button(action_frame, text="按国家统计演习", command=lambda: show_country_exercise_stats(window))
            country_stats_button.pack(side=tk.LEFT, padx=10)

        elif table_name == "Equipment":
            # 装备表统计信息按钮
            equipment_stats_button = tk.Button(action_frame, text="装备总数统计", command=lambda: show_equipment_stats(window))
            equipment_stats_button.pack(side=tk.LEFT, padx=10)

            equipment_type_stats_button = tk.Button(action_frame, text="按装备类型统计", command=lambda: show_equipment_type_stats(window))
            equipment_type_stats_button.pack(side=tk.LEFT, padx=10)

        elif table_name == "Scale":
            # 规模表统计信息按钮
            scale_stats_button = tk.Button(action_frame, text="按演习统计规模", command=lambda: show_scale_stats(window))
            scale_stats_button.pack(side=tk.LEFT, padx=10)

        elif table_name == "Media":
            # 媒体表统计信息按钮
            media_stats_button = tk.Button(action_frame, text="媒体总数统计", command=lambda: show_media_stats(window))
            media_stats_button.pack(side=tk.LEFT, padx=10)

            media_per_exercise_button = tk.Button(action_frame, text="按演习统计媒体", command=lambda: show_media_per_exercise_stats(window))
            media_per_exercise_button.pack(side=tk.LEFT, padx=10)

        elif table_name == "Reaction":
            # 反应表统计信息按钮
            reaction_stats_button = tk.Button(action_frame, text="反应总数统计", command=lambda: show_reaction_stats(window))
            reaction_stats_button.pack(side=tk.LEFT, padx=10)

            reactions_per_exercise_button = tk.Button(action_frame, text="按演习统计反应", command=lambda: show_reactions_per_exercise_stats(window))
            reactions_per_exercise_button.pack(side=tk.LEFT, padx=10)

        # 返回按钮
        back_button = tk.Button(window, text="返回", command=lambda: show_table_select_of_user(window))
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
    def go_back_to_login():
        window.destroy()  # 关闭注册窗口
        import ui.login  # 导入登录界面
        ui.login.login_window()  # 显示登录界面
    return_button = tk.Button(window, text="返回登录界面", command=lambda: go_back_to_login(),
                              bg='#4CAF50', fg='white', font=("Arial", 14))
    return_button.place(relx=1.0, rely=0.0, anchor=tk.NE, x=-10, y=10)
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

def show_table_select_of_user(window):
    """显示表选择界面"""
    # 设置背景图片
    bg_image = Image.open("./icons/bk_user01.jpg")
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
    def go_back_to_login():
        window.destroy()  # 关闭注册窗口
        import ui.login  # 导入登录界面
        ui.login.login_window()  # 显示登录界面
    return_button = tk.Button(window, text="返回登录界面", command=lambda: go_back_to_login(),
                              bg='#4CAF50', fg='white', font=("Arial", 14))
    return_button.place(relx=1.0, rely=0.0, anchor=tk.NE, x=-10, y=10)
     # 创建大标题
    title_label = tk.Label(window, text="听党指挥,能打胜仗！", font=("Arial", 50), bg='blue', fg='red')
    title_label.pack(pady=(50, 20))
    title_label2 = tk.Label(window, text="欢迎您，军事迷同志！", font=("Arial", 30), bg='blue', fg='red')
    title_label2.pack(pady=(50, 20))
    # 创建父控件并设置背景透明
    frame = tk.Frame(window, bg='white')  # 使用白色背景
    frame.pack(side=tk.BOTTOM, fill=tk.X)  # 将父控件放置在底部

    # 创建表按钮
    tables = ["Exercise", "Equipment", "Scale", "Media", "Reaction"]  # 表名列表
    tables_CN = ["军事演习", "武器装备", "演习规模", "媒体", "反应信息"]
    colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1']  # 按钮颜色列表

    for i, (table, table_cn, color) in enumerate(zip(tables, tables_CN, colors)):
        button = tk.Button(frame, text=table_cn, command=lambda t=table: user_show_table(window, t),
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
        show_table_select_of_user(window)

    window.mainloop()



# 统计相关函数

def show_country_exercise_stats(window):
    """展示按国家统计的演习数量"""
    try:
        # 清除现有的显示
        for widget in window.winfo_children():
            widget.destroy()

        # 设置背景图片
        bg_image = Image.open("./icons/bk_admin01.jpg")
        bg_image = bg_image.resize((1600, 800))  # 确保图片大小与窗口一致
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(window, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_photo  # 防止图片被垃圾回收
        bg_label.is_bg_label = True  # 标记为背景图片标签

        # 创建大标题
        title_label = tk.Label(window, text="按国家统计的演习数量", font=("Arial", 30), bg='blue', fg='red')
        title_label.pack(pady=(50, 20))

        # 统计信息区域
        stats_frame = tk.Frame(window, bg='white')
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 按国家统计演习数量
        country_exercises_value = fetch_all("SELECT Country, COUNT(*) FROM Exercise GROUP BY Country")

        # 计算演习总数量
        total_count_query = "SELECT COUNT(*) FROM Exercise"
        total_count_result = fetch_one(total_count_query)
        total_count = total_count_result[0] if total_count_result else 0

        # 使用 Treeview 展示统计信息
        treeview = ttk.Treeview(stats_frame, columns=("Country", "Count"), show="headings")
        treeview.heading("Country", text="国家")
        treeview.heading("Count", text="演习数量")
        treeview.column("Country", width=200, anchor="center")
        treeview.column("Count", width=100, anchor="center")

        for row in country_exercises_value:
            treeview.insert("", "end", values=row)

        # 插入总计行
        treeview.insert("", "end", values=("总计", total_count), tags=('total',))

        # 设置总计行的样式
        style = ttk.Style()
        style.configure('Total.TLabel', background='lightgray', foreground='black', font=("Arial", 14, 'bold'))
        treeview.tag_configure('total', background='lightgray', foreground='black', font=("Arial", 14, 'bold'))

        treeview.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 返回按钮
        back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Exercise"),
                                bg='#4CAF50', fg='white', font=("Arial", 14))
        back_button.pack(side=tk.BOTTOM, pady=10)

    except Exception as e:
        messagebox.showerror("错误", f"加载数据时发生错误: {e}")

def show_exercise_stats(window):
    """展示演习总数统计"""
    try:
        # 清除现有的显示
        for widget in window.winfo_children():
            widget.destroy()

        # 设置背景图片
        bg_image = Image.open("./icons/bk_admin01.jpg")
        bg_image = bg_image.resize((1600, 800))  # 确保图片大小与窗口一致
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(window, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_photo  # 防止图片被垃圾回收
        bg_label.is_bg_label = True  # 标记为背景图片标签

        # 创建大标题
        title_label = tk.Label(window, text="演习统计信息", font=("Arial", 30), bg='blue', fg='red')
        title_label.pack(pady=(50, 20))

        # 统计信息区域
        stats_frame = tk.Frame(window, bg='white')
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 演习总数
        total_exercises_query = "SELECT COUNT(*) FROM Exercise"
        total_exercises_result = fetch_one(total_exercises_query)
        total_exercises = total_exercises_result[0] if total_exercises_result else 0

        # 演习次数最多的国家
        most_exercises_country_query = """
        SELECT Country, COUNT(*) AS Count
        FROM Exercise
        GROUP BY Country
        ORDER BY Count DESC
        LIMIT 1
        """
        most_exercises_country_result = fetch_one(most_exercises_country_query)
        most_exercises_country = most_exercises_country_result[0] if most_exercises_country_result else "无数据"
        most_exercises_count = most_exercises_country_result[1] if most_exercises_country_result else 0

        # 演习国家总数
        unique_countries_query = "SELECT COUNT(DISTINCT Country) FROM Exercise"
        unique_countries_result = fetch_one(unique_countries_query)
        unique_countries = unique_countries_result[0] if unique_countries_result else 0

        # 使用 Treeview 展示统计信息
        treeview = ttk.Treeview(stats_frame, columns=("Statistic", "Value"), show="headings")
        treeview.heading("Statistic", text="统计信息")
        treeview.heading("Value", text="值")
        treeview.column("Statistic", width=250, anchor="center")
        treeview.column("Value", width=150, anchor="center")

        treeview.insert("", "end", values=("总演习数", total_exercises))
        treeview.insert("", "end", values=("演习次数最多的国家", f"{most_exercises_country} ({most_exercises_count})"))
        treeview.insert("", "end", values=("演习国家总数", unique_countries))

        treeview.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 返回按钮
        back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Exercise"),
                                bg='#4CAF50', fg='white', font=("Arial", 14))
        back_button.pack(side=tk.BOTTOM, pady=10)

    except Exception as e:
        messagebox.showerror("错误", f"加载数据时发生错误: {e}")

def show_equipment_stats(window):
    """展示装备总数统计"""
    try:
        # 清除现有的显示
        for widget in window.winfo_children():
            widget.destroy()

        # 设置背景图片
        bg_image = Image.open("./icons/bk_admin01.jpg")
        bg_image = bg_image.resize((1600, 800))  # 确保图片大小与窗口一致
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(window, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_photo  # 防止图片被垃圾回收
        bg_label.is_bg_label = True  # 标记为背景图片标签

        # 创建大标题
        title_label = tk.Label(window, text="装备统计信息", font=("Arial", 30), bg='blue', fg='red')
        title_label.pack(pady=(50, 20))

        # 统计信息区域
        stats_frame = tk.Frame(window, bg='white')
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 装备总数
        total_equipment_query = "SELECT COUNT(*) FROM Equipment"
        total_equipment_value = fetch_one(total_equipment_query)
        total_equipment_label_value = tk.Label(stats_frame, text=f"总装备数：{total_equipment_value[0]}", font=("Arial", 14))
        total_equipment_label_value.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # 部署最多的装备
        most_deployed_equipment_query = """
        SELECT EquipmentName, SUM(DeploymentQty) FROM Equipment 
        JOIN Exercise_Equipment ON Equipment.EquipmentID = Exercise_Equipment.EquipmentID
        GROUP BY EquipmentName
        ORDER BY SUM(DeploymentQty) DESC LIMIT 1
        """
        most_deployed_equipment_value = fetch_one(most_deployed_equipment_query)
        most_deployed_equipment_label_value = tk.Label(stats_frame, text=f"部署最多的装备：{most_deployed_equipment_value[0]} ({most_deployed_equipment_value[1]} 部署)", font=("Arial", 14))
        most_deployed_equipment_label_value.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # 部署总数
        total_deployment_query = "SELECT SUM(DeploymentQty) FROM Equipment"
        total_deployment_value = fetch_one(total_deployment_query)
        total_deployment_label_value = tk.Label(stats_frame, text=f"部署总数：{total_deployment_value[0]}", font=("Arial", 14))
        total_deployment_label_value.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # 持续最长的装备
        longest_equipment_query = """
        SELECT EquipmentName FROM Equipment 
        JOIN Exercise_Equipment ON Equipment.EquipmentID = Exercise_Equipment.EquipmentID
        JOIN Exercise ON Exercise_Equipment.ExerciseID = Exercise.ExerciseID
        ORDER BY DATEDIFF(Exercise.EndTime, Exercise.StartTime) DESC LIMIT 1
        """
        longest_equipment_value = fetch_one(longest_equipment_query)
        longest_equipment_label_value = tk.Label(stats_frame, text=f"持续最长的装备：{longest_equipment_value[0]}", font=("Arial", 14))
        longest_equipment_label_value.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # 返回按钮
        back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Equipment"), bg='#4CAF50', fg='white', font=("Arial", 14))
        back_button.pack(side=tk.BOTTOM, pady=10)

    except Exception as e:
        messagebox.showerror("错误", f"加载数据时发生错误: {e}")



def show_equipment_type_stats(window):
    """展示按装备类型统计的数量"""
    try:
        # 清除现有的显示
        for widget in window.winfo_children():
            widget.destroy()

        # 设置背景图片
        bg_image = Image.open("./icons/bk_admin01.jpg")
        bg_image = bg_image.resize((1600, 800))  # 确保图片大小与窗口一致
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(window, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_photo  # 防止图片被垃圾回收
        bg_label.is_bg_label = True  # 标记为背景图片标签

        # 创建大标题
        title_label = tk.Label(window, text="按装备类型统计数量", font=("Arial", 30), bg='blue', fg='red')
        title_label.pack(pady=(50, 20))

        # 统计信息区域
        stats_frame = tk.Frame(window, bg='white')
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 修正SQL查询，确保其正确执行
        equipment_type_value = fetch_all("SELECT EquipmentType, COUNT(*) FROM Equipment GROUP BY EquipmentType")

        # 计算总数量
        total_count_query = "SELECT COUNT(*) FROM Equipment"
        total_count_result = fetch_one(total_count_query)
        total_count = total_count_result[0] if total_count_result else 0

        # 使用 Treeview 展示统计信息
        treeview = ttk.Treeview(stats_frame, columns=("EquipmentType", "Count"), show="headings")
        treeview.heading("EquipmentType", text="装备类型")
        treeview.heading("Count", text="数量")
        treeview.column("EquipmentType", width=300, anchor="center")
        treeview.column("Count", width=150, anchor="center")

        for row in equipment_type_value:
            treeview.insert("", "end", values=row)

        # 插入总数行
        treeview.insert("", "end", values=("总计", total_count), tags=('total',))

        # 设置总数行的样式
        style = ttk.Style()
        style.configure('Total.TLabel', background='lightgray', foreground='black', font=("Arial", 14, 'bold'))
        treeview.tag_configure('total', background='lightgray', foreground='black', font=("Arial", 14, 'bold'))

        treeview.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 返回按钮
        back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Equipment"),
                                bg='#4CAF50', fg='white', font=("Arial", 14))
        back_button.pack(side=tk.BOTTOM, pady=10)

    except Exception as e:
        messagebox.showerror("错误", f"加载数据时发生错误: {e}")

def show_scale_stats(window):
    """展示按演习统计的规模数量"""
    try:
        # 清除现有的显示
        for widget in window.winfo_children():
            widget.destroy()

        # 统计信息区域
        stats_frame = tk.Frame(window)
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 按演习统计规模数量
        scale_value = fetch_all("SELECT ExerciseID, COUNT(*) FROM Scale GROUP BY ExerciseID")
        scale_label = tk.Label(stats_frame, text="按演习统计的规模数量：", font=("Arial", 14))
        scale_label.grid(row=0, column=0, padx=10, pady=5)

        scale_value_label = tk.Label(stats_frame, text="\n".join([f"演习ID {row[0]}: {row[1]}" for row in scale_value]), font=("Arial", 14))
        scale_value_label.grid(row=1, column=0, padx=10, pady=5)

        # 返回按钮
        back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Scale"))
        back_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("错误", f"加载数据时发生错误: {e}")

def show_media_stats(window):
    """展示媒体总数统计"""
    try:
        # 清除现有的显示
        for widget in window.winfo_children():
            widget.destroy()

        # 统计信息区域
        stats_frame = tk.Frame(window)
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 媒体总数
        total_media_label = tk.Label(stats_frame, text="媒体总数：", font=("Arial", 14))
        total_media_label.grid(row=0, column=0, padx=10, pady=5)

        total_media_value = fetch_all("SELECT COUNT(*) FROM Media")
        total_media_label_value = tk.Label(stats_frame, text=total_media_value[0][0], font=("Arial", 14))
        total_media_label_value.grid(row=0, column=1, padx=10, pady=5)

        # 返回按钮
        back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Media"))
        back_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("错误", f"加载数据时发生错误: {e}")
def show_media_per_exercise_stats(window):
    """展示按演习统计媒体数量"""
    try:
        # 清除现有的显示
        for widget in window.winfo_children():
            widget.destroy()

        # 设置背景图片
        bg_image = Image.open("./icons/bk_admin01.jpg")
        bg_image = bg_image.resize((1600, 800))  # 确保图片大小与窗口一致
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(window, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_photo  # 防止图片被垃圾回收
        bg_label.is_bg_label = True  # 标记为背景图片标签

        # 创建大标题
        title_label = tk.Label(window, text="按演习统计的媒体数量", font=("Arial", 30), bg='blue', fg='red')
        title_label.pack(pady=(50, 20))

        # 统计信息区域
        stats_frame = tk.Frame(window, bg='white')
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 按演习统计媒体数量
        media_per_exercise_value = fetch_all("""
            SELECT ExerciseID, COUNT(*) 
            FROM Media 
            GROUP BY ExerciseID
        """)

        # 查询演习名称
        exercise_names = {row[0]: row[1] for row in fetch_all("SELECT ExerciseID, ExerciseName FROM Exercise")}

        # 计算总媒体数量
        total_media_query = "SELECT COUNT(*) FROM Media"
        total_media_result = fetch_one(total_media_query)
        total_media = total_media_result[0] if total_media_result else 0

        # 使用 Treeview 展示统计信息
        treeview = ttk.Treeview(stats_frame, columns=("ExerciseName", "MediaCount"), show="headings")
        treeview.heading("ExerciseName", text="演习名称")
        treeview.heading("MediaCount", text="媒体数量")
        treeview.column("ExerciseName", width=400, anchor="center")  # 设置列宽
        treeview.column("MediaCount", width=200, anchor="center")    # 设置列宽

        # 插入每个演习的媒体数量
        for row in media_per_exercise_value:
            exercise_name = exercise_names.get(row[0], "未知演习")  # 如果没有找到名称则显示"未知演习"
            treeview.insert("", "end", values=(exercise_name, row[1]))

        # 插入总计行
        treeview.insert("", "end", values=("总计", total_media), tags=('total',))

        # 设置总计行的样式
        style = ttk.Style()
        style.configure('Total.TLabel', background='lightgray', foreground='black', font=("Arial", 14, 'bold'))
        treeview.tag_configure('total', background='lightgray', foreground='black', font=("Arial", 14, 'bold'))

        treeview.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 返回按钮
        back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Media"),
                                bg='#4CAF50', fg='white', font=("Arial", 14))
        back_button.pack(side=tk.BOTTOM, pady=10)

    except Exception as e:
        messagebox.showerror("错误", f"加载数据时发生错误: {e}")




def show_reaction_stats(window):
    """展示反应总数统计"""
    try:
        # 清除现有的显示
        for widget in window.winfo_children():
            widget.destroy()

        # 统计信息区域
        stats_frame = tk.Frame(window)
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 反应总数
        total_reactions_label = tk.Label(stats_frame, text="总反应数：", font=("Arial", 14))
        total_reactions_label.grid(row=0, column=0, padx=10, pady=5)

        total_reactions_value = fetch_all("SELECT COUNT(*) FROM Reaction")
        total_reactions_label_value = tk.Label(stats_frame, text=total_reactions_value[0][0], font=("Arial", 14))
        total_reactions_label_value.grid(row=0, column=1, padx=10, pady=5)

        # 返回按钮
        back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Reaction"))
        back_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("错误", f"加载数据时发生错误: {e}")
def show_reactions_per_exercise_stats(window):
    """展示按演习统计反应数量"""
    try:
        # 清除现有的显示
        for widget in window.winfo_children():
            widget.destroy()

        # 统计信息区域
        stats_frame = tk.Frame(window)
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 按演习统计反应数量
        reactions_per_exercise_value = fetch_all("SELECT ExerciseID, COUNT(*) FROM Reaction GROUP BY ExerciseID")
        reactions_per_exercise_label = tk.Label(stats_frame, text="按演习统计的反应数量：", font=("Arial", 14))
        reactions_per_exercise_label.grid(row=0, column=0, padx=10, pady=5)

        reactions_per_exercise_value_label = tk.Label(stats_frame, text="\n".join([f"演习ID {row[0]}: {row[1]}" for row in reactions_per_exercise_value]), font=("Arial", 14))
        reactions_per_exercise_value_label.grid(row=1, column=0, padx=10, pady=5)

        # 返回按钮
        back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Reaction"))
        back_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("错误", f"加载数据时发生错误: {e}")


# 示例调用
if __name__ == "__main__":
    main_window("admin")  # 或者 main_window("military_enthusiast")