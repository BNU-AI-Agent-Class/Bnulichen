# s1_turn.py —— 单轮聊天：验证环境能跑
# 说明：持续接收用户输入，但每次对话都是独立的单轮请求，不保留历史记忆。
# 重点验证 .env 配置、API 调用、模型返回是否正常。

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

print("[系统] 环境已加载，输入空行跳过。输入 'exit' 退出。")            # 9. 启动提示

while True:                                                         # 10. 外层循环：持续接收新任务
    user_input = input("\n你：")                                     # 11. 等待用户输入
    if not user_input:                                              # 12. 跳过空输入
        continue
    if user_input.lower() in ("exit", "quit", "退出"):              # 13. 支持退出
        break

    # 14. 每次重新构造 messages，不保留历史
    messages = [
        {"role": "system", "content": "你是一个乐于助人的 AI 助手。"},
        {"role": "user", "content": user_input},
    ]

    # 15. 调用模型并输出回答
    response = client.chat.completions.create(model=model, messages=messages)
    reply = response.choices[0].message.content
    print(f"\n[AI] {reply}")

# MIT License | 郑先隽，北师大心理学部教授，人本AI设计与创新
