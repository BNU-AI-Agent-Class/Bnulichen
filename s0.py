# s0.py —— 最小 API 骨架：单轮对话
# 说明：用户输入一次，模型回答一次，程序即结束。
# 这是所有后续版本的基础：先验证能成功调用一次大模型 API。

from dotenv import load_dotenv; load_dotenv()                      # 1. 从 .env 读取 API 配置
from openai import OpenAI                                           # 2. 导入 OpenAI 兼容 SDK
import os                                                           # 3. 读取环境变量
import sys                                                          # 4. 用于设置输入输出编码
sys.stdin.reconfigure(encoding='utf-8')                             # 5. Windows 终端默认 GBK，改为 UTF-8 避免输入乱码
sys.stdout.reconfigure(encoding='utf-8')                            # 6. Windows 终端默认 GBK，改为 UTF-8 避免输出乱码

client = OpenAI(                                                    # 7. 创建客户端
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL", "https://api.moonshot.cn/v1"),   # 默认 Kimi（Moonshot）接口
)
model = os.getenv("MODEL", "moonshot-v1-8k")                        # 8. 读取模型名称

# 9. 用户输入一次
user_input = input("\n你：")

# 10. 构造单轮 messages
messages = [
    {"role": "system", "content": "你是一个乐于助人的 AI 助手。"},
    {"role": "user", "content": user_input},
]

# 11. 调用模型并输出回答
response = client.chat.completions.create(model=model, messages=messages)
reply = response.choices[0].message.content
print(f"\n[AI] {reply}")

# MIT License | 郑先隽，北师大心理学部教授，人本AI设计与创新
