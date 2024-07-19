from models import send_prompt_to_model
from utils import extract_test_cases, run_tests, extract_code_from_response
from prompts import create_implementation_prompt, create_challenge_prompt

import textwrap

def format_test_cases(visible_tests, hidden_tests):
    formatted = "# Visible test cases\n"
    formatted += '\n'.join(visible_tests)
    formatted += "\n"  # Add an empty line after visible test cases
    if hidden_tests:
        formatted += "\n# Hidden test cases\n"  # Add an empty line before hidden test cases
        formatted += '\n'.join(hidden_tests)
    return formatted

def run_game(model1, model2, rounds, challenge_prompt, game_number, total_games):
    model1_id = f"{model1['name']}_1"
    model2_id = f"{model2['name']}_2"
    scores = {model1_id: 0, model2_id: 0}
    
    for round_num in range(1, rounds + 1):
        print(f"\nGame {game_number} of {total_games}")
        print(f"Round {round_num} of {rounds}")
        print(f"Opponents: {model1['name']} vs {model2['name']}")
        
        for creator, opponent in [(model1, model2), (model2, model1)]:
            creator_id = model1_id if creator == model1 else model2_id
            opponent_id = model2_id if opponent == model2 else model1_id
            
            print(f"\n  {creator['name']} challenge:")
            challenge_response = send_prompt_to_model(challenge_prompt, creator)
            
            visible_tests, hidden_tests = extract_test_cases(challenge_response)
            formatted_test = format_test_cases(visible_tests, hidden_tests)
            
            print()
            print(textwrap.indent(formatted_test, '    '))
            print()  # Add an empty line after the challenge
            
            implementation_prompt = create_implementation_prompt('\n'.join(visible_tests))
            creator_implementation = extract_code_from_response(send_prompt_to_model(implementation_prompt, creator))
            opponent_implementation = extract_code_from_response(send_prompt_to_model(implementation_prompt, opponent))

            creator_success = run_tests(creator_implementation, visible_tests, hidden_tests)
            opponent_success = run_tests(opponent_implementation, visible_tests, hidden_tests)
            
            update_scores(scores, creator_id, opponent_id, creator_success, opponent_success)
            
            print(f"  Results: {creator['name']}: {'✓' if creator_success else '✗'}, {opponent['name']}: {'✓' if opponent_success else '✗'}")
            print(f"  Scores: {model1['name']}: {scores[model1_id]}, {model2['name']}: {scores[model2_id]}")

    print(f"\nFinal Scores: {model1['name']}: {scores[model1_id]}, {model2['name']}: {scores[model2_id]}")
    
    ratio = scores[model1_id] / scores[model2_id] if scores[model2_id] != 0 else float('inf')
    return ratio

def update_scores(scores, creator_id, opponent_id, creator_success, opponent_success):
    if creator_success and not opponent_success:
        scores[creator_id] += 3
    elif creator_success and opponent_success:
        scores[creator_id] += 1
        scores[opponent_id] += 2
    elif not creator_success and opponent_success:
        scores[creator_id] -= 1
        scores[opponent_id] += 3

def run_tournament(list_of_model_dicts, num_of_rounds):
    challenge_prompt = create_challenge_prompt()
    num_models = len(list_of_model_dicts)
    results_table = [["-" for _ in range(num_models)] for _ in range(num_models)]

    total_games = num_models * (num_models + 1) // 2  # Including diagonal and upper triangle
    game_count = 0

    print(f"\nStarting tournament with {num_models} models and {num_of_rounds} rounds per game.")
    print(f"Total number of games to be played: {total_games}")

    for i in range(num_models):
        for j in range(i, num_models):  # Including diagonal and upper triangle
            model1 = list_of_model_dicts[i]
            model2 = list_of_model_dicts[j]
            game_count += 1
            ratio = run_game(model1, model2, num_of_rounds, challenge_prompt, game_count, total_games)
            results_table[i][j] = ratio

            print("\nCurrent Results Table:")
            print_results_table(list_of_model_dicts, results_table)

    return results_table

def print_results_table(list_of_model_dicts, results_table):
    model_names = [model["name"] for model in list_of_model_dicts]
    
    max_name_length = max(len(name) for name in model_names)
    
    header = "Model".ljust(max_name_length + 4)
    for name in model_names:
        header += f"{name:>12}"
    print(header)
    
    for i, row in enumerate(results_table):
        print(f"{model_names[i]:<{max_name_length + 4}}", end="")
        for j, value in enumerate(row):
            if value == "-":
                print(f"{'-':>12}", end="")
            elif value == float('inf'):
                print(f"{'inf':>12}", end="")
            else:
                print(f"{value:12.2f}", end="")
        print()