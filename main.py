import fitz  # PyMuPDF
import qrcode
from qrcode.image.pil import PilImage
import json
import os

# 读取 JSON 数据
with open("all_orders.json", "r", encoding="utf-8") as f:
    tickets = json.load(f)

# 确保输出文件夹存在
os.makedirs("output", exist_ok=True)

# 加载 Noto Sans 字体
font_path = "NotoSansSC-Bold.ttf"  # 确保字体文件在同一文件夹中
if not os.path.exists(font_path):
    raise FileNotFoundError(f"字体文件 {font_path} 未找到，请确保文件存在。")

for ticket in tickets:
    id_ = ticket['id']  # 使用 id
    user_id = ticket['user_id'] if 'user_id' in ticket else "N/A"
    ticket_type = ticket['type']
    order_id = ticket['order_id']
    
    # 输出文件路径
    output_path = f"output/{order_id}.pdf"

    # 如果文件已存在，跳过生成
    if os.path.exists(output_path):
        print(f"文件 {output_path} 已存在，跳过生成。")
        continue

    # 使用 id 生成二维码内容
    qr_content = id_

    # 打开原始模板
    doc = fitz.open("input.pdf")
    page = doc[0]

    # 在固定位置写文本（修复 color 参数）
    page.insert_text((440, 1545), f"{user_id}", fontsize=96, fontname='Noto-Sans-SC-Bold', fontfile=font_path, color=(0.12, 0.12, 0.12))  # 转换为 0-1 范围
    page.insert_text((730, 1787), f"{ticket_type}", fontsize=96, fontname='Noto-Sans-SC-Bold', fontfile=font_path, color=(0.12, 0.12, 0.12))  # 转换为 0-1 范围
    page.insert_text((730, 2029), f"{order_id}", fontsize=96, fontname='Noto-Sans-SC-Bold', fontfile=font_path, color=(0.12, 0.12, 0.12))  # 转换为 0-1 范围

    # 生成二维码临时保存（调整二维码尺寸）
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,  # 调整 box_size 值以改变二维码尺寸（默认值为 10）
        border=0  # 移除白色边框
    )
    qr.add_data(qr_content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#272E39", back_color="#D9D9D9")  # 设置黑色为 #272E39，无背景
    qr_path = f"temp_qr_{id_}.png"
    img.save(qr_path)

    # 插入二维码到指定位置
    rect = fitz.Rect(1300, 2380, 2000, 3080)  # 确保矩形的宽度和高度不为零
    page.insert_image(rect, filename=qr_path)

    # 保存输出
    doc.save(output_path)
    doc.close()

    # 删除临时二维码
    os.remove(qr_path)

print("全部生成完成！")