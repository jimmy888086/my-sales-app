# 【修复重点】这里补上了 import datetime
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ==========================================
# 1. 核心后端逻辑与算法优化 (Backend Logic)
# ==========================================
DATA_FILE = "dealership_db.json"

class SmartPayrollSystem:
    def __init__(self):
        self.data = self.load_data()
        self.currency = "RM"

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def add_sale(self, record):
        self.data.append(record)
        self.save_data()

    def get_stats(self):
        total_profit = sum(item['profit'] for item in self.data)
        total_sales = len(self.data)
        return total_profit, total_sales

# ==========================================
# 2. 前端界面 (GUI)
# ==========================================
class App:
    def __init__(self, root):
        self.db = SmartPayrollSystem()
        self.root = root
        self.root.title("2026 车行智能管理系统")
        self.root.geometry("500x700")
        self.root.configure(bg="#1e1e1e") # 深色背景

        # 样式配置
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12), padding=6, background="#4CAF50")
        style.map("TButton", background=[("active", "#45a049")])
        style.configure("TEntry", padding=6)

        self.create_widgets()

    def create_widgets(self):
        # --- 标题 ---
        lbl_title = tk.Label(self.root, text="🚗 车辆销售录入", font=("Helvetica", 18, "bold"), bg="#1e1e1e", fg="#4CAF50")
        lbl_title.pack(pady=20)

        # --- 表单框架 ---
        form_frame = tk.Frame(self.root, bg="#1e1e1e")
        form_frame.pack(padx=20, pady=10, fill="x")

        # 销售员姓名
        ttk.Label(form_frame, text="销售员姓名:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_seller = ttk.Entry(form_frame)
        self.entry_seller.grid(row=0, column=1, sticky="ew", pady=5)

        # 日期 (自动填充今天)
        ttk.Label(form_frame, text="销售日期 (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_date = ttk.Entry(form_frame)
        self.entry_date.grid(row=1, column=1, sticky="ew", pady=5)
        # 【修复点】这里现在可以正常运行了
        self.entry_date.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))

        # 车牌号
        ttk.Label(form_frame, text="车牌号码:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_plate = ttk.Entry(form_frame)
        self.entry_plate.grid(row=2, column=1, sticky="ew", pady=5)

        # 车型
        ttk.Label(form_frame, text="车型描述:").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_model = ttk.Entry(form_frame)
        self.entry_model.grid(row=3, column=1, sticky="ew", pady=5)

        # 成本价
        ttk.Label(form_frame, text="💰 车辆成本 (RM):").grid(row=4, column=0, sticky="w", pady=5)
        self.entry_cost = ttk.Entry(form_frame)
        self.entry_cost.grid(row=4, column=1, sticky="ew", pady=5)

        # 销售价
        ttk.Label(form_frame, text="💸 销售价格 (RM):").grid(row=5, column=0, sticky="w", pady=5)
        self.entry_price = ttk.Entry(form_frame)
        self.entry_price.grid(row=5, column=1, sticky="ew", pady=5)

        # 让输入框横向填满
        form_frame.columnconfigure(1, weight=1)

        # --- 按钮 ---
        btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        btn_frame.pack(pady=20)

        self.btn_save = ttk.Button(btn_frame, text="💾 录入销售记录", command=self.save_record)
        self.btn_save.pack(fill="x", padx=40, pady=5)

        self.btn_view = ttk.Button(btn_frame, text="📊 查看老板报表", command=self.show_report)
        self.btn_view.pack(fill="x", padx=40, pady=5)

    def save_record(self):
        # 获取数据
        seller = self.entry_seller.get()
        date = self.entry_date.get()
        plate = self.entry_plate.get()
        model = self.entry_model.get()
        cost_str = self.entry_cost.get()
        price_str = self.entry_price.get()

        # 简单验证
        if not seller or not plate or not cost_str or not price_str:
            messagebox.showwarning("警告", "请填写必填项（姓名、车牌、价格）！")
            return

        try:
            cost = float(cost_str)
            price = float(price_str)
            profit = price - cost

            # 简单的提成算法：利润的 10%
            commission = profit * 0.10
            if profit < 0: commission = 0 # 亏本没提成

            # 保存数据
            record = {
                "seller": seller,
                "date": date,
                "plate": plate,
                "model": model,
                "cost": cost,
                "price": price,
                "profit": profit,
                "commission": commission
            }

            self.db.add_sale(record)

            # 成功提示
            messagebox.showinfo("成功", f"录入成功！\n预估提成: {self.db.currency} {commission:,.2f}")

            # 清空输入框（除了销售员名字，方便连续录入）
            self.entry_plate.delete(0, tk.END)
            self.entry_model.delete(0, tk.END)
            self.entry_cost.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("错误", "价格和成本必须是数字！")

    def show_report(self):
        # 弹出新窗口显示报表
        top = tk.Toplevel(self.root)
        top.title("📊 老板报表")
        top.geometry("400x500")
        top.configure(bg="#252526")

        total_profit, total_sales = self.db.get_stats()

        lbl = tk.Label(top, text="📈 销售统计概览", font=("Helvetica", 16, "bold"), bg="#252526", fg="#4CAF50")
        lbl.pack(pady=10)

        info_frame = tk.Frame(top, bg="#252526")
        info_frame.pack(pady=10)

        tk.Label(info_frame, text=f"总销量:", font=("Helvetica", 12), bg="#252526", fg="white").grid(row=0, column=0, sticky="w", padx=20)
        tk.Label(info_frame, text=f"{total_sales} 辆", font=("Helvetica", 12, "bold"), bg="#252526", fg="white").grid(row=0, column=1, sticky="w")

        tk.Label(info_frame, text=f"总毛利润:", font=("Helvetica", 12), bg="#252526", fg="white").grid(row=1, column=0, sticky="w", padx=20)
        tk.Label(info_frame, text=f"{self.db.currency} {total_profit:,.2f}", font=("Helvetica", 12, "bold"), bg="#252526", fg="#FFD700").grid(row=1, column=1, sticky="w")

        # 详细列表
        tk.Label(top, text="--- 详细记录 ---", font=("Helvetica", 10), bg="#252526", fg="gray").pack(pady=5)

        # 创建一个带滚动条的列表框
        listbox = tk.Listbox(top, bg="#1e1e1e", fg="white", font=("Courier", 9), height=15)
        listbox.pack(fill="both", expand=True, padx=20, pady=5)

        for item in reversed(self.db.data): # 倒序显示，最新的在最上面
            text = f"[{item['date']}] {item['plate']} ({item['model']})\n   卖价: {item['price']} | 赚: {item['profit']} | 员: {item['seller']}"
            listbox.insert(tk.END, text)

# ==========================================
# 3. 启动程序
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
