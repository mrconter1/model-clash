from config import get_api_providers
from model import Model

import logging


async def send_prompt_to_model(prompt, model: Model):
    providers = get_api_providers()
    try:
        if model.provider in providers:
            return await providers[model.provider].send_prompt(prompt, model.name)
        else:
            raise ValueError(f"Unsupported provider: {model.provider}")
    except Exception as e:
        logging.error(f"Error in API call to {model.provider}: {str(e)}")
        return f"An error occurred: {str(e)}"