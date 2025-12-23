import requests
from django.conf import settings

OPENAI_BASE_URL = "https://gms.ssafy.io/gmsapi/api.openai.com"

class UpstreamAIError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

def call_chat_completions(messages, model=None, timeout=30):
    api_key = getattr(settings, "GMS_KEY", "")
    if not api_key:
        raise RuntimeError("GMS_KEY is not configured")

    # 기본 모델: settings.OPENAI_MODEL 있으면 그걸 쓰고, 없으면 gpt-5-mini
    model_name = model or getattr(settings, "OPENAI_MODEL", "gpt-5-mini")

    payload = {
        "model": model_name,
        "messages": messages,
    }

    url = f"{OPENAI_BASE_URL}/v1/chat/completions"

    try:
        res = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=timeout,
        )

        if res.status_code >= 400:
            raise UpstreamAIError(res.status_code, res.text)

        return res.json()

    except requests.RequestException as e:
        raise UpstreamAIError(502, str(e))
