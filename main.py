import os
import re
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def send_prompt_to_gpt(prompt, model="gpt-3.5-turbo"):
    try:
        chat_completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def extract_code_from_response(response):
    pattern = r'\[Start of final answer\](.*?)\[End of final answer\]'
    match = re.search(pattern, response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return "No code found between [Start of final answer] and [End of final answer]"

def clean_and_format_code(extracted_code):
    # Split the code into lines
    code_lines = extracted_code.split('\n')
    
    # Format assert statements
    formatted_lines = ['def test_X():']
    visible_tests_started = False
    for line in code_lines:
        if '# Visible test cases' in line:
            visible_tests_started = True
            continue
        if '# Hidden test cases' in line:
            break
        if visible_tests_started and 'assert' in line:
            line = line.strip()
            line = re.sub(r'assert\s+\w+', 'assert X', line)
            # Remove trailing comments
            line = re.sub(r'\s*#.*$', '', line)
            formatted_lines.append(f'    {line}')
    
    return '\n'.join(formatted_lines)

def play_game(model1, model2, rounds):
    scores = {model1: 0, model2: 0}
    
    for round in range(1, rounds + 1):
        print(f"\nRound {round}")
        for player, opponent in [(model1, model2), (model2, model1)]:
            print(f"\n{player} is creating the function:")
            response = send_prompt_to_gpt(prompt, model=player)
            extracted_code = extract_code_from_response(response)
            formatted_code = clean_and_format_code(extracted_code)
            print(formatted_code)
            
            print(f"\n{opponent} is implementing the function:")
            implementation_prompt = f"Implement the function X based on these test cases:\n\n{formatted_code}"
            implementation = send_prompt_to_gpt(implementation_prompt, model=opponent)
            print(implementation)
            
            # Here you would actually test the implementation
            # For simplicity, we'll randomly decide if it passes or fails
            import random
            passes = random.choice([True, False])
            
            if passes:
                print(f"{opponent} succeeded in implementing the function.")
                scores[opponent] += 1
            else:
                print(f"{opponent} failed to implement the function correctly.")
                scores[player] += 2
        
        print(f"\nCurrent scores: {scores}")
    
    print("\nFinal scores:")
    print(scores)
    winner = max(scores, key=scores.get)
    print(f"The winner is: {winner}")

# The full original prompt
prompt = """**Your Task:**
Design a function X of ANY type and write unit tests for it. You will play multiple rounds of this with alternating roles. Your context memory will be reset before each round, answering and test case generation. The primary goal is to create a function that your opponent fails to implement correctly, while ensuring you can solve it yourself later even without any memory of this stage.
**Key Points:**
- The function can be of ANY type: mathematical, string processing, list manipulation, data transformation, algorithm implementation, etc.
- You can incorporate specialized knowledge from any field (e.g., physics, chemistry, linguistics, economics) as long as it's not personal or private information.
- The function should be challenging enough to make your opponent fail, but not so complex that you risk failing yourself.
**Scoring System:**
- If both succeed: You get 0, Opponent gets +1
- If both fail: You get -1, Opponent gets -1
- If you succeed and the opponent fails: You get +2, Opponent gets 0
- If you fail and the opponent succeeds: You get -2, Opponent gets +2
**Instructions:**
1. Design a function X of any type that your opponent would find difficult to implement correctly.
2. Provide a thorough explanation of how X works before implementation.
3. Ensure you fully understand how to implement the function before finalizing the tests (even in the future when you have no memory of this event)
4. Create enough test cases to make it possible to infer the function X. Also include enough hidden ones to verify the opponents implementation is valid.
**Expected (exact) format:**
[Start of final answer]
def test_X():
    # Visible test cases
    assert X(inputX) == expected_outputX
    assert X(inputX) == expected_outputX
    # ... more visible test cases
    
    # Hidden test cases
    assert X(inputX) == expected_outputX
    assert X(inputX) == expected_outputX
    # ... more invisible test cases
[End of final answer]"""

# Choose models and number of rounds
model1 = "gpt-4-turbo"
model2 = "gpt-4o"
num_rounds = 5

# Play the game
play_game(model1, model2, num_rounds)