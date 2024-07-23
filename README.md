# ModelClash: Dynamic LLM Evaluation Duel

`ModelClash` is a framework for evaluating and comparing Large Language Models (LLMs) in a dynamic, competitive environment. It pits AI models against each other in creative problem-solving duels, offering an adaptive approach to benchmarking that evolves with AI advancements.

## Table of Contents
- [How ModelClash Works](#-how-modelclash-works)
- [Advantages over Traditional Benchmarks](#-top-5-advantages-over-traditional-benchmarks)
- [Results](#-results)
- [Getting Started](#-getting-started)
- [Example Challenges](#-example-challenges)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## 🎮 How ModelClash Works

### Duel Structure

1. **Challenge Creation**: A model generates a challenge consisting of N visible test cases and M hidden test cases.

2. **Challenge Solving**: Both models attempt to solve the challenge by implementing a function that passes all visible and hidden test cases.

3. **Role Switch**: Models switch roles, with the previous solver becoming the challenge creator and vice versa.

> [!NOTE]
>
> The challenge creator is explicitly informed it must later solve its own challenge without access to any memory of the creation process. It is also told that the goal is to create a challenge the opponent will fail while ensuring its own success.

### Scoring System

- Creator solves, opponent fails: Creator +3 points
- Both solve: Creator +1 point, Opponent +2 points
- Creator fails, opponent solves: Creator -1 point, Opponent +3 points

This system encourages creating challenges that are difficult yet solvable.

## 🏆 Top 5 Advantages over Traditional Benchmarks

Compared to other existing benchmark approaches such as [MMLU](https://github.com/hendrycks/test), [GPQA](https://github.com/idavidrein/gpqa), or [Chatbot Arena](https://chat.lmsys.org/), ModelClash offers:

1. **Automatic Challenge Generation**: Eliminates the need for manual challenge creation, saving time and reducing human bias.
2. **Infinite Scalability**: Adapts to any level of model capability, ensuring the benchmark remains relevant as AI technology advances.
3. **Living Benchmark**: Real-time challenge generation prevents memorization and data leakage
4. **Comprehensive Evaluation**: Tests both problem creation and solving abilities, providing a more holistic assessment.
5. **Extreme Diversity**: Can theoretically cover a large range of problem types and domains.

## 📊 Results

| Player A                   | Player B                   | A's Score | B's Score | Rounds Played |
|----------------------------|----------------------------|-----------|-----------|---------------|
| claude-3-5-sonnet-20240620 | claude-3-5-sonnet-20240620 | 48        | 43        | 50            |
| claude-3-5-sonnet-20240620 | gpt-3.5-turbo              | 74        | 48        | 69            |
| claude-3-5-sonnet-20240620 | gpt-4o                     | 39        | 39        | 52            |
| claude-3-5-sonnet-20240620 | gpt-4o-mini                | 37        | 34        | 49            |
| gpt-3.5-turbo              | gpt-3.5-turbo              | 94        | 75        | 106           |
| gpt-3.5-turbo              | gpt-4o                     | 46        | 82        | 76            |
| gpt-3.5-turbo              | gpt-4o-mini                | 54        | 71        | 64            |
| gpt-4o                     | gpt-4o                     | 30        | 30        | 55            |
| gpt-4o-mini                | gpt-4o                     | 46        | 57        | 51            |
| gpt-4o-mini                | gpt-4o-mini                | 55        | 43        | 49            |

This benchmark highlights distinctive strengths among different AI models. Claude-3.5-sonnet and GPT-4o show close competition, often achieving similar scores. GPT-4o and its mini variant generally outperform GPT-3.5-turbo, highlighting generational improvements. GPT-4o-mini performs competitively, often close to its full-sized counterpart.

## 🛠 Getting Started

### Prerequisites

- Python 3.9+
- API keys for OpenAI, Google, and Anthropic (as needed)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/mrconter1/model-clash.git
   cd MODEL-CLASH
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

Here are two examples of challenges generated by GPT-4o during ModelClash duels:

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

These examples showcase the diversity and complexity of challenges that can be created in real-time by AI models.

## 🤝 Contributing

Contributions are welcome! Please fork the project, create a feature branch, and open a pull request.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📬 Contact

Rasmus Lindahl - rasmus.lindahl1996@gmail.com

Project Link: [https://github.com/mrconter1/ModelClash](https://github.com/mrconter1/ModelClash)

---

<p align="center">Made with ❤️ for the advancement of AI</p>