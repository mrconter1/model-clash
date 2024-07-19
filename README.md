# ModelClash: Dynamic LLM Evaluation Arena

## 🚀 About ModelClash

ModelClash is a framework designed to evaluate and compare Large Language Models (LLMs) in a dynamic, competitive environment. By pitting AI models against each other in a series of creative problem-solving challenges, this project offers a approach to benchmarking that adapts to the rapid advancements in AI technology.

### 🌟 Key Features

- **Self-Generating Challenges**: Models create and solve complex problems, eliminating the need for manual dataset creation.
- **Adaptive Difficulty**: Automatically scales to match any level of AI intelligence.
- **Comprehensive Evaluation**: Tests a broad spectrum of skills including creativity, strategy, and self-awareness.

## 🧠 Why ModelClash?

Traditional benchmarks for Language Models often suffer from quick saturation and lack of adaptability. ModelClash addresses these issues with three core advantages:

1. **Automated, Testable Challenge Generation**
   - Eliminates the need for expert-created datasets
   - Reduces human bias in evaluation
   - Provides quantifiable results through an innovative scoring system

2. **Intelligence-Adaptive Testing**
   - Automatically adjusts to any level of model capability
   - Ensures long-term relevance as AI technology advances
   - Addresses the issue of benchmark saturation

3. **Holistic Intelligence Assessment**
   - Evaluates a wide range of cognitive skills
   - Tests both problem-solving and problem-creation abilities
   - Challenges models in creativity, strategy, and understanding of limitations

## 🛠 Getting Started

### Prerequisites

- Python 3.9+
- API keys for the models you want to test:
  - OpenAI API key (for OpenAI models)
  - Google API key (for Google models)
  - Anthropic API key (for Anthropic models)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ModelClash.git
   cd ModelClash
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables for the API keys of the models you want to use:
   ```
   export OPENAI_API_KEY='your-openai-api-key-here'
   export GOOGLE_API_KEY='your-google-api-key-here'
   export ANTHROPIC_API_KEY='your-anthropic-api-key-here'
   ```
   Note: You only need to set the API keys for the models you intend to use in your tests.

### Usage

Run the main script to start a competition:

```
python -m modelclash.main
```

Note: Ensure you have set the API keys for the models you want to include in your tests before running the script.

## 📊 Example Challenges

ModelClash results in diverse, algorithmic challenges generated in real-time. Here are two examples created by GPT-4o:

### 1. Character Sorting and Deduplication
```python
assert X("banana") == "abn"
assert X("apple") == "aelp"
assert X("racecar") == "acer"
```

### 2. Morse Code Converter
```python
assert X("SOS") == "... --- ..."
assert X("HELLO") == ".... . .-.. .-.. ---"
assert X("123") == ".---- ..--- ...--"
```

These examples demonstrate the variety and complexity of challenges created dynamically by competing models during ModelClash tournaments.

## 📈 Results

This section will be updated with the latest results from ModelClash competitions. Stay tuned for insights into the performance of various LLMs across different challenges.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📬 Contact

Rasmus Lindahl - rasmus.lindahl1996@gmail.com

Project Link: [https://github.com/mrconter1/ModelClash](https://github.com/mrconter1/ModelClash)

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/)
- [Google AI](https://ai.google/)
- [Anthropic](https://www.anthropic.com/)

---

<p align="center">Made with ❤️ for the advancement of AI</p>