def create_challenge_prompt():
    return """You are participating in an AI challenge tournament that tests problem-solving across various domains.
Your task is to design a challenging problem that can be solved by implementing a function.
This problem will evaluate both your ability to create intricate challenges and to solve complex tasks.

Tournament Structure:
1. You will create a problem with test cases.
2. Later, without any memory of creating it, you will attempt to solve this problem.
3. If you fail to solve your own problem, the round ends and you move to the next round without points.
4. If you succeed, other AI models will attempt to solve your problem.
5. Points are awarded as follows:
   - You get 1 point for solving your own problem.
   - You get 1 point for each opponent that fails to solve your problem.
   - Any opponent gets 1 point for solving your problem.

Important Rules:
- If your problem can't be parsed or executed, the round ends and you move to the next round without points.
- You have no memory between creating and solving stages, so ensure the problem is solvable by you without prior knowledge.
- Failing to solve your own problem doesn't result in negative points, but you miss the opportunity to score.

Your Task:
Design a programming problem that requires implementing a function named 'X'. 

Guidelines:
- The function can be of ANY type: mathematical, string processing, list manipulation, data transformation, algorithm implementation, etc.
- You can incorporate specialized knowledge from any field (e.g., physics, chemistry, linguistics, economics) as long as it's not personal or private information.
- The function should be challenging enough to potentially make your opponents fail, but not so complex that you risk failing to solve it yourself.
- Include enough test cases to both now that it is solvable and that it actually verifies that the solution is correct.

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
[End of code]

Remember, balance difficulty with solvability. You need to solve this later without any memory of creating it, while also challenging your opponents. If you can't solve it yourself, you won't get any points, so make sure it's within your capabilities."""

def create_implementation_prompt(formatted_code):
    return f"""Based on the following test cases, figure out what the function X does and implement it. Write your implementation between [Start of code] and [End of code] tags.

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