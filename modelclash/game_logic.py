from api_provider import OpenRouterProvider
from utils import extract_test_cases, run_tests, extract_code_from_response
from prompts import create_implementation_prompt, create_challenge_prompt
from tabulate import tabulate
import asyncio
import logging

class TournamentState:
    def __init__(self, models, total_rounds):
        self.models = models
        self.total_rounds = total_rounds
        self.scores = {model.unique_id: 0 for model in models}
        self.current_round = 0
        self.lock = asyncio.Lock()

    async def update_score(self, model_id, points):
        async with self.lock:
            self.scores[model_id] += points
            self.current_round += 1
            await self.print_results_table()

    async def print_results_table(self):
        await asyncio.to_thread(print_results_table, self.models, self.scores, self.current_round, self.total_rounds)

async def run_tournament(models, rounds_per_model):
    total_rounds = len(models) * rounds_per_model
    state = TournamentState(models, total_rounds)
    provider = OpenRouterProvider()

    tasks = []
    for model in models:
        for _ in range(rounds_per_model):
            task = asyncio.create_task(run_round(model, models, provider, state))
            tasks.append(task)

    await asyncio.gather(*tasks)

async def run_round(creator_model, all_models, provider, state):
    challenge_prompt = create_challenge_prompt()
    challenge_response = await provider.send_prompt(challenge_prompt, creator_model.name)
    
    visible_tests, hidden_tests = extract_test_cases(challenge_response)
    if not visible_tests or not hidden_tests:
        logging.error(f"Failed to extract test cases for {creator_model.name}")
        return

    implementation_prompt = create_implementation_prompt('\n'.join(visible_tests))
    
    # Creator solves its own challenge
    creator_implementation = extract_code_from_response(await provider.send_prompt(implementation_prompt, creator_model.name))
    creator_success = run_tests(creator_implementation, visible_tests, hidden_tests)
    
    if not creator_success:
        return  # If creator can't solve its own challenge, round ends

    await state.update_score(creator_model.unique_id, 1)  # Point for solving own challenge

    for opponent_model in all_models:
        if opponent_model != creator_model:
            opponent_implementation = extract_code_from_response(await provider.send_prompt(implementation_prompt, opponent_model.name))
            opponent_success = run_tests(opponent_implementation, visible_tests, hidden_tests)
            
            if opponent_success:
                await state.update_score(opponent_model.unique_id, 1)  # Point for solving
            else:
                await state.update_score(creator_model.unique_id, 1)  # Point for opponent failing

def print_results_table(models, scores, current_round, total_rounds):
    table_data = [(model.display_name, scores[model.unique_id]) for model in models]
    table_data.sort(key=lambda x: x[1], reverse=True)
    
    headers = ["Model", "Score"]
    print(f"\nRound {current_round}/{total_rounds}")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))