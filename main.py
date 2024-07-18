import os
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def send_prompt_to_gpt4(prompt):
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

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
4. Create enough test cases to make it possible to infer the function X. Also include enough hidden ones to verify the opponents implementation.
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

print("Sending prompt to GPT-4o...")
response = send_prompt_to_gpt4(prompt)
print("\nResponse from GPT-4o:")
print(response)