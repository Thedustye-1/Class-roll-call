import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

class EnhancedRollCall:
    def __init__(self, root):
        self.root = root
        self.root.title("隧三智能课堂点名系统")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f8ff')
        
        # 初始化变量
        self.is_rolling = False
        self.current_number = 0
        self.roll_count = 0  # 这里初始化 roll_count
        
        # 设置窗口图标和居中
        self.center_window(600, 500)
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建界面元素
        self.create_widgets()
        
    def center_window(self, width, height):
        """将窗口居中显示"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 关于菜单
        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="关于", menu=about_menu)
        about_menu.add_command(label="版权信息", command=self.show_copyright)
        about_menu.add_separator()
        about_menu.add_command(label="退出", command=self.root.quit)
        
    def create_widgets(self):
        """创建界面元素"""
        # 主标题框架
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🎓 隧三智能课堂点名系统", 
                              font=("微软雅黑", 24, "bold"), 
                              fg="white", bg='#2c3e50')
        title_label.pack(expand=True)
        
        # 数字显示区域
        display_frame = tk.Frame(self.root, bg='#ecf0f1', relief='ridge', bd=3)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.number_label = tk.Label(display_frame, text="准备开始", 
                                    font=("Arial", 48, "bold"), 
                                    bg="#34495e", fg="#e74c3c",
                                    width=12, height=3, relief="sunken")
        self.number_label.pack(pady=30)
        
        # 控制按钮区域
        button_frame = tk.Frame(self.root, bg='#f0f8ff')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.start_button = tk.Button(button_frame, text="🎲 开始点名", 
                                     font=("微软雅黑", 16, "bold"), 
                                     command=self.toggle_roll_call, 
                                     bg="#27ae60", fg="white",
                                     width=15, height=2,
                                     relief="raised", bd=3)
        self.start_button.pack(pady=10)
        
        # 状态信息区域
        info_frame = tk.Frame(self.root, bg='#f0f8ff')
        info_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.status_label = tk.Label(info_frame, text="系统就绪，点击开始按钮进行点名", 
                                    font=("微软雅黑", 12), 
                                    fg="#2c3e50", bg='#f0f8ff')
        self.status_label.pack()
        
        # 统计信息 - 使用实例变量
        self.stats_label = tk.Label(info_frame, text=f"今日已点名: {self.roll_count} 次", 
                                   font=("微软雅黑", 10), 
                                   fg="#7f8c8d", bg='#f0f8ff')
        self.stats_label.pack()
        
        # 历史记录区域
        history_frame = tk.LabelFrame(self.root, text="📝 点名历史记录", 
                                     font=("微软雅黑", 12, "bold"),
                                     bg='#f0f8ff', fg='#2c3e50')
        history_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 添加滚动条
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(history_frame, height=8, width=50, 
                                   font=("Consolas", 10),
                                   yscrollcommand=scrollbar.set,
                                   bg='#fafafa', fg='#2c3e50',
                                   relief='solid', bd=1)
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.history_text.yview)
        self.history_text.config(state=tk.DISABLED)
        
        # 底部按钮区域
        bottom_frame = tk.Frame(self.root, bg='#f0f8ff')
        bottom_frame.pack(fill=tk.X, padx=20, pady=10)
        
        clear_button = tk.Button(bottom_frame, text="🗑️ 清空记录", 
                                font=("微软雅黑", 10), 
                                command=self.clear_history, 
                                bg="#e67e22", fg="white",
                                width=12, height=1)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        export_button = tk.Button(bottom_frame, text="💾 导出记录", 
                                 font=("微软雅黑", 10), 
                                 command=self.export_history, 
                                 bg="#3498db", fg="white",
                                 width=12, height=1)
        export_button.pack(side=tk.LEFT, padx=5)
        
        # 添加样式
        self.apply_styles()
    
    def apply_styles(self):
        """应用样式"""
        style = ttk.Style()
        style.configure("TButton", font=("微软雅黑", 10))
        
    def toggle_roll_call(self):
        """切换点名状态"""
        if not self.is_rolling:
            # 开始点名
            self.is_rolling = True
            self.start_button.config(text="⏹️ 停止点名", bg="#e74c3c")
            self.status_label.config(text="点名进行中...", fg="#e74c3c")
            self.roll_call()
        else:
            # 停止点名
            self.is_rolling = False
            self.start_button.config(text="🎲 开始点名", bg="#27ae60")
            self.status_label.config(text=f"选中学生: 第 {self.current_number} 号", fg="#27ae60")
            self.roll_count += 1
            
            # 更新统计信息
            self.stats_label.config(text=f"今日已点名: {self.roll_count} 次")
            
            # 添加到历史记录
            self.add_to_history(self.current_number)
    
    def roll_call(self):
        """执行点名动画"""
        if self.is_rolling:
            self.current_number = random.randint(1, 45)
            self.number_label.config(text=str(self.current_number))
            
            # 随机改变颜色增加动感效果
            colors = ["#e74c3c", "#3498db", "#9b59b6", "#e67e22", "#2ecc71"]
            self.number_label.config(fg=random.choice(colors))
            
            self.root.after(80, self.roll_call)  # 每80毫秒更新一次
    
    def add_to_history(self, number):
        """将选中的数字添加到历史记录"""
        self.history_text.config(state=tk.NORMAL)
        
        # 获取当前时间
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # 插入新记录到开头
        self.history_text.insert("1.0", f"[{current_time}] 选中学生: 第 {number:2d} 号\n")
        
        # 限制历史记录行数
        lines = self.history_text.get("1.0", tk.END).split('\n')
        if len(lines) > 21:  # 保留20条记录
            self.history_text.delete("20.0", tk.END)
            
        self.history_text.config(state=tk.DISABLED)
    
    def clear_history(self):
        """清空历史记录"""
        if messagebox.askyesno("确认", "确定要清空所有历史记录吗？"):
            self.history_text.config(state=tk.NORMAL)
            self.history_text.delete("1.0", tk.END)
            self.history_text.config(state=tk.DISABLED)
            messagebox.showinfo("成功", "历史记录已清空！")
    
    def export_history(self):
        """导出历史记录（示例功能）"""
        messagebox.showinfo("导出", "导出功能开发中...\n这里可以添加保存到文件的功能")
    
    def show_copyright(self):
        """显示版权信息"""
        copyright_info = """
隧三智能课堂点名系统 v3.0

版权所有 © 2025-2030 Thedustye
保留所有权利

开发者: Thedustye
联系方式: thedustye1@outlook.com
官方网站: www.thedustye.com

本软件仅供教学使用，未经许可不得用于商业用途。

感谢使用我们的课堂点名系统！
        """
        messagebox.showinfo("版权信息", copyright_info)

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedRollCall(root)
    
    # 设置窗口图标（如果有图标文件）
    try:
        root.iconbitmap("rollcall_icon.ico")  # 如果有图标文件可以取消注释
    except:
        pass
        
    root.mainloop()