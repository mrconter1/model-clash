from utils import extract_test_cases, run_tests, extract_code_from_response
from prompts import create_implementation_prompt, create_challenge_prompt
from model_handler import send_prompt_to_model
from tabulate import tabulate
import asyncio

class TournamentState:
    def __init__(self, num_models, total_rounds):
        self.results_table = [[1.0 for _ in range(num_models)] for _ in range(num_models)]
        self.score_table = [[[0, 0] for _ in range(num_models)] for _ in range(num_models)]
        self.total_rounds = total_rounds
        self.current_round = 0
        self.lock = asyncio.Lock()
        self.pair_progress = {}  # Track progress for each pair
        self.models = None  # Will be set in run_tournament

    async def update_tables(self, i, j, ratio, score1, score2):
        async with self.lock:
            self.results_table[i][j] = ratio
            if i != j:
                self.results_table[j][i] = 1 / ratio
            self.score_table[i][j] = [score1, score2]
            if i != j:
                self.score_table[j][i] = [score2, score1]
            pair_key = (min(i, j), max(i, j))
            self.pair_progress[pair_key] = self.pair_progress.get(pair_key, 0) + 1
            self.current_round = sum(self.pair_progress.values())
            await self.print_results_table()

    async def print_results_table(self):
        await asyncio.to_thread(print_results_table, self.models, self.results_table, self.score_table, self.current_round, self.total_rounds)

async def run_tournament(models, rounds_per_pair):
    challenge_prompt = create_challenge_prompt()
    num_models = len(models)
    total_rounds = sum(range(num_models + 1)) * rounds_per_pair
    state = TournamentState(num_models, total_rounds)
    state.models = models

    print(f"Starting tournament with {num_models} models, {rounds_per_pair} rounds per pair, total {total_rounds} rounds")

    tasks = []
    for i in range(num_models):
        for j in range(i, num_models):
            model1 = models[i]
            model2 = models[j]
            task = asyncio.create_task(run_game(model1, model2, rounds_per_pair, challenge_prompt, state, i, j))
            tasks.append(task)

    await asyncio.gather(*tasks)
    return state.results_table, state.score_table

async def run_game(model1, model2, rounds, challenge_prompt, state, i, j):
    model1_id = f"{model1.name}_1"
    model2_id = f"{model2.name}_2"
    scores = {model1_id: 1, model2_id: 1}
    
    for round_num in range(rounds):
        for creator, opponent in [(model1, model2), (model2, model1)]:
            creator_id = model1_id if creator == model1 else model2_id
            opponent_id = model2_id if opponent == model2 else model1_id
            
            challenge_response = await send_prompt_to_model(challenge_prompt, creator)
            visible_tests, hidden_tests = extract_test_cases(challenge_response)
            
            implementation_prompt = create_implementation_prompt('\n'.join(visible_tests))
            creator_implementation = extract_code_from_response(await send_prompt_to_model(implementation_prompt, creator))
            opponent_implementation = extract_code_from_response(await send_prompt_to_model(implementation_prompt, opponent))

            creator_success = run_tests(creator_implementation, visible_tests, hidden_tests)
            opponent_success = run_tests(opponent_implementation, visible_tests, hidden_tests)
            
            update_scores(scores, creator_id, opponent_id, creator_success, opponent_success)

        ratio = scores[model1_id] / scores[model2_id] if scores[model2_id] != 0 else float('inf')
        await state.update_tables(i, j, ratio, scores[model1_id], scores[model2_id])

def update_scores(scores, creator_id, opponent_id, creator_success, opponent_success):
    if creator_success and not opponent_success:
        scores[creator_id] += 3
    elif creator_success and opponent_success:
        scores[creator_id] += 1
        scores[opponent_id] += 2
    elif not creator_success and opponent_success:
        scores[creator_id] -= 1
        scores[opponent_id] += 3

def calculate_ratio(score_a, score_b):
    min_score = min(score_a, score_b)
    offset = abs(min_score) + 1 if min_score < 0 else 1
    adjusted_a = score_a + offset
    adjusted_b = score_b + offset
    return adjusted_a / adjusted_b

def print_results_table(models, results_table, score_table, current_round, total_rounds):
    model_names = [model.name for model in models]
    
    table_data = []
    for i, row in enumerate(results_table):
        table_row = [model_names[i]]
        for j in range(len(row)):
            if i == j:
                table_row.append(f"{1.00:.2f}")
            else:
                score_i, score_j = score_table[i][j][0], score_table[i][j][1]
                ratio = calculate_ratio(score_i, score_j)
                table_row.append(f"{ratio:.2f}")
        table_data.append(table_row)
    
    headers = ["Model"] + model_names
    print(f"\nRound {current_round}/{total_rounds}")
    print(tabulate(table_data, headers=headers, tablefmt="grid", floatfmt=".2f"))