from models import send_prompt_to_model
from utils import extract_test_cases, run_tests, extract_code_from_response
from prompts import create_implementation_prompt, create_challenge_prompt

def run_game(model1, model2, rounds, challenge_prompt):
    scores = {model1["name"]: 0, model2["name"]: 0}
    
    for _ in range(rounds):
        for creator, opponent in [(model1, model2), (model2, model1)]:
            challenge_response = send_prompt_to_model(challenge_prompt, creator)
            visible_tests, hidden_tests = extract_test_cases(challenge_response)
            
            implementation_prompt = create_implementation_prompt('\n'.join(visible_tests))
            creator_implementation = send_prompt_to_model(implementation_prompt, creator)
            opponent_implementation = send_prompt_to_model(implementation_prompt, opponent)
            
            creator_success = run_tests(extract_code_from_response(creator_implementation), visible_tests, hidden_tests)
            opponent_success = run_tests(extract_code_from_response(opponent_implementation), visible_tests, hidden_tests)
            
            update_scores(scores, creator, opponent, creator_success, opponent_success)

    total_games = rounds * 2
    ratio = scores[model1["name"]] / total_games
    return ratio

def update_scores(scores, creator, opponent, creator_success, opponent_success):
    if creator_success and not opponent_success:
        scores[creator["name"]] += 3
    elif creator_success and opponent_success:
        scores[creator["name"]] += 1
        scores[opponent["name"]] += 2
    elif not creator_success and opponent_success:
        scores[creator["name"]] -= 1
        scores[opponent["name"]] += 3

def run_tournament(list_of_model_dicts, num_of_rounds):
    challenge_prompt = create_challenge_prompt()
    num_models = len(list_of_model_dicts)
    results_table = [[0 for _ in range(num_models)] for _ in range(num_models)]

    for i in range(num_models):
        for j in range(i + 1, num_models):
            model1 = list_of_model_dicts[i]
            model2 = list_of_model_dicts[j]
            ratio = run_game(model1, model2, num_of_rounds, challenge_prompt)
            results_table[i][j] = ratio
            results_table[j][i] = 1 - ratio

    return results_table

def print_results_table(list_of_model_dicts, results_table):
    model_names = [model["name"] for model in list_of_model_dicts]
    
    # Print header
    print("Model\t" + "\t".join(model_names))
    
    # Print data rows
    for i, row in enumerate(results_table):
        print(f"{model_names[i]}", end="")
        for value in row:
            print(f"\t{value:.2f}", end="")
        print()  # New line after each row
