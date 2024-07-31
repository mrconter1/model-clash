# 🏆 ModelClash: Autonomous AI Tournament

Autonomous AI tournament platform where language models compete by creating and solving self-generated challenges across diverse domains. Unlike other benchmarks, ModelClash offers a diverse human-free approach to AI evaluation that automatically scale with model capabilities, naturally resists benchmark saturation, and assesses both problem-solving and problem-creation skills.

## 🏅 Tournament Results

<div align="center">

| Model                   | Score (50 rounds) |
|:-----------------------:|:-----:|
| claude-3.5-sonnet       | 139   |
| gpt-3.5-turbo           | 126   |
| gemini-pro-1.5          | 123   |
| llama-3.1-405b-instruct | 123   |
| gpt-4-turbo             | 119   |
| gpt-4o-mini             | 114   |
| claude-3-opus           | 111   |
| gpt-4o                  | 109   |
| mistral-large           | 95    |
| llama-3.1-70b-instruct  | 85    |
| llama-3.1-8b-instruct   | 66    |

</div>

## 🧠 How ModelClash Works

### 🏟️ Tournament Structure

The tournament consists of a configurable number of rounds per participating model. Each model's final score is the sum of points earned across all rounds.

### 🎯 Round Gameplay

1. **Challenge Creation**: Creates any type of challenge by creating test cases that it knows it could solve by figuring out and implementing a function X.
2. **Self-Solving**: The creator, with no memory of the creation process, tries to solve its own challenge.
3. **Opponent Solving**: If the creator succeeds, other models attempt the challenge.

This process is repeated for a predetermined number of rounds for each model, ensuring every participant gets an equal number of opportunities to create challenges.

### 📊 Round Scoring

If model fails to create a parsable problem or solve its own challenge, the round ends.

In case of a valid challenge:
- For successful self-solve: Creator gains 1 point
- For each stumped opponent: Creator gains 1 point
- For each successful opponent: Opponent gains 1 point

## 📈 Comparison to traditional benchmarks

| Feature                                           | ModelClash | MMLU | HellaSwag | GSM-8K | MT-Bench | AlpacaEval | Chatbot Arena |
|---------------------------------------------------|:----------:|:----:|:---------:|:------:|:--------:|:----------:|:-------------:|
| General challenges                                |     ✔️     |  ✔️  |     ✔️    |   ❌   |    ✔️    |     ❌     |      ✔️       |
| Automatic evaluation                              |     ✔️     |  ✔️  |     ✔️    |   ✔️   |    ✔️    |     ✔️     |      ❌       |
| Immune to dataset leakage                         |     ✔️     |  ❌  |     ❌    |   ❌   |    ❌    |     ❌     |      ✔️       |
| Human-free challenge design                       |     ✔️     |  ❌  |     ❌    |   ❌   |    ❌    |     ❌     |      ❌       |
| Automatically scales to model capabilities        |     ✔️     |  ❌  |     ❌    |   ❌   |    ❌    |     ❌     |      ❌       |
| Tests both problem creation and solving abilities |     ✔️     |  ❌  |     ❌    |   ❌   |    ❌    |     ❌     |      ❌       |

## ❓ Frequently Asked Questions

**Q: What prevents a model from making nonsensical, ambiguous, impossible or unfair challenges?**

A: If it fails to solve its own challenge it won't get any score that round.

**Q: What prevents a highly specialized model in domain expertise, programming or mathematics from winning?**

A: Specialized models may excel in their niche but struggle elsewhere, limiting their overall score.

## 🚀 Getting Started

### 📋 Prerequisites

- Python 3.9+
- OpenRouter API key

### 💻 Installation

1. Clone the repository:
   ```
   git clone https://github.com/mrconter1/model-clash
   cd MODEL-CLASH
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up API key environment variable:
   ```
   export OPENROUTER_API_KEY='your-openrouter-api-key'
   ```

### 🖥️ Usage

Run the main script:

```
python main.py
```

## 👥 Contributing

Contributions are welcome! Please fork the project, create a feature branch, and open a pull request.

## 📚 Citation

If you use ModelClash in your research or wish to refer to it, please use the following BibTeX entry:

```bibtex
@misc{lindahl2024modelclash,
  author = {Lindahl, Rasmus},
  title = {ModelClash: Autonomous AI Tournament with Self-Generated Challenges for Competitive Language Model Evaluation},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/mrconter1/model-clash}}
}
```

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

Rasmus Lindahl - rasmus.lindahl1996@gmail.com

---

<p align="center">Made with ❤️ for the advancement of AI</p>