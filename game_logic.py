from models import send_prompt_to_model
from utils import extract_test_cases, run_tests, extract_code_from_response
from prompts import create_implementation_prompt

def play_game(model1, model2, rounds, challenge_prompt):
    scores = {model1["name"]: 0, model2["name"]: 0}
    
    for round in range(1, rounds + 1):
        print(f"\nRound {round}")
        for creator, opponent in [(model1, model2), (model2, model1)]:
            print(f"{creator['name']} challenge:")
            challenge_response = send_prompt_to_model(challenge_prompt, creator)
            visible_tests, hidden_tests = extract_test_cases(challenge_response)
            
            implementation_prompt = create_implementation_prompt('\n'.join(visible_tests))
            creator_implementation = send_prompt_to_model(implementation_prompt, creator)
            opponent_implementation = send_prompt_to_model(implementation_prompt, opponent)
            
            creator_success = run_tests(extract_code_from_response(creator_implementation), visible_tests, hidden_tests)
            opponent_success = run_tests(extract_code_from_response(opponent_implementation), visible_tests, hidden_tests)
            
            update_scores(scores, creator, opponent, creator_success, opponent_success)
        
        print(f"Scores: {scores}")
    
    print("\nFinal Scores:")
    print(scores)
    winner = max(scores, key=scores.get)
    print(f"Winner: {winner}")

def update_scores(scores, creator, opponent, creator_success, opponent_success):
    if creator_success and not opponent_success:
        scores[creator["name"]] += 3
        print(f"  {creator['name']}: +3, {opponent['name']}: 0")
    elif creator_success and opponent_success:
        scores[creator["name"]] += 1
        scores[opponent["name"]] += 2
        print(f"  {creator['name']}: +1, {opponent['name']}: +2")
    elif not creator_success and opponent_success:
        scores[creator["name"]] -= 1
        scores[opponent["name"]] += 3
        print(f"  {creator['name']}: -1, {opponent['name']}: +3")
    else:
        print(f"  Both failed: 0")