import asyncio
from model_handler import send_prompt_to_model
from utils import extract_test_cases, run_tests, extract_code_from_response
from prompts import create_implementation_prompt, create_challenge_prompt
from model import Model

async def run_tournament(models, num_of_rounds):
    challenge_prompt = create_challenge_prompt()
    num_models = len(models)
    results_table = [[1.0 for _ in range(num_models)] for _ in range(num_models)]
    score_table = [[[0, 0] for _ in range(num_models)] for _ in range(num_models)]

    tasks = []
    for i in range(num_models):
        for j in range(i, num_models):
            model1 = models[i]
            model2 = models[j]
            task = asyncio.create_task(run_game(model1, model2, num_of_rounds, challenge_prompt, results_table, score_table, i, j, models))
            tasks.append(task)

    await asyncio.gather(*tasks)
    return results_table, score_table

async def run_game(model1, model2, rounds, challenge_prompt, results_table, score_table, i, j, models):
    model1_id = f"{model1.name}_1"
    model2_id = f"{model2.name}_2"
    scores = {model1_id: 1, model2_id: 1}
    
    for round_num in range(rounds):
        for creator, opponent in [(model1, model2), (model2, model1)]:
            creator_id = model1_id if creator == model1 else model2_id
            opponent_id = model2_id if opponent == model2 else model1_id
            
            challenge_response = await send_prompt_to_model(challenge_prompt, creator)
            visible_tests, hidden_tests = extract_test_cases(challenge_response)
            
            if not visible_tests and not hidden_tests:
                continue
            
            implementation_prompt = create_implementation_prompt('\n'.join(visible_tests))
            creator_implementation = extract_code_from_response(await send_prompt_to_model(implementation_prompt, creator))
            opponent_implementation = extract_code_from_response(await send_prompt_to_model(implementation_prompt, opponent))

            creator_success = run_tests(creator_implementation, visible_tests, hidden_tests)
            opponent_success = run_tests(opponent_implementation, visible_tests, hidden_tests)
            
            update_scores(scores, creator_id, opponent_id, creator_success, opponent_success)

        ratio = scores[model1_id] / scores[model2_id] if scores[model2_id] != 0 else float('inf')
        results_table[i][j] = ratio
        if i != j:
            results_table[j][i] = 1 / ratio
        
        score_table[i][j] = [scores[model1_id], scores[model2_id]]
        if i != j:
            score_table[j][i] = [scores[model2_id], scores[model1_id]]

        # Print results table after each complete round
        await asyncio.to_thread(print_results_table, models, results_table, score_table, round_num + 1)

def update_scores(scores, creator_id, opponent_id, creator_success, opponent_success):
    if creator_success and not opponent_success:
        scores[creator_id] += 3
    elif creator_success and opponent_success:
        scores[creator_id] += 1
        scores[opponent_id] += 2
    elif not creator_success and opponent_success:
        scores[creator_id] -= 1
        scores[opponent_id] += 3

def print_results_table(models, results_table, score_table, round_num):
    model_names = [model.name for model in models]
    
    max_name_length = max(len(name) for name in model_names)
    
    print(f"\nAfter Round {round_num}:")
    header = "Model".ljust(max_name_length + 4)
    for name in model_names:
        header += f"{name:>24}"
    print(header)
    
    for i, row in enumerate(results_table):
        print(f"{model_names[i]:<{max_name_length + 4}}", end="")
        for j in range(len(row)):
            if j < i:
                print(f"{' ':>24}", end="")
            else:
                ratio = row[j]
                score = score_table[i][j]
                if ratio == float('inf'):
                    ratio_str = 'inf'
                else:
                    ratio_str = f"{ratio:.2f}"
                print(f"{ratio_str:>10} ({score[0]:>3}-{score[1]:<3})", end="")
        print()
    print("\n" + "="*50 + "\n")