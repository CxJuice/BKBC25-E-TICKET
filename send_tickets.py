import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
import os
import time  # 添加时间模块用于睡眠

# 邮件服务器配置
SMTP_SERVER = ""  # 替换为你的SMTP服务器地址
SMTP_PORT = 587  # 通常为587
EMAIL_ADDRESS = ""  # 替换为你的邮箱地址
EMAIL_PASSWORD = ""  # 替换为你的邮箱密码

# 读取 JSON 数据
with open("all_orders.json", "r", encoding="utf-8") as f:
    tickets = json.load(f)

# 加载已发送记录
sent_records_path = "sent_records.json"
if os.path.exists(sent_records_path):
    with open(sent_records_path, "r", encoding="utf-8") as f:
        sent_records = json.load(f)
else:
    sent_records = []

# 遍历订单并发送邮件
for ticket in tickets:
    email = ticket['email']
    order_id = ticket['order_id']
    ticket_type = ticket['type']  # 获取 "type" 字段
    pdf_path = f"output/{order_id}.pdf"

    # 跳过已发送的订单
    if order_id in sent_records:
        print(f"订单号 {order_id} 已发送，跳过...")
        continue

    # 跳过 "type" 字段包含 "纪念品包" 的订单
    if "纪念品包" in ticket_type:
        print(f"订单号 {order_id} 的类型为纪念品包，跳过...")
        continue

    # 检查 PDF 文件是否存在
    if not os.path.exists(pdf_path):
        print(f"PDF 文件未找到: {pdf_path}，跳过...")
        continue

    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = "2955北京BC <no-reply@notify.2955bjbc.com>"
    msg['To'] = email
    msg['Subject'] = f"2025北京BC电子门票 - 订单号 {order_id}"

    # 邮件正文
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; font-size: 15px; color: #333;">
        <p>您好，</p>

        <p>
            您的电子门票（订单号：<strong>{order_id}</strong>）已附加在本邮件附件中，
            请下载并妥善保存，<strong>切勿随意分享门票内容</strong>。
        </p>

        <p>
            若您的订单包含代领代寄服务（赏金猎人、深空探索、开拓者），且未能在现场完成核销，我们将根据您提供的邮寄地址为您寄送礼品。
        </p>

        <p><small>由于部分电子邮件服务商存在速率限制，我们已更换了发送门票所使用的邮箱。因此，如果您收到来自多个不同邮箱地址发送的门票邮件，属于正常情况。请放心，所有门票内容一致且均可正常使用。</small></p>

        <p>感谢您的支持与信任！</p>

        <p style="margin-top: 30px;">
            <strong>2955 北京 BC 筹办组</strong>
        </p>
    </body>
    </html>
    """
    # 设置邮件正文为 HTML 格式
    msg.attach(MIMEText(body, 'html'))

    # 附加 PDF 文件
    with open(pdf_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(pdf_path)}",
        )
        msg.attach(part)

    # 发送邮件
    while True:  # 添加循环以处理 550 错误
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
                print(f"邮件已发送至 {email}（订单号：{order_id}）")
                # 记录发送成功的订单号
                sent_records.append(order_id)
                # 立即保存发送记录
                with open(sent_records_path, "w", encoding="utf-8") as f:
                    json.dump(sent_records, f, ensure_ascii=False, indent=4)
                break  # 发送成功，退出循环
        except Exception as e:
            print(f"发送邮件失败: {email}（订单号：{order_id}） - {e}")
            break  # 退出循环，处理下一个订单

print("邮件发送任务完成！")
