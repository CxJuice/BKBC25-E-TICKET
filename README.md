# 2025北京BC电子门票生成器

本工具可用于根据订单数据批量生成 PDF 格式的电子门票，并支持通过邮箱发送。
本项目仅作为学习用途，内容和2025北京BC无关。

---

## 1. 填写订单数据（all_orders.json）

在项目根目录下创建或编辑文件 `all_orders.json`，内容格式如下：

```json
[
    {
        "email": "你的邮箱",
        "id": "rup923579z8t679",
        "order_id": "20250416244257403139",
        "type": "赞助门票-开拓者",
        "user_id": "填上你的ID"
    }
]
```

字段说明：

- `email`: 收票邮箱
- `id`: 门票编号
- `order_id`: 订单号
- `type`: 门票类型
- `user_id`: 用户 ID

---

## 2. 运行 main.py 生成电子门票

执行以下命令：

```bash
python main.py
```

程序会在 `output/` 文件夹下生成 PDF 格式的电子门票。

---

## 3. 邮件发送功能（可选）

如需发送门票至邮箱，请编辑 `send_tickets.py`，填写以下配置：

```python
# 邮件服务器配置
SMTP_SERVER = ""         # 替换为你的 SMTP 服务器地址，例如 smtp.qq.com
SMTP_PORT = 587          # 通常为 587
EMAIL_ADDRESS = ""       # 替换为你的发件邮箱地址
EMAIL_PASSWORD = ""      # 替换为你的邮箱密码或授权码
```

然后运行：

```bash
python send_tickets.py
```

程序将自动读取 `output/` 文件夹下的 PDF，并将门票发送到每位用户的邮箱。

---

## 4. 所需依赖库

请先安装以下第三方库：

```bash
pip install PyMuPDF qrcode pillow
```

标准库（无需额外安装）：

- `smtplib`
- `email`
- `json`
- `os`
- `time`

---

## 📁 项目结构示例

```
.
├── all_orders.json         # 用户订单数据
├── main.py                 # 门票生成主程序
├── send_tickets.py         # 邮件发送脚本
├── output/                 # 生成的 PDF 门票文件夹
└── README.md               # 使用说明
```

---

如需自定义门票模板或二维码内容，欢迎自行修改 `main.py` 中相关逻辑。
