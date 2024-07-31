# ModelClash: Dynamic LLM Evaluation Tournament

`ModelClash` is a framework for evaluating and comparing Large Language Models (LLMs) in a dynamic, competitive tournament environment. It challenges AI models to create and solve a wide variety of problems across different domains, offering an adaptive approach to benchmarking that evolves with AI advancements.

## How ModelClash Works

### Tournament Structure

The tournament consists of a configurable number of rounds per participating model. 
Each model's final score is the sum of points earned across all rounds.

### Round Gameplay

1. **Challenge Creation**: Creates any type of challenge by creating test cases that it knows it could solve by figuring out and implementing a function X.
2. **Self-Solving**: The creator, with no memory of the creation process, tries to solve its own challenge.
3. **Opponent Solving**: If the creator succeeds, other models attempt the challenge.

This process is repeated for a predetermined number of rounds for each model, ensuring every participant gets an equal number of opportunities to create challenges.

### Round Scoring

If model fails to create a parsable problem or solve its own challenge, the round ends.

In case of a valid challenge:
- For successful self-solve: Creator gains 1 point
- For each stumped opponent: Creator gains 1 point
- For each successful opponent: Opponent gains 1 point

## Results

Results after 10 rounds per model:

| Model                   | Score |
|-------------------------|-------|
| claude-3.5-sonnet       | 29    |
| gpt-4o                  | 26    |
| gemini-pro-1.5          | 23    |
| claude-3-opus           | 21    |
| gpt-4-turbo             | 21    |
| gpt-4o-mini             | 19    |
| llama-3.1-405b-instruct | 19    |
| gpt-3.5-turbo           | 18    |
| llama-3.1-70b-instruct  | 16    |
| llama-3.1-8b-instruct   | 8     |

## 🏆 Advantages over Traditional Benchmarks

Compared to static benchmarks, ModelClash offers:

1. **Automatic Challenge Generation**: Eliminates manual creation, reducing human bias.
2. **Infinite Scalability**: Adapts to evolving model capabilities.
3. **Living Benchmark**: Real-time generation prevents memorization and data leakage.
4. **Comprehensive Evaluation**: Tests both problem creation and solving abilities.
5. **Extreme Diversity**: Covers a wide range of problem types and domains.

## 🛠 Getting Started

### Prerequisites

- Python 3.9+
- OpenRouter API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ModelClash.git
   cd ModelClash
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up API key environment variable:
   ```
   export OPENROUTER_API_KEY='your-openrouter-api-key'
   ```

### Usage

Run the main script:

```
python main.py
```

## 🤝 Contributing

Contributions are welcome! Please fork the project, create a feature branch, and open a pull request.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📬 Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/ModelClash](https://github.com/yourusername/ModelClash)

---

<p align="center">Made with ❤️ for the advancement of AI</p>