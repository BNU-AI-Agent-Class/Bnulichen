# s2_memory.py —— 多轮对话 + 记忆
# 说明：使用同一个 messages 列表保存对话历史，因此用户可以追问，模型记得上文。

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

# 9. 初始化对话历史，只包含系统提示
messages = [{"role": "system", "content": "你是一个乐于助人的 AI 助手。"}]

print("[系统] 多轮对话已启动，我会记住上下文。输入 'exit' 退出，输入 'clear' 清空历史。")

while True:                                                         # 10. 主循环：持续多轮对话
    user_input = input("\n你：")                                     # 11. 等待用户输入
    if not user_input:                                              # 12. 跳过空输入
        continue
    if user_input.lower() in ("exit", "quit", "退出"):              # 13. 支持退出
        break
    if user_input.lower() == "clear":                               # 14. 支持清空历史
        messages = [messages[0]]
        print("[系统] 历史已清空。")
        continue

    # 15. 把用户输入加入历史
    messages.append({"role": "user", "content": user_input})

    # 16. 调用模型
    response = client.chat.completions.create(model=model, messages=messages)
    reply = response.choices[0].message.content

    # 17. 把模型回答也加入历史，形成记忆
    messages.append({"role": "assistant", "content": reply})
    print(f"\n[AI] {reply}")

# MIT License | 郑先隽，北师大心理学部教授，人本AI设计与创新
