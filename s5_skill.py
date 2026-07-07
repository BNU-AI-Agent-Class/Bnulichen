# s5_skill.py —— 专业 Agent：导师审阅研究报告
# 说明：同一个 Agent 框架，换上导师审阅技能包（skill_mentor_review.md）。
# 用户提供研究报告文件路径后，Agent 会读取文件并给出导师级审阅意见。

from dotenv import load_dotenv; load_dotenv()                      # 1. 从 .env 读取 API 配置
from openai import OpenAI                                           # 2. 导入 OpenAI 兼容 SDK
import os                                                           # 3. 读取环境变量和执行命令
import sys                                                          # 4. 用于设置输入输出编码
sys.stdin.reconfigure(encoding='utf-8')                             # 5. Windows 终端默认 GBK，改为 UTF-8 避免输入乱码
sys.stdout.reconfigure(encoding='utf-8')                            # 6. Windows 终端默认 GBK，改为 UTF-8 避免输出乱码

client = OpenAI(                                                    # 7. 创建客户端
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL", "https://api.moonshot.cn/v1"),   # 默认 Kimi（Moonshot）接口
)
model = os.getenv("MODEL", "moonshot-v1-8k")                        # 8. 读取模型名称

# 9. 加载通用 Agent 规则 + 导师审阅技能
with open("agent.md", encoding="utf-8") as f:
    agent_rule = f.read()
with open("skill_mentor_review.md", encoding="utf-8") as f:
    skill = f.read()
system_prompt = f"{agent_rule}\n\n{skill}"

while True:                                                         # 10. 外层循环：等待用户输入新任务
    messages = [{"role": "system", "content": system_prompt}]       # 11. 每个新任务重置上下文，保留规则和技能
    user_input = input("\n你：")                                     # 12. 等待用户输入
    if not user_input:                                              # 13. 跳过空输入
        continue
    if user_input.lower() in ("exit", "quit", "退出"):              # 14. 支持退出
        break
    messages.append({"role": "user", "content": user_input})        # 15. 存入对话历史

    while True:                                                     # 16. 内层循环：Agent 自主执行，直到任务完成
        response = client.chat.completions.create(                  # 17. 发送对话历史给模型
            model=model,
            messages=messages,
        )
        reply = response.choices[0].message.content                 # 18. 提取模型回复
        messages.append({"role": "assistant", "content": reply})    # 19. 存入历史
        print(f"[AI] {reply}")                                      # 20. 打印模型决策

        if reply.strip().startswith("完成:"):                        # 21. 任务完成，跳出内层循环
            break

        if "命令:" not in reply:                                    # 22. 没有命令则结束本次任务
            print("[系统] AI 没有给出可执行的命令，结束本次任务。")
            break

        command = reply.strip().split("命令:")[1].strip()            # 23. 提取 AI 想执行的命令
        result = os.popen(command).read()                           # 24. 执行命令
        print(f"[系统] {result}")                                    # 25. 打印命令结果
        messages.append({"role": "user", "content": f"执行完毕:{result}"})  # 26. 反馈给模型

# MIT License | 郑先隽，北师大心理学部教授，人本AI设计与创新
