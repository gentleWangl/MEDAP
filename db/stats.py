# import tkinter as tk
# from tkinter import messagebox
# from PIL import Image, ImageTk
# from tkinter import ttk, messagebox
# from db.utils import fetch_all







# def show_equipment_stats(window):
#     """展示装备总数统计"""
#     try:
#         # 清除现有的显示
#         for widget in window.winfo_children():
#             widget.destroy()

#         # 统计信息区域
#         stats_frame = tk.Frame(window)
#         stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

#         # 装备总数
#         total_equipment_label = tk.Label(stats_frame, text="总装备数：", font=("Arial", 14))
#         total_equipment_label.grid(row=0, column=0, padx=10, pady=5)

#         total_equipment_value = fetch_all("SELECT COUNT(*) FROM Equipment")
#         total_equipment_label_value = tk.Label(stats_frame, text=total_equipment_value[0][0], font=("Arial", 14))
#         total_equipment_label_value.grid(row=0, column=1, padx=10, pady=5)

#         # 返回按钮
#         back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Equipment"))
#         back_button.pack(pady=10)

#     except Exception as e:
#         messagebox.showerror("错误", f"加载数据时发生错误: {e}")

# def show_country_exercise_stats(window):
#     """展示按国家统计的演习数量"""
#     try:
#         # 清除现有的显示
#         for widget in window.winfo_children():
#             widget.destroy()

#         # 统计信息区域
#         stats_frame = tk.Frame(window)
#         stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

#         # 按国家统计演习数量
#         country_exercises_value = fetch_all("SELECT Country, COUNT(*) FROM Exercise GROUP BY Country")
#         country_exercises_label = tk.Label(stats_frame, text="按国家统计的演习数量：", font=("Arial", 14))
#         country_exercises_label.grid(row=0, column=0, padx=10, pady=5)

#         country_exercises_value_label = tk.Label(stats_frame, text="\n".join([f"{row[0]}: {row[1]}" for row in country_exercises_value]), font=("Arial", 14))
#         country_exercises_value_label.grid(row=1, column=0, padx=10, pady=5)

#         # 返回按钮
#         back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Exercise"))
#         back_button.pack(pady=10)

#     except Exception as e:
#         messagebox.showerror("错误", f"加载数据时发生错误: {e}")

# def show_exercise_stats(window):
#     """展示演习总数统计"""
#     try:
#         # 清除现有的显示
#         for widget in window.winfo_children():
#             widget.destroy()

#         # 统计信息区域
#         stats_frame = tk.Frame(window)
#         stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

#         # 演习总数
#         total_exercises_label = tk.Label(stats_frame, text="总演习数：", font=("Arial", 14))
#         total_exercises_label.grid(row=0, column=0, padx=10, pady=5)

#         total_exercises_value = fetch_all("SELECT COUNT(*) FROM Exercise")
#         total_exercises_label_value = tk.Label(stats_frame, text=total_exercises_value[0][0], font=("Arial", 14))
#         total_exercises_label_value.grid(row=0, column=1, padx=10, pady=5)

#         # 返回按钮
#         back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Exercise"))
#         back_button.pack(pady=10)

#     except Exception as e:
#         messagebox.showerror("错误", f"加载数据时发生错误: {e}")

# def show_equipment_type_stats(window):
#     """展示按装备类型统计的数量"""
#     try:
#         # 清除现有的显示
#         for widget in window.winfo_children():
#             widget.destroy()

#         # 统计信息区域
#         stats_frame = tk.Frame(window)
#         stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

#         # 按装备类型统计数量
#         equipment_type_value = fetch_all("SELECT EquipmentType, COUNT(*) FROM Equipment GROUP BY EquipmentType")
#         equipment_type_label = tk.Label(stats_frame, text="按装备类型统计数量：", font=("Arial", 14))
#         equipment_type_label.grid(row=0, column=0, padx=10, pady=5)

#         equipment_type_value_label = tk.Label(stats_frame, text="\n".join([f"{row[0]}: {row[1]}" for row in equipment_type_value]), font=("Arial", 14))
#         equipment_type_value_label.grid(row=1, column=0, padx=10, pady=5)

#         # 返回按钮
#         back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Equipment"))
#         back_button.pack(pady=10)

#     except Exception as e:
#         messagebox.showerror("错误", f"加载数据时发生错误: {e}")
# def show_scale_stats(window):
#     """展示按演习统计的规模数量"""
#     try:
#         # 清除现有的显示
#         for widget in window.winfo_children():
#             widget.destroy()

#         # 统计信息区域
#         stats_frame = tk.Frame(window)
#         stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

#         # 按演习统计规模数量
#         scale_value = fetch_all("SELECT ExerciseID, COUNT(*) FROM Scale GROUP BY ExerciseID")
#         scale_label = tk.Label(stats_frame, text="按演习统计的规模数量：", font=("Arial", 14))
#         scale_label.grid(row=0, column=0, padx=10, pady=5)

