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
    pattern = r'\[Start of code\](.*?)\[End of code\]'
    match = re.search(pattern, response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return "No code found between [Start of code] and [End of code]"

def clean_and_format_code(extracted_code):
    code_lines = extracted_code.split('\n')
    
    visible_tests = []
    hidden_tests = []
    current_list = visible_tests
    
    for line in code_lines:
        if '# Visible test cases' in line:
            current_list = visible_tests
            continue
        if '# Hidden test cases' in line:
            current_list = hidden_tests
            continue
        if 'assert' in line:
            line = line.strip()
            line = re.sub(r'assert\s+\w+', 'assert X', line)
            line = re.sub(r'\s*#.*$', '', line)
            current_list.append(line)

    if not visible_tests and not hidden_tests:
        print("Warning: No test cases found in extracted code.")
        print(extracted_code)
    
    return visible_tests, hidden_tests

def create_opponent_prompt(formatted_code):
    prompt = f"""Based on the following test cases, figure out what the function X does and implement it. Write your implementation between [Start of code] and [End of code] tags.

Test cases:
{formatted_code}

Your task:
1. Analyze the test cases carefully.
2. Determine the purpose and behavior of function X.
3. Implement function X to pass all the given test cases.
4. Write your implementation between the [Start of code] and [End of code] tags.
5. There are also hidden test cases that you will need to pass as well.
6. Only the X (should be named X) should be present inside the tags.

Please provide your implementation below:

[Start of code]
# Your implementation of function X goes here
[End of code]
"""
    return prompt

def play_game(model1, model2, rounds):
    scores = {model1: 0, model2: 0}
    
    for round in range(1, rounds + 1):
        print(f"\n==================== Round {round} ====================")
        for player, opponent in [(model1, model2), (model2, model1)]:
            print(f"\n---------- {player} is creating a challenge ----------")
            challenge_response = send_prompt_to_gpt(prompt, model=player)
            challenge_code = extract_code_from_response(challenge_response)
            visible_tests, hidden_tests = clean_and_format_code(challenge_code)
            implementation_prompt = create_opponent_prompt('\n'.join(visible_tests))
            print(f"Prompt for {opponent}:\n{implementation_prompt}\n")
            
            print(f"---------- {opponent} is trying to solve the challange ----------")
            implementation_response = send_prompt_to_gpt(implementation_prompt, model=opponent)
            implementation_code = extract_code_from_response(implementation_response)
            print(f"Extracted implementation code:\n{implementation_code}\n")
            
            print(f"Executing {opponent}'s implementation...")
            exec(implementation_code, globals())

            print("Running visible tests...")
            try:
                for test in visible_tests:
                    exec(test)
                print(f"{opponent} passed visible tests.")
                print("Running hidden tests...")
                try:
                    for test in hidden_tests:
                        exec(test)
                    print(f"{opponent} passed hidden tests.")
                    print(f"{opponent} succeeded in implementing the function.")
                    scores[opponent] += 1
                except AssertionError as e:
                    print(f"{opponent} failed hidden tests.")
                    print(f"AssertionError: {e}")
                    scores[player] += 2
            except AssertionError as e:
                print(f"{opponent} failed visible tests.")
                print(f"AssertionError: {e}")
                scores[player] += 2

            print("\nCleaning up global namespace...")
            if 'X' in globals():
                del globals()['X']
            print("Cleanup complete.\n")
            
            print(f"Current scores: {scores}")

            input()
        
    print("\n==================== Final Scores ====================")
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
[Start of code]
def test_X():
    # Visible test cases
    assert X(inputX) == expected_outputX
    assert X(inputX) == expected_outputX
    # ... more visible test cases
    
    # Hidden test cases
    assert X(inputX) == expected_outputX
    assert X(inputX) == expected_outputX
    # ... more invisible test cases
[End of code]"""

# Choose models and number of rounds
model1 = "gpt-4-turbo"
model2 = "gpt-4o"
num_rounds = 5

# Play the game
play_game(model1, model2, num_rounds)