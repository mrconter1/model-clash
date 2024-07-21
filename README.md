# ModelClash: Dynamic LLM Evaluation Arena

ModelClash is a framework for evaluating and comparing Large Language Models (LLMs) in a dynamic, competitive environment. It pits AI models against each other in creative problem-solving challenges, offering an adaptive approach to benchmarking that evolves with AI advancements.

## 🚀 Key Features

- **Self-Generating Challenges**: Models create and solve complex problems in real-time.
- **Adaptive Difficulty**: Automatically scales to match any level of AI intelligence.
- **Comprehensive Evaluation**: Tests a broad spectrum of skills including creativity, strategy, and problem-solving.

## 🎮 How ModelClash Works

### Round Structure

1. **Challenge Creation**: One model creates a programming challenge with test cases.
2. **Challenge Solving**: Both models attempt to solve the challenge.

Models alternate roles, ensuring fair evaluation.

### Scoring System

- Creator solves, opponent fails: Creator +3 points
- Both solve: Creator +1 point, Opponent +2 points
- Creator fails, opponent solves: Creator -1 point, Opponent +3 points

This system encourages creating challenges that are difficult yet solvable.

## 🏆 Advantages over Traditional Benchmarks

Compared to benchmarks like MMLU, GPQA, HumanEval, or LMSYS Chatbot Arena, ModelClash offers:

1. **Dynamic Content**: Generates new challenges in real-time, preventing memorization.
2. **Comprehensive Evaluation**: Tests both problem creation and solving abilities.
3. **Adaptive Difficulty**: Scales with model capabilities, ensuring long-term relevance.
4. **Reduced Human Bias**: AI-driven challenge creation and evaluation.
5. **Diverse Skill Coverage**: Encourages a wide range of problem types.
6. **Competitive Format**: Provides engaging, insightful head-to-head comparisons.

## 📊 Example Results

| Player A                   | Player B                   | A's Score | B's Score | Rounds Played |
|----------------------------|----------------------------|-----------|-----------|---------------|
| claude-3-5-sonnet-20240620 | gpt-3.5-turbo              | 8         | 6         | 11            |
| claude-3-5-sonnet-20240620 | gpt-4o                     | 4         | 7         | 8             |
| gpt-3.5-turbo              | gpt-4o                     | 6         | 13        | 12            |
| gpt-4o-mini                | gpt-4o                     | 9         | 10        | 9             |

## 🛠 Getting Started

### Prerequisites

- Python 3.9+
- API keys for OpenAI, Google, and Anthropic (as needed)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/mrconter1/ModelClash.git
   cd ModelClash
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up API key environment variables:
   ```
   export OPENAI_API_KEY='your-openai-api-key'
   export GOOGLE_API_KEY='your-google-api-key'
   export ANTHROPIC_API_KEY='your-anthropic-api-key'
   ```

### Usage

Run the main script:

```
python -m modelclash.main
```

## 📊 Example Challenges

1. Character Sorting and Deduplication
```python
assert X("banana") == "abn"
assert X("apple") == "aelp"
assert X("racecar") == "acer"
```

2. Morse Code Converter
```python
assert X("SOS") == "... --- ..."
assert X("HELLO") == ".... . .-.. .-.. ---"
assert X("123") == ".---- ..--- ...--"
```

## 🤝 Contributing

Contributions are welcome! Please fork the project, create a feature branch, and open a pull request.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📬 Contact

Rasmus Lindahl - rasmus.lindahl1996@gmail.com

Project Link: [https://github.com/mrconter1/ModelClash](https://github.com/mrconter1/ModelClash)

---

<p align="center">Made with ❤️ for the advancement of AI</p>