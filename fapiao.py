# 2023-04-07: designed by ChatGPT  
# 2025-09-05: 复制粘贴后，由AI重构
# pip install pdfminer.six xlsxwriter

import os
import re
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

import xlsxwriter
from pdfminer.high_level import extract_text

YEN_AMOUNT_PATTERN = re.compile(r'[¥￥]\s*([0-9]+(?:\.[0-9]{1,2})?)')
AMOUNT_SUFFIX_PATTERN = re.compile(r'_(\d+(?:\.\d{1,2}))元$', re.IGNORECASE)
REPORT_NAME_PATTERN = re.compile(r'_(\d+(?:\.\d{1,2}))元\.(pdf|jpeg|jpg|png)$', re.IGNORECASE)


class FapiaoApp:
    def __init__(self, root):
        self.root = root
        self._setup_ui()

    def _setup_ui(self):
        self.root.title("报销清单生成器")
        # 简洁窗口，仅一个大按钮
        w, h = 360, 180
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x, y = int((sw - w) / 2), int((sh - h) / 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        main = tk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        btn = tk.Button(
            main,
            text="选择文件夹并一键处理",
            command=self._on_click_process,
            width=28,
            height=3,
            bg="#dfe9ff",
            relief=tk.RAISED
        )
        btn.pack(expand=True)

    def _on_click_process(self):
        dir_path = filedialog.askdirectory()
        if not dir_path:
            return

        scanned_pdf, renamed_pdf, failed_pdf = self._rename_pdfs_with_amount(dir_path)
        file_count, total_amount, report_path = self._generate_report(dir_path)

        message = (
            f"PDF 扫描数量：{scanned_pdf}\n"
            f"成功改名：{renamed_pdf}\n"
            f"失败/跳过：{failed_pdf}\n\n"
            f"报表条目数：{file_count}\n"
            f"合计金额：{total_amount:.2f} 元\n"
            f"报表文件：{report_path}"
        )
        messagebox.showinfo("处理完成", message)

    def _rename_pdfs_with_amount(self, dir_path):
        scanned = renamed = failed = 0
        for name in sorted(os.listdir(dir_path)):
            base, ext = os.path.splitext(name)
            if ext.lower() != ".pdf":
                continue

            scanned += 1

            # 已带“_金额元”后缀的 PDF 跳过
            if AMOUNT_SUFFIX_PATTERN.search(base):
                continue

            src = os.path.join(dir_path, name)

            try:
                text = extract_text(src) or ""
            except Exception:
                failed += 1
                continue

            # 仅基于带货币符号的数值，取最大值
            amounts = [a for a in YEN_AMOUNT_PATTERN.findall(text)]
            if not amounts:
                failed += 1
                continue

            try:
                # 取最大金额（以数值比较）
                amount_str = max(amounts, key=lambda s: float(s))
            except Exception:
                failed += 1
                continue

            # 生成“源文件名_金额元.pdf”（单下划线）
            new_base = f"{base}_{amount_str}元"
            dst_name = f"{new_base}.pdf"
            dst = self._unique_path(dir_path, dst_name)

            try:
                shutil.move(src, dst)
                renamed += 1
            except Exception:
                failed += 1

        return scanned, renamed, failed

    def _generate_report(self, dir_path):
        today = datetime.today().strftime("%Y-%m-%d-%H%M%S")
        tmp_path = os.path.join(dir_path, f"{today}_报销0.00元.xlsx")

        workbook = xlsxwriter.Workbook(tmp_path)
        ws = workbook.add_worksheet()
        money_fmt = workbook.add_format({'num_format': '#,##0.00'})

        ws.write('A1', '文件名')
        ws.write('B1', '报销金额')

        row = 1
        total = 0.0
        count = 0

        for name in sorted(os.listdir(dir_path)):
            m = REPORT_NAME_PATTERN.search(name)
            if not m:
                continue
            try:
                amount = float(m.group(1))
            except ValueError:
                continue

            ws.write(row, 0, name)
            ws.write(row, 1, amount, money_fmt)
            total += amount
            count += 1
            row += 1

        ws.write(row, 0, '总金额')
        ws.write_number(row, 1, total, money_fmt)
        ws.set_column('A:A', 60)
        ws.set_column('B:B', 16, money_fmt)

        workbook.close()

        final_path = os.path.join(dir_path, f"{today}_报销{total:.2f}元.xlsx")
        try:
            os.replace(tmp_path, final_path)
        except Exception:
            # 回退：若替换失败，仍返回临时文件路径
            final_path = tmp_path

        return count, total, final_path

    def _unique_path(self, dir_path, filename):
        # 若存在同名文件，自动追加 (1), (2)...
        base, ext = os.path.splitext(filename)
        candidate = os.path.join(dir_path, filename)
        i = 1
        while os.path.exists(candidate):
            candidate = os.path.join(dir_path, f"{base} ({i}){ext}")
            i += 1
        return candidate


if __name__ == "__main__":
    root = tk.Tk()
    app = FapiaoApp(root)
    root.mainloop()