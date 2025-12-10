# -*- coding: utf-8 -*-
# 文件名：PPT批量统一裁剪 - 永不报错终极版.py
import os
from tkinter import Tk, Canvas, filedialog, messagebox
from PIL import Image, ImageTk

# ==================== 1. 选文件夹 ====================
root = Tk()
root.withdraw()  # 只隐藏主窗口
folder = filedialog.askdirectory(title="请选中你所有PPT图片所在的文件夹")
if not folder or not os.path.isdir(folder):
    messagebox.showerror("错误", "你没选文件夹，程序结束")
    exit()

files = sorted([f for f in os.listdir(folder)
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp'))])
if not files:
    messagebox.showerror("错误", "这个文件夹里没找到图片！")
    exit()

# ==================== 2. 加载第一张图并缩放显示 ====================
img_path = os.path.join(folder, files[0])
img = Image.open(img_path)

MAX_DISPLAY = 1080
ratio = min(MAX_DISPLAY / img.width, MAX_DISPLAY / img.height, 1.0)
display_w = int(img.width * ratio)
display_h = int(img.height * ratio)
display_img = img.resize((display_w, display_h), Image.Resampling.LANCZOS)

# ==================== 3. 创建唯一的主窗口（关键！只有一个 Tk()） ====================
root.deiconify()  # 把刚才隐藏的那个 root 显示出来
root.title("拖动红框选裁剪区域 → 松开鼠标自动开始")
canvas = Canvas(root, width=display_w, height=display_h, highlightthickness=0)
canvas.pack()

photo = ImageTk.PhotoImage(display_img)  # 创建 PhotoImage
canvas.photo = photo  # ★ 保活！必须加这一句
canvas.create_image(0, 0, anchor="nw", image=photo)

# ==================== 4. 鼠标拖拽选框 ====================
start_x = start_y = 0
rect = None


def press(e):
    global start_x, start_y, rect
    start_x, start_y = e.x, e.y
    rect = canvas.create_rectangle(start_x, start_y, start_x, start_y,
                                   outline="#FF0000", width=5)


def drag(e):
    if rect:
        canvas.coords(rect, start_x, start_y, e.x, e.y)


def release(e):
    if not rect: return

    x1, y1 = e.x, e.y
    # 防止选太小
    if abs(x1 - start_x) < 40: x1 = start_x + 40 if x1 >= start_x else start_x - 40
    if abs(y1 - start_y) < 40: y1 = start_y + 40 if y1 >= start_y else start_y - 40

    left = int(min(start_x, x1) / ratio)
    top = int(min(start_y, y1) / ratio)
    right = int(max(start_x, x1) / ratio)
    bottom = int(max(start_y, y1) / ratio)

    global crop_box
    crop_box = (left, top, right, bottom)
    print(f"\n裁剪区域已确定：{crop_box}  (宽{right - left}×高{bottom - top})")
    root.quit()  # 退出主循环，进入裁剪阶段


canvas.bind("<ButtonPress-1>", press)
canvas.bind("<B1-Motion>", drag)
canvas.bind("<ButtonRelease-1>", release)

print("窗口已弹出，请拖动红框选择你要保留的区域，然后松开鼠标...")
root.mainloop()
root.destroy()  # 彻底关闭窗口

# ==================== 5. 开始批量裁剪 ====================
if 'crop_box' not in globals() or crop_box[2] - crop_box[0] < 50:
    messagebox.showerror("错误", "你选的区域太小了！请重新运行程序")
    exit()

out_folder = os.path.join(folder, "裁剪后")
os.makedirs(out_folder, exist_ok=True)

print(f"开始批量裁剪 {len(files)} 张图片...")
for i, f in enumerate(files, 1):
    im = Image.open(os.path.join(folder, f))
    cropped = im.crop(crop_box)
    cropped.save(os.path.join(out_folder, f"{i:04d}_{f}"))
    im.close()
    print(f"\r已完成 {i}/{len(files)}", end="")

print(f"\n\n全部完成！裁剪后的图片保存在：\n{out_folder}")
messagebox.showinfo("大功告成", f"成功裁剪 {len(files)} 张图片！\n保存在：裁剪后 文件夹")