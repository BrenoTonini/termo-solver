import os
import argparse
import unicodedata
import random

def load_valid_inputs():
    valid_inputs_path = os.path.join(os.path.dirname(__file__), 'dictionary', 'valid-inputs.txt')
    with open(valid_inputs_path, 'r') as file:
        valid_inputs = [line.strip() for line in file.readlines()]
    return valid_inputs

VALID_INPUTS = load_valid_inputs()
ATTEMPTS_LIMIT = 6
CORRECT = '#'
CLOSE = '*'
WRONG = '-'

def random_word():
    return random.choice(VALID_INPUTS)

def wait_user_input():
    user_input = input("Sua resposta: ").lower()
    user_input_ascii = unicodedata.normalize('NFKD', user_input).encode('ascii', 'ignore').decode('ascii')

    if not validate_input(user_input_ascii, VALID_INPUTS):
        return wait_user_input()
    
    return user_input_ascii.strip()

def validate_input(input, valid_inputs):
    if len(input) != 5 or input not in valid_inputs:
        print("essa palavra não é aceita")
        print()
        return False
    return True

def new_attempt(guess, correct_answer):
    attempt = []
    for i in range(5):
        if guess[i] == correct_answer[i]:
            attempt.append([guess[i], CORRECT])
        elif guess[i] in correct_answer:
            attempt.append([guess[i], CLOSE])
        else:
            attempt.append([guess[i], WRONG])

    return attempt

def display_feedback(attempts):
    os.system('cls' if os.name == 'nt' else 'clear')

    for attempt in attempts:
        print("")
        for i in range(len(attempt)):
            print(attempt[i][1] + ' ', end='')
        
        print()

        for i in range(len(attempt)):
            print(attempt[i][0] + ' ', end='')

        print()
        print()

def start_solver(game_context):
    mode = game_context['mode']
    correct_answer = random_word()

    if mode == 'default':
        print("Iniciando solver")
    elif mode == 'assisted':
        print("Iniciando solver assistido")
    elif mode == 'auto':
        print("Iniciando solver automático")

    while len(game_context['attempts']) < ATTEMPTS_LIMIT:
        guess = wait_user_input()
        attempt = new_attempt(guess, correct_answer)
        game_context['attempts'].append(attempt)

        display_feedback(game_context['attempts'])

        if guess == correct_answer:
            print("Parabéns! Você acertou a palavra!")
            break


def init_config():
    parser = argparse.ArgumentParser(description="Termo Solver")
    parser.add_argument('--sanitize', action='store_true', help='gera dicionário de palavras válidas')
    parser.add_argument('--mode', choices=['default', 'assisted', 'auto'], default='default', help='Modo de operação do solver')

    args = parser.parse_args()

    selected_mode = str(args.mode)

    game_context = {
        'mode': selected_mode,
        'attempts': [],
    }
    
    start_solver(game_context)

if __name__ == "__main__":
    init_config()