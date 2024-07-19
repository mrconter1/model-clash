from game_logic import play_game
from prompts import create_challenge_prompt

# Define models
MODEL1 = {"name": "gpt-4o", "provider": "openai"}
MODEL2 = {"name": "gpt-4o-mini", "provider": "openai"}

# Number of rounds
NUM_ROUNDS = 100

def main():
    challenge_prompt = create_challenge_prompt()
    play_game(MODEL1, MODEL2, NUM_ROUNDS, challenge_prompt)

if __name__ == "__main__":
    main()