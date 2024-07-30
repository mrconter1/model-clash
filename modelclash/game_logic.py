from api_provider import OpenRouterProvider
from utils import extract_test_cases, run_tests, extract_code_from_response
from prompts import create_implementation_prompt, create_challenge_prompt
from tabulate import tabulate
import asyncio
import logging

class TournamentState:
    def __init__(self, model_templates, total_rounds):
        self.model_templates = model_templates
        self.total_rounds = total_rounds
        self.current_round = 0
        self.lock = asyncio.Lock()
        self.pair_progress = {}  # Track progress for each pair
        self.score_table = {}
        self.rounds_played = {}
        self.model_instances = {}  # Dictionary to store all model instances

    async def update_tables(self, model1, model2, score1, score2):
        async with self.lock:
            id1, id2 = model1.unique_id, model2.unique_id
            self.model_instances[id1] = model1  # Store model instance
            self.model_instances[id2] = model2  # Store model instance
            
            if id1 not in self.score_table:
                self.score_table[id1] = {}
                self.rounds_played[id1] = {}
            if id2 not in self.score_table:
                self.score_table[id2] = {}
                self.rounds_played[id2] = {}
            
            self.score_table[id1][id2] = [score1, score2]
            self.score_table[id2][id1] = [score2, score1]
            pair_key = (min(id1, id2), max(id1, id2))
            self.pair_progress[pair_key] = self.pair_progress.get(pair_key, 0) + 1
            self.current_round = sum(self.pair_progress.values())
            
            if id2 not in self.rounds_played[id1]:
                self.rounds_played[id1][id2] = 0
            if id1 not in self.rounds_played[id2]:
                self.rounds_played[id2][id1] = 0
            
            self.rounds_played[id1][id2] += 1
            self.rounds_played[id2][id1] += 1
            await self.print_results_table()

    async def print_results_table(self):
        await asyncio.to_thread(print_results_table, self.model_instances, self.score_table, self.rounds_played, self.current_round, self.total_rounds)

async def run_tournament(models, rounds_per_pair):
    challenge_prompt = create_challenge_prompt()
    num_models = len(models)
    total_rounds = sum(range(num_models + 1)) * rounds_per_pair
    state = TournamentState(models, total_rounds)

    logging.info(f"Starting tournament with {num_models} models, {rounds_per_pair} rounds per pair, total {total_rounds} rounds")

    tasks = []
    for i in range(num_models):
        for j in range(i, num_models):
            model1 = models[i].new_instance()
            model2 = models[j].new_instance()
            task = asyncio.create_task(run_game(model1, model2, rounds_per_pair, challenge_prompt, state))
            tasks.append(task)

    chunk_size = 10
    for i in range(0, len(tasks), chunk_size):
        chunk = tasks[i:i+chunk_size]
        await asyncio.gather(*chunk)

async def run_game(model1, model2, rounds, challenge_prompt, state):
    model1_id = model1.unique_id
    model2_id = model2.unique_id
    scores = {model1_id: 1, model2_id: 1}
    provider = OpenRouterProvider()
    
    for round_num in range(rounds):
        for creator, opponent in [(model1, model2), (model2, model1)]:
            creator_id = creator.unique_id
            opponent_id = opponent.unique_id
            
            try:
                challenge_response = await provider.send_prompt(challenge_prompt, creator.name)
                logging.info(f"Challenge response from {creator.name} ({creator_id}): {challenge_response[:250]}...")
                
                visible_tests, hidden_tests = extract_test_cases(challenge_response)
                if not visible_tests or not hidden_tests:
                    logging.error(f"Failed to extract test cases for {creator.name} ({creator_id})")
                    continue
                
                implementation_prompt = create_implementation_prompt('\n'.join(visible_tests))
                creator_implementation = extract_code_from_response(await provider.send_prompt(implementation_prompt, creator.name))
                opponent_implementation = extract_code_from_response(await provider.send_prompt(implementation_prompt, opponent.name))
                
                logging.info(f"Creator ({creator.name} {creator_id}) implementation: {creator_implementation[:100]}...")
                logging.info(f"Opponent ({opponent.name} {opponent_id}) implementation: {opponent_implementation[:100]}...")

                creator_success = run_tests(creator_implementation, visible_tests, hidden_tests)
                opponent_success = run_tests(opponent_implementation, visible_tests, hidden_tests)
                
                logging.info(f"Creator success: {creator_success}, Opponent success: {opponent_success}")
                
                update_scores(scores, creator_id, opponent_id, creator_success, opponent_success)
            except Exception as e:
                logging.error(f"Error in round {round_num} for {creator.name} ({creator_id}) vs {opponent.name} ({opponent_id}): {str(e)}")

        await state.update_tables(model1, model2, scores[model1_id], scores[model2_id])

def update_scores(scores, creator_id, opponent_id, creator_success, opponent_success):
    if creator_success and not opponent_success:
        scores[creator_id] += 3
    elif creator_success and opponent_success:
        scores[creator_id] += 1
        scores[opponent_id] += 2
    elif not creator_success and opponent_success:
        scores[creator_id] -= 1
        scores[opponent_id] += 3

def print_results_table(model_instances, score_table, rounds_played, current_round, total_rounds):
    table_data = []
    for id1 in score_table:
        for id2 in score_table[id1]:
            if id1 < id2:  # Avoid duplicate entries
                score_i, score_j = score_table[id1][id2][0], score_table[id1][id2][1]
                rounds = rounds_played[id1][id2]
                model1 = model_instances[id1]  # Get the model instance directly
                model2 = model_instances[id2]  # Get the model instance directly
                table_data.append([
                    f"{model1.display_name}",
                    f"{model2.display_name}",
                    score_i,
                    score_j,
                    rounds
                ])

    # Sort the table_data based on the first two columns
    table_data.sort(key=lambda x: (x[0].lower(), x[1].lower()))
    
    headers = ["Player A", "Player B", "A's Score", "B's Score", "Rounds Played"]

    print(f"\nRound {current_round}/{total_rounds}")
    logging.info(f"\nRound {current_round}/{total_rounds}")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    logging.info(tabulate(table_data, headers=headers, tablefmt="grid"))