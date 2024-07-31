from game_logic import run_tournament
from model import Model
import logging
import asyncio
import warnings

logging.basicConfig(filename='output.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

warnings.filterwarnings("ignore", message="Event loop is closed")

# Define the model list here
MODELS = [
    "google/gemini-pro-1.5",
    "anthropic/claude-3-opus",
    "anthropic/claude-3.5-sonnet",
    "openai/gpt-3.5-turbo",
    "openai/gpt-4-turbo",
    "openai/gpt-4o",
    "openai/gpt-4o-mini",
    "meta-llama/llama-3.1-8b-instruct",
    "meta-llama/llama-3.1-70b-instruct",
    "meta-llama/llama-3.1-405b-instruct",
    "mistralai/mistral-large"
]

async def main():
    models = [Model(model_name) for model_name in MODELS]
    rounds_per_model = 50
    await run_tournament(models, rounds_per_model)

if __name__ == "__main__":
    asyncio.run(main())