#         scale_value_label = tk.Label(stats_frame, text="\n".join([f"演习ID {row[0]}: {row[1]}" for row in scale_value]), font=("Arial", 14))
#         scale_value_label.grid(row=1, column=0, padx=10, pady=5)

#         # 返回按钮
#         back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Scale"))
#         back_button.pack(pady=10)

#     except Exception as e:
#         messagebox.showerror("错误", f"加载数据时发生错误: {e}")
# def show_media_stats(window):
#     """展示媒体总数统计"""
#     try:
#         # 清除现有的显示
#         for widget in window.winfo_children():
#             widget.destroy()

#         # 统计信息区域
#         stats_frame = tk.Frame(window)
#         stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

#         # 媒体总数
#         total_media_label = tk.Label(stats_frame, text="媒体总数：", font=("Arial", 14))
#         total_media_label.grid(row=0, column=0, padx=10, pady=5)

#         total_media_value = fetch_all("SELECT COUNT(*) FROM Media")
#         total_media_label_value = tk.Label(stats_frame, text=total_media_value[0][0], font=("Arial", 14))
#         total_media_label_value.grid(row=0, column=1, padx=10, pady=5)

#         # 返回按钮
#         back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Media"))
#         back_button.pack(pady=10)

#     except Exception as e:
#         messagebox.showerror("错误", f"加载数据时发生错误: {e}")
# def show_media_per_exercise_stats(window):
#     """展示按演习统计媒体数量"""
#     try:
#         # 清除现有的显示
#         for widget in window.winfo_children():
#             widget.destroy()

#         # 统计信息区域
#         stats_frame = tk.Frame(window)
#         stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

#         # 按演习统计媒体数量
#         media_per_exercise_value = fetch_all("SELECT ExerciseID, COUNT(*) FROM Media GROUP BY ExerciseID")
#         media_per_exercise_label = tk.Label(stats_frame, text="按演习统计的媒体数量：", font=("Arial", 14))
#         media_per_exercise_label.grid(row=0, column=0, padx=10, pady=5)

#         media_per_exercise_value_label = tk.Label(stats_frame, text="\n".join([f"演习ID {row[0]}: {row[1]}" for row in media_per_exercise_value]), font=("Arial", 14))
#         media_per_exercise_value_label.grid(row=1, column=0, padx=10, pady=5)

#         # 返回按钮
#         back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Media"))
#         back_button.pack(pady=10)

#     except Exception as e:
#         messagebox.showerror("错误", f"加载数据时发生错误: {e}")
# def show_reaction_stats(window):
#     """展示反应总数统计"""
#     try:
#         # 清除现有的显示
#         for widget in window.winfo_children():
#             widget.destroy()

#         # 统计信息区域
#         stats_frame = tk.Frame(window)
#         stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

#         # 反应总数
#         total_reactions_label = tk.Label(stats_frame, text="总反应数：", font=("Arial", 14))
#         total_reactions_label.grid(row=0, column=0, padx=10, pady=5)

#         total_reactions_value = fetch_all("SELECT COUNT(*) FROM Reaction")
#         total_reactions_label_value = tk.Label(stats_frame, text=total_reactions_value[0][0], font=("Arial", 14))
#         total_reactions_label_value.grid(row=0, column=1, padx=10, pady=5)

#         # 返回按钮
#         back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Reaction"))
#         back_button.pack(pady=10)

#     except Exception as e:
#         messagebox.showerror("错误", f"加载数据时发生错误: {e}")
# def show_reactions_per_exercise_stats(window):
#     """展示按演习统计反应数量"""
#     try:
#         # 清除现有的显示
#         for widget in window.winfo_children():
#             widget.destroy()

#         # 统计信息区域
#         stats_frame = tk.Frame(window)
#         stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

#         # 按演习统计反应数量
#         reactions_per_exercise_value = fetch_all("SELECT ExerciseID, COUNT(*) FROM Reaction GROUP BY ExerciseID")
#         reactions_per_exercise_label = tk.Label(stats_frame, text="按演习统计的反应数量：", font=("Arial", 14))
#         reactions_per_exercise_label.grid(row=0, column=0, padx=10, pady=5)

#         reactions_per_exercise_value_label = tk.Label(stats_frame, text="\n".join([f"演习ID {row[0]}: {row[1]}" for row in reactions_per_exercise_value]), font=("Arial", 14))
#         reactions_per_exercise_value_label.grid(row=1, column=0, padx=10, pady=5)

#         # 返回按钮
#         back_button = tk.Button(window, text="返回", command=lambda: user_show_table(window, "Reaction"))
#         back_button.pack(pady=10)

#     except Exception as e:
#         messagebox.showerror("错误", f"加载数据时发生错误: {e}")
