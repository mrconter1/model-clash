from aiolimiter import AsyncLimiter
from openai import AsyncOpenAI
import google.generativeai as genai
from anthropic import AsyncAnthropic

class APIProvider:
    def __init__(self, name, api_key, rate_limit, period):
        self.name = name
        self.api_key = api_key
        self.limiter = AsyncLimiter(rate_limit, period)
        self.client = self._setup_client()

    def _setup_client(self):
        if self.name == "openai":
            return AsyncOpenAI(api_key=self.api_key)
        elif self.name == "google":
            genai.configure(api_key=self.api_key)
            return genai
        elif self.name == "anthropic":
            return AsyncAnthropic(api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported provider: {self.name}")

    async def send_prompt(self, prompt, model_name):
        async with self.limiter:
            if self.name == "openai":
                chat_completion = await self.client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ]
                )
                return chat_completion.choices[0].message.content
            elif self.name == "google":
                google_model = self.client.GenerativeModel(model_name)
                response = await google_model.generate_content(prompt)
                return response.text
            elif self.name == "anthropic":
                message = await self.client.messages.create(
                    max_tokens=4096,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="claude-3-5-sonnet-20240620",
                )
                return message.content[0].text