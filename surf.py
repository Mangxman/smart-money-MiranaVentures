import requests

class SurfAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.asksurf.ai/gateway/v1/chat/completions"

    def ask(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "surf-ask",
            "stream": False,
            "reasoning_effort": "medium",
            "ability": [
                "evm_onchain",
                "market_analysis",
                "calculate"
            ],
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        r = requests.post(
            self.url,
            headers=headers,
            json=payload,
            timeout=60
        )
        r.raise_for_status()
        data = r.json()

        try:
            return data["choices"][0]["message"]["content"]
        except Exception:
            return str(data)