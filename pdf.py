# -*- coding: utf-8 -*-
from PIL import Image
import os, tkinter.filedialog as fd

# 1. 选文件夹
folder = fd.askdirectory(title="请选择裁剪好的图片文件夹")
if not folder: exit()
files = sorted([f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))])
if not files: exit("没找到图片")

imgs = [Image.open(os.path.join(folder, f)).convert("RGB") for f in files]

# 2. 选择每页放几张
print("每页竖着放几张？（推荐3或4）")
n = input("输入 3 或 4（默认4）：").strip()
n = 4 if n not in ["3", "4"] else int(n)

# A4 @ 300dpi
A4_W, A4_H = 2480, 3508
left_margin = 150  # 左边距稍大一点（可自行改小）
top_margin = 30
gap = 20  # 图之间间隙
right_left_space = A4_W - left_margin - 150  # 右侧预留写笔记空间

per_h = (A4_H - top_margin * 2 - gap * (n - 1)) // n  # 每张可用高度

pages = []
for i in range(0, len(imgs), n):
    page = Image.new("RGB", (A4_W, A4_H), "white")
    for j in range(n):
        if i + j >= len(imgs): break
        img = imgs[i + j]
        # 等比缩放，宽度撑满可用空间（左对齐所以宽度最大化）
        ratio = min(right_left_space / img.width, per_h / img.height)
        new_w = int(img.width * ratio)
        new_h = int(img.height * ratio)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        y = top_margin + j * (per_h + gap)
        x = left_margin  # 固定左对齐！！！
        page.paste(img, (x, y))
    pages.append(page)

save_path = os.path.join(folder, f"【A4左对齐-每页{n}张】完整课件.pdf")
pages[0].save(save_path, save_all=True, append_images=pages[1:], dpi=(300, 300), quality=95)
print(f"\n成功！已生成左对齐PDF：\n{save_path}")
os.startfile(folder)
input("按回车退出")