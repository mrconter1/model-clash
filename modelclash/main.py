from game_logic import run_tournament, print_results_table

def main():
    models = [
        {"name": "gpt-4o", "provider": "openai"},
        {"name": "gpt-4o-mini", "provider": "openai"},
        {"name": "gpt-3.5-turbo", "provider": "openai"},
        # {"name": "claude-3.5-sonnet", "provider": "anthropic"},
        # Add more models as needed
    ]

    num_rounds = 3
    results = run_tournament(models, num_rounds)
    print_results_table(models, results)

if __name__ == "__main__":
    main()