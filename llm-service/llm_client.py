import os
import requests
from dotenv import load_dotenv

load_dotenv()

class QwenClient:
    def __init__(self):
        self.api_key = os.getenv("MODELSCOPE_API_KEY")
        self.base_url = os.getenv("MODELSCOPE_BASE_URL")
        self.model_name = "Qwen/Qwen3-235B-A22B-Instruct-2507"

    def chat(self, messages, temperature=0.7, max_tokens=1024):
        """
        调用 Qwen3-235B 进行对话
        
        参数:
            messages: list, 例如 [{"role": "user", "content": "你好"}]
        """
        url = f"{self.base_url}chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

# 简单测试代码
if __name__ == "__main__":
    client = QwenClient()
    test_messages = [{"role": "user", "content": "你好，请自我介绍一下。"}]
    print(f"📡 正在向 {client.model_name} 发送请求...")
    result = client.chat(test_messages)
    print("✅ 收到响应:")
    print(result)
