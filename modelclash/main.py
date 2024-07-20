from game_logic import run_tournament, print_results_table
from config import get_api_providers
from model import Model
import asyncio

async def main():
    # Ensure API providers are initialized
    get_api_providers()

    models = [
        Model("gpt-4o", "openai"),
        Model("gpt-4o-mini", "openai"),
        Model("gpt-3.5-turbo", "openai"),
        Model("claude-3-5-sonnet-20240620", "anthropic"),
        # Add more models as needed
    ]

    num_rounds = 100
    await run_tournament(models, num_rounds)

if __name__ == "__main__":
    asyncio.run(main())