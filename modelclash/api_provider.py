from openai import AsyncOpenAI
from aiolimiter import AsyncLimiter
import asyncio
import os
import logging
import sys

logging.basicConfig(filename='output.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OpenRouterProvider:
    _instance = None
    _lock = asyncio.Lock()
    _rate_limiter = AsyncLimiter(1, 1)  # 1 request per 1 second

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenRouterProvider, cls).__new__(cls)
            cls._instance.client = AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv('OPENROUTER_API_KEY')
            )
        return cls._instance

    async def send_prompt(self, prompt: str, model: str) -> str:
        async with self._rate_limiter:
            try:
                response = await self.client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # Check if the status code is available in the response
                status_code = getattr(response, 'status_code', None)
                if status_code is not None and status_code != 200:
                    error_message = f"Error: Received status code {status_code} for model {model}"
                    print(error_message, file=sys.stderr)
                    logging.error(error_message)
                    return f"An error occurred: {error_message}"
                
                return response.choices[0].message.content
            except Exception as e:
                error_message = f"Error in API call to {model}: {str(e)}"
                print(error_message, file=sys.stderr)
                logging.error(error_message)
                return f"An error occurred: {str(e)}"

    @staticmethod
    def log_http_request(method, url, status):
        log_message = f"HTTP Request: {method} {url} {status}"
        print(log_message)
        logging.info(log_message)