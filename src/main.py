import os
import argparse
import unicodedata
import random
import time

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
    char_info = {}

    for char, status in attempt:
        if char not in char_info:
            char_info[char] = {
                "min": 0,
                "total": 0
            }

        char_info[char]["total"] += 1

        if status in (CORRECT, CLOSE):
            char_info[char]["min"] += 1

    for char, info in char_info.items():
        count = word.count(char)

        if count < info["min"]:
            return False

        if info["total"] > info["min"]:
            if count > info["min"]:
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

def build_frequency(candidates):
    freq = {}
    for word in candidates:
        for c in set(word):
            freq[c] = freq.get(c, 0) + 1
    return freq


def score_word(word, freq):
    score = 0
    used = set()

    for c in word:
        if c in used:
            continue
        score += freq.get(c, 0)
        used.add(c)

    return score


def best_word(candidates):
    if not candidates:
        return random_word()
    
    freq = build_frequency(candidates)

    best = None
    best_score = -1

    for word in candidates:
        score = score_word(word, freq)

        if score > best_score:
            best_score = score
            best = word

    return best


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
        guess = best_word(get_remainig_possibilities(game_context['attempts']))
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
    wins_by_attempt = {i: 0 for i in range(1, ATTEMPTS_LIMIT + 1)}
    losses = 0
    loss_records = []

    start_time = time.perf_counter()
 
    for i in range(n):
        correct_answer = random_word()
        attempts = []
 
        while len(attempts) < ATTEMPTS_LIMIT:
            candidates = get_remainig_possibilities(attempts)
            guess = best_word(candidates)
            attempt = new_attempt(guess, correct_answer)
            attempts.append(attempt)
 
            if guess == correct_answer:
                wins += 1
                wins_by_attempt[len(attempts)] += 1
                break
        else:
            losses += 1
            guesses = guesses = ', '.join(''.join(c[0] for c in attempt) for attempt in attempts)
            remaining = len(get_remainig_possibilities(attempts))
            loss_records.append(f"answer: {correct_answer}, attempts: {guesses}, remaining: {remaining}")
 
        print(f"[{i + 1}/{n}] palavra: {correct_answer} | tentativas: {len(attempts)} | {'✓' if guess == correct_answer else '✗'}", end='\r')
    
    total_time = time.perf_counter() - start_time
    avg_time = total_time / n
 
    print('\n')
    print(f"resultado: {wins}/{n} ({(wins / n * 100):.1f}% de acerto) | derrotas: {losses}")
    print(f"tempo médio por partida: {avg_time:.6f}s")
    print()
    for attempt_n, count in wins_by_attempt.items():
        bar = '█' * (count * 20 // max(wins_by_attempt.values(), default=1))
        print(f"  {attempt_n} tentativa(s): {bar} {count} ({count / n * 100:.1f}%)")

    if loss_records:
        losses_dir = os.path.join(os.path.dirname(__file__), 'losses')
        os.makedirs(losses_dir, exist_ok=True)
        losses_path = os.path.join(losses_dir, 'losses.txt')
        with open(losses_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(loss_records))
        print(f"\nderrotas salvas em: {losses_path}")


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