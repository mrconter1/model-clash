from game_logic import run_tournament, print_results_table
from model import Model

def main():
    models = [
        Model("gpt-4o", "openai"),
        Model("gpt-4o-mini", "openai"),
        Model("gpt-3.5-turbo", "openai"),
        # Model("claude-3.5-sonnet", "anthropic"),
        # Add more models as needed
    ]

    num_rounds = 10
    results = run_tournament(models, num_rounds)
    print_results_table(models, results)

if __name__ == "__main__":
    main()