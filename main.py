import os
import re
import asyncio
from openai import AsyncOpenAI
import google.generativeai as genai
import anthropic

# OpenAI setup
openai_api_key = os.getenv('OPENAI_API_KEY')
openai_client = AsyncOpenAI(api_key=openai_api_key)

# Google setup
google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)

# Anthropic setup
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)

async def send_prompt_to_model(prompt, model):
    try:
        if model["provider"] == "openai":
            chat_completion = await openai_client.chat.completions.create(
                model=model["name"],
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return chat_completion.choices[0].message.content
        elif model["provider"] == "google":
            google_model = genai.GenerativeModel(model["name"])
            response = google_model.generate_content(prompt)
            return response.text
        elif model["provider"] == "anthropic":
            response = anthropic_client.messages.create(
                model=model["name"],
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def extract_code_from_response(response):
    pattern = r'\[Start of code\](.*?)\[End of code\]'
    match = re.search(pattern, response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return "No code found between [Start of code] and [End of code]"

def extract_test_cases(extracted_code):
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

def create_implementation_prompt(formatted_code):
    prompt = f"""Based on the following test cases, figure out what the function X does and implement it. Write your implementation between [Start of code] and [End of code] tags.

Test cases:
{formatted_code}

Your task:
1. Analyze the test cases carefully.
2. Determine the purpose and behavior of function X.
3. Implement function X to pass all the given test cases.
4. Write your implementation between the [Start of code] and [End of code] tags.
5. There are also hidden test cases that you will need to pass as well.
6. Only the function X (should be named X) should be present inside the tags.

Please provide your implementation below:

[Start of code]
# Your implementation of function X goes here
[End of code]
"""
    return prompt

def run_tests(implementation_code, visible_tests, hidden_tests):
    try:
        exec(implementation_code, globals())
    except Exception:
        return False

    for test in visible_tests + hidden_tests:
        try:
            exec(test)
        except:
            return False
    
    if 'X' in globals():
        del globals()['X']
    
    return True

async def play_game(model1, model2, rounds):
    scores = {model1["name"]: 0, model2["name"]: 0}
    
    for round in range(1, rounds + 1):
        print(f"\nRound {round}")
        for creator, opponent in [(model1, model2), (model2, model1)]:
            print(f"{creator['name']} challenge:")
            challenge_response = await send_prompt_to_model(prompt, creator)
            visible_tests, hidden_tests = extract_test_cases(challenge_response)
            
            creator_implementation = await send_prompt_to_model(create_implementation_prompt('\n'.join(visible_tests)), creator)
            opponent_implementation = await send_prompt_to_model(create_implementation_prompt('\n'.join(visible_tests)), opponent)
            
            creator_success = run_tests(extract_code_from_response(creator_implementation), visible_tests, hidden_tests)
            opponent_success = run_tests(extract_code_from_response(opponent_implementation), visible_tests, hidden_tests)
            
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
                print(f"  Both: 0")
        
        print(f"Scores: {scores}")
    
    print("\nFinal Scores:")
    print(scores)
    winner = max(scores, key=scores.get)
    print(f"Winner: {winner}")

# The full original prompt
prompt = """**Your Task:**
Design a function X of ANY type and write unit tests for it. You will play multiple rounds of this with alternating roles. Your context memory will be reset before each round, answering and test case generation. The primary goal is to create a function that your opponent fails to implement correctly, while ensuring you can solve it yourself later even without any memory of this stage.
**Key Points:**
- The function can be of ANY type: mathematical, string processing, list manipulation, data transformation, algorithm implementation, etc.
- You can incorporate specialized knowledge from any field (e.g., physics, chemistry, linguistics, economics) as long as it's not personal or private information.
- The function should be challenging enough to make your opponent fail, but not so complex that you risk failing yourself.
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

# Define models
model1 = {"name": "gpt-4o", "provider": "openai"}
model2 = {"name": "gpt-4o-mini", "provider": "openai"}

# Number of rounds
num_rounds = 25

# Run the game
asyncio.run(play_game(model1, model2, num_rounds))