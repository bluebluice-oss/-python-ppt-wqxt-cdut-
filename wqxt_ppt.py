import re
import requests
import os
from urllib.parse import urlparse

# 1. 把你之前保存的完整 html 文件路径改这里
html_file = r"D:\xxxxx\xxxx\xxxxx\saved_page.html"   # ← 改这里

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 2. 提取所有真实高清图（优先 data-src，其次 src）
urls = re.findall(r'data-src="(https?://video\.wqxt\.cdut\.edu\.cn/ai3/ppt[^"]+\.jpg)"', html)
if not urls:  # 万一没抓到 data-src，就用 src
    urls = re.findall(r'<img[^>]+src="(http[^"]+\.jpg)"', html, re.I)

urls = list(dict.fromkeys(urls))  # 去重但保持顺序

# 3. 下载
os.makedirs('PPT全套', exist_ok=True)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://video.wqxt.cdut.edu.cn/'   # 很多教育平台要这个防盗链
}

for i, url in enumerate(urls, 1):
    try:
        print(f"下载 {i}/{len(urls)}: {url}")
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 200:
            filename = url.split('/')[-1]          # 取 4306192.jpg
            # 或者用页码命名更好找（从 ppt_order 提取页码）
            # 这里简单用原文件名
            with open(f'PPT全套/{i:03d}_{filename}', 'wb') as f:
                f.write(r.content)
        else:
            print("  下载失败，状态码:", r.status_code)
    except Exception as e:
        print("  异常:", e)

print("全部下载完成！保存在 PPT全套 文件夹")
