from api_provider import OpenRouterProvider
from utils import extract_test_cases, run_tests, extract_code_from_response
from prompts import create_implementation_prompt, create_challenge_prompt
from tabulate import tabulate
import asyncio
import logging

class TournamentState:
    def __init__(self, models, rounds_per_model):
        self.models = models
        self.rounds_per_model = rounds_per_model
        self.scores = {model.unique_id: 0 for model in models}
        self.completed_rounds = {model.unique_id: 0 for model in models}
        self.lock = asyncio.Lock()

    async def update_score(self, model_id, points):
        async with self.lock:
            self.scores[model_id] += points

    async def increment_completed_round(self, model_id):
        async with self.lock:
            self.completed_rounds[model_id] += 1

    async def print_results_table(self):
        await asyncio.to_thread(print_results_table, self.models, self.scores, self.completed_rounds, self.rounds_per_model)

async def run_tournament(models, rounds_per_model):
    state = TournamentState(models, rounds_per_model)
    provider = OpenRouterProvider()

    for round_num in range(1, rounds_per_model + 1):
        logging.info(f"\n--- Starting Round {round_num} ---")
        tasks = []
        for model in models:
            task = asyncio.create_task(run_round(model, models, provider, state, round_num))
            tasks.append(task)
        await asyncio.gather(*tasks)
        await state.print_results_table()

async def run_round(creator_model, all_models, provider, state, round_num):
    logging.info(f"\nRound {round_num}: {creator_model.display_name} is creating a challenge")
    challenge_prompt = create_challenge_prompt()
    challenge_response = await provider.send_prompt(challenge_prompt, creator_model.name)
    
    visible_tests, hidden_tests = extract_test_cases(challenge_response)
    if not visible_tests or not hidden_tests:
        logging.error(f"Round {round_num}: {creator_model.display_name} failed to create a valid challenge (couldn't parse challenge)")
        await state.increment_completed_round(creator_model.unique_id)
        return

    logging.info(f"Round {round_num}: Challenge created by {creator_model.display_name}")
    logging.info("Visible tests:\n" + "\n".join(visible_tests))
    logging.info("Hidden tests:\n" + "\n".join(hidden_tests))

    implementation_prompt = create_implementation_prompt('\n'.join(visible_tests))
    
    # Creator solves its own challenge
    logging.info(f"Round {round_num}: {creator_model.display_name} is attempting to solve its own challenge")
    creator_implementation = extract_code_from_response(await provider.send_prompt(implementation_prompt, creator_model.name))
    creator_success = run_tests(creator_implementation, visible_tests, hidden_tests)
    
    if not creator_success:
        logging.error(f"Round {round_num}: {creator_model.display_name} failed to solve its own challenge")
        await state.increment_completed_round(creator_model.unique_id)
        return

    logging.info(f"Round {round_num}: {creator_model.display_name} successfully solved its own challenge")
    logging.info(f"Solution by {creator_model.display_name}:\n{creator_implementation}")

    await state.update_score(creator_model.unique_id, 1)  # Point for solving own challenge

    opponent_tasks = []
    for opponent_model in all_models:
        if opponent_model != creator_model:
            task = asyncio.create_task(run_opponent_attempt(opponent_model, implementation_prompt, visible_tests, hidden_tests, state, creator_model, provider, round_num))
            opponent_tasks.append(task)
    
    await asyncio.gather(*opponent_tasks)

    await state.increment_completed_round(creator_model.unique_id)

async def run_opponent_attempt(opponent_model, implementation_prompt, visible_tests, hidden_tests, state, creator_model, provider, round_num):
    logging.info(f"Round {round_num}: {opponent_model.display_name} is attempting to solve {creator_model.display_name}'s challenge")
    opponent_implementation = extract_code_from_response(await provider.send_prompt(implementation_prompt, opponent_model.name))
    opponent_success = run_tests(opponent_implementation, visible_tests, hidden_tests)
    
    if opponent_success:
        logging.info(f"Round {round_num}: {opponent_model.display_name} successfully solved {creator_model.display_name}'s challenge")
        await state.update_score(opponent_model.unique_id, 1)  # Point for solving
    else:
        logging.info(f"Round {round_num}: {opponent_model.display_name} failed to solve {creator_model.display_name}'s challenge")
        await state.update_score(creator_model.unique_id, 1)

    logging.info(f"Solution attempt by {opponent_model.display_name}:\n{opponent_implementation}")

def print_results_table(models, scores, completed_rounds, rounds_per_model):
    total_models = len(models)
    total_rounds = total_models * rounds_per_model

    # Prepare the table data
    table_data = [(model.display_name, scores[model.unique_id], completed_rounds[model.unique_id]) for model in models]
    table_data.sort(key=lambda x: x[1], reverse=True)

    # Define headers and print the table
    headers = ["Model", "Score", "Completed Rounds"]
    total_completed = sum(completed_rounds.values())

    # Create the results string
    results = (
        f"\nTotal Completed Rounds: {total_completed}/{total_rounds}\n"
        f"Total Models: {total_models}\n"
        f"Rounds per Model: {rounds_per_model}\n"
        f"{tabulate(table_data, headers=headers, tablefmt='grid')}"
    )

    # Print the results string
    print(results)
    logging.info(results)