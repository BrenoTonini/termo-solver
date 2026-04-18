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

def random_word(word_list = VALID_INPUTS):
    return random.choice(word_list)

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
            continue
        
        elif guess[i] not in correct_answer:
            attempt.append([guess[i], WRONG])
            continue

        ocurrences = guess.count(guess[i])
        correct_ocurrences = correct_answer.count(guess[i])
        if ocurrences > correct_ocurrences:
            attempt.append([guess[i], WRONG])
            continue

        attempt.append([guess[i], CLOSE])

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

def filter_correct_characters(attempt, word):
    for i in range(len(attempt)):
        if attempt[i][1] == CORRECT:
            if word[i] != attempt[i][0]: 
                return False
            
    return True

def filter_close_characters(attempt, word):
    for i in range(len(attempt)):
        if attempt[i][1] == CLOSE:
            if attempt[i][0] not in word or word[i] == attempt[i][0]: 
                return False
            
    return True

def filter_wrong_characters(attempt, word):
    attempted_word = [attempt[i][0] for i in range(len(attempt))]
    for i in range(len(attempt)):
        if attempt[i][1] == WRONG:
            if attempt[i][0] in word: 
                correct_ocurrences = attempted_word.count(attempt[i][0])
                if correct_ocurrences == 0:
                    return False
                
    return True

def filter_attempted_word(attempt, word):
    attempted_word = ''.join([attempt[i][0] for i in range(len(attempt))])
    if attempted_word == word:
        return False
            
    return True

def get_remainig_possibilities(attempts):
    possible_words = VALID_INPUTS

    for attempt in attempts:
        possible_words = list(filter(lambda word: filter_correct_characters(attempt, word), possible_words))
        possible_words = list(filter(lambda word: filter_close_characters(attempt, word), possible_words))
        possible_words = list(filter(lambda word: filter_wrong_characters(attempt, word), possible_words))
        possible_words = list(filter(lambda word: filter_attempted_word(attempt, word), possible_words))

    return possible_words


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
        guess = random_word(get_remainig_possibilities(game_context['attempts']))
        if mode != 'auto':
            guess = wait_user_input()

        attempt = new_attempt(guess, correct_answer)
        game_context['attempts'].append(attempt)

        display_feedback(game_context['attempts'])

        if mode == 'assisted':
            get_remainig_possibilities(game_context['attempts'])

        if guess == correct_answer:
            print("Parabéns! Você acertou a palavra!")
            break

def run_test(n):
    wins = 0
 
    for i in range(n):
        correct_answer = random_word()
        attempts = []
 
        while len(attempts) < ATTEMPTS_LIMIT:
            guess = random_word(get_remainig_possibilities(attempts))
            attempt = new_attempt(guess, correct_answer)
            attempts.append(attempt)
 
            if guess == correct_answer:
                wins += 1
                break
 
        print(f"[{i + 1}/{n}] palavra: {correct_answer} | tentativas: {len(attempts)} | {'✓' if guess == correct_answer else '✗'}")
 
    print()
    print(f"resultado: {wins}/{n} ({(wins / n * 100):.1f}% de acerto)")


def init_config():
    parser = argparse.ArgumentParser(description="Termo Solver")
    parser.add_argument('--sanitize', action='store_true', help='gera dicionário de palavras válidas')
    parser.add_argument('--mode', choices=['default', 'assisted', 'auto'], default='default', help='Modo de operação do solver')
    parser.add_argument('--test', type=int, metavar='N', help='testa a acurácia do solver automático em N partidas')

    args = parser.parse_args()

    if args.test:
        run_test(args.test)
        return

    selected_mode = str(args.mode)

    game_context = {
        'mode': selected_mode,
        'attempts': [],
    }
    
    start_solver(game_context)

if __name__ == "__main__":
    init_config